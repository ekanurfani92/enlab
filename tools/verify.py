#!/usr/bin/env python3
"""
Pemeriksa kesehatan situs ENLab. Jalankan setelah menyunting konten:

    python3 tools/verify.py

Memeriksa: kelengkapan terjemahan, tautan dan aset lokal, keberadaan berkas
materi kuliah, kesahihan JSON-LD & manifest, struktur HTML, dan aksesibilitas dasar.
"""

import os, re, json, subprocess, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
PAGES = ["index.html", "publications.html", "teaching.html", "404.html"]
problems = []


def ok(label, detail=""):
    print("  \033[32mOK\033[0m   " + label.ljust(34) + detail)


def bad(label, detail=""):
    problems.append(label)
    print("  \033[31mGAGAL\033[0m " + label.ljust(34) + detail)


# ---- 1. terjemahan (pakai Node agar objek JS dibaca sungguhan) --------------
print("\n1. Terjemahan")
node_src = (
    "global.window={};require('./assets/js/i18n.js');"
    "const d=window.I18N;"
    "console.log(JSON.stringify({id:Object.keys(d.id),en:Object.keys(d.en)}));"
)
try:
    out = subprocess.run(["node", "-e", node_src], capture_output=True, text=True, check=True)
    dic = json.loads(out.stdout)
    KID, KEN = set(dic["id"]), set(dic["en"])
except Exception as e:
    bad("baca kamus i18n", str(e)[:60])
    KID = KEN = set()

used = set()
for p in PAGES:
    used |= set(re.findall(r'data-i18n="([^"]+)"', open(p, encoding="utf-8").read()))
# kunci yang dirujuk dari main.js: setiap literal berbentuk 'bagian.bagian'
_js = open("assets/js/main.js", encoding="utf-8").read()
used |= set(re.findall(r"'([a-z][a-z0-9]*(?:\.[a-z0-9]+)+)'", _js))
# kunci yang disusun saat berjalan, mis. 'pub.filter.' + p.k
used |= {"pub.filter.journal", "pub.filter.conference", "pub.filter.national"}

if KID:
    diff = (KID ^ KEN)
    ok("jumlah kunci", f"ID={len(KID)}  EN={len(KEN)}") if not diff else bad("ID/EN tidak sinkron", ", ".join(sorted(diff))[:70])
    miss = sorted(used - KID) + sorted(used - KEN)
    ok("kunci terpakai tersedia", f"{len(used)} kunci") if not miss else bad("kunci hilang", ", ".join(miss)[:70])
    unused = sorted(KID - used)
    ok("tidak ada kunci menganggur") if not unused else print("  \033[33mCATATAN\033[0m tidak terpakai: " + ", ".join(unused)[:70])

# ---- 2. tautan & aset lokal ------------------------------------------------
print("\n2. Tautan dan aset lokal")
broken = []
for p in PAGES:
    t = open(p, encoding="utf-8").read()
    for m in re.findall(r'(?:href|src)="([^"]+)"', t):
        if m.startswith(("http", "mailto:", "#", "data:", "javascript:")):
            continue
        tgt = m.lstrip("/").split("#")[0].split("?")[0]
        if tgt and not os.path.exists(tgt):
            broken.append(f"{p} -> {m}")
ok("seluruh tautan lokal hidup") if not broken else bad("tautan rusak", "; ".join(broken[:3]))

# ---- 3. berkas materi kuliah ----------------------------------------------
print("\n3. Materi kuliah")
cj = open("assets/js/data-courses.js", encoding="utf-8").read()
body = cj[cj.index("window.COURSES"):]
refs = re.findall(r'"f": ?"([^"]+)"', body)
missing = [r for r in refs if not os.path.exists(r)]
ok("berkas materi tersedia", f"{len(refs)} berkas") if not missing else bad("berkas hilang", "; ".join(missing[:3]))

# saklar penerbitan harus sejalan dengan .gitignore
_ign = False
if os.path.exists(".gitignore"):
    _ign = any(l.strip().rstrip("/") == "materi" for l in open(".gitignore", encoding="utf-8"))
_flag = re.search(r"window\.MATERI_TERSEDIA\s*=\s*(true|false)", cj)
_flag = (_flag.group(1) == "true") if _flag else True
if _ign and _flag:
    bad("saklar materi tidak sinkron",
        "materi/ diabaikan .gitignore tetapi MATERI_TERSEDIA=true -> tautan unduh akan rusak")
elif (not _ign) and (not _flag) and refs:
    bad("saklar materi tidak sinkron",
        "materi/ ikut terbit tetapi MATERI_TERSEDIA=false -> berkas terunggah tetapi tersembunyi")
else:
    ok("saklar materi sinkron",
       ("belum diterbitkan" if _ign else "diterbitkan") + f" ({len(refs)} berkas)")

orphan = []
for dirpath, _, files in os.walk("materi"):
    for f in files:
        if f.endswith(".pdf") and os.path.join(dirpath, f).replace(os.sep, "/") not in refs:
            orphan.append(os.path.join(dirpath, f))
ok("tidak ada berkas yatim") if not orphan else print("  \033[33mCATATAN\033[0m PDF tak terdaftar: " + ", ".join(orphan[:3]))

# ---- 4. JSON --------------------------------------------------------------
print("\n4. Data terstruktur")
t = open("index.html", encoding="utf-8").read()
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
try:
    g = json.loads(m.group(1))
    ok("JSON-LD sah", f'{len(g["@graph"])} entitas')
except Exception as e:
    bad("JSON-LD", str(e)[:60])
try:
    json.load(open("site.webmanifest", encoding="utf-8"))
    ok("site.webmanifest sah")
except Exception as e:
    bad("site.webmanifest", str(e)[:60])

# ---- 5. struktur HTML -----------------------------------------------------
print("\n5. Struktur HTML")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "source", "track", "wbr"}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.err = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.err.append(f"</{tag}> berlebih")
        elif self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.err.append(f"<{self.stack.pop()}> tidak ditutup")
            self.stack.pop()
        else:
            self.err.append(f"</{tag}> tak cocok")


for p in PAGES:
    c = Checker()
    c.feed(open(p, encoding="utf-8").read())
    left = [x for x in c.stack if x != "html"]
    ok(p) if not (c.err or left) else bad(p, "; ".join((c.err + left)[:3]))

# ---- 6. aksesibilitas & SEO ----------------------------------------------
print("\n6. Aksesibilitas dan SEO")
for p in PAGES:
    t = open(p, encoding="utf-8").read()
    issues = []
    if len([i for i in re.findall(r"<img\b[^>]*>", t) if "alt=" not in i]):
        issues.append("img tanpa alt")
    if len([i for i in re.findall(r"<iframe\b[^>]*>", t) if "title=" not in i]):
        issues.append("iframe tanpa title")
    if "<title" not in t:
        issues.append("tanpa <title>")
    if p != "404.html" and 'name="description"' not in t:
        issues.append("tanpa meta description")
    if t.count("<h1") != 1:
        issues.append(f"{t.count('<h1')} buah <h1>")
    if 'class="skip-link"' not in t and p != "404.html":
        issues.append("tanpa skip-link")
    ok(p) if not issues else bad(p, ", ".join(issues))

# ---- 7. teks cadangan HTML harus cocok dengan kamus Indonesia -------------
# Teks di dalam HTML dibaca mesin pencari dan pengunjung tanpa JavaScript.
# Bila ia menyimpang dari kamus, situs menampilkan dua versi berbeda.
print("\n7. Teks cadangan tanpa JavaScript")
try:
    node_src2 = ("global.window={};require('./assets/js/i18n.js');"
                 "console.log(JSON.stringify(window.I18N.id));")
    ID = json.loads(subprocess.run(["node", "-e", node_src2],
                                   capture_output=True, text=True, check=True).stdout)
except Exception as e:
    bad("baca kamus ID", str(e)[:60]); ID = {}

if ID:
    drift = []
    pat = re.compile(r'<(\w+)([^>]*\bdata-i18n="([^"]+)"[^>]*)>(.*?)</\1>', re.S)
    for pg in PAGES:
        txt = open(pg, encoding="utf-8").read()
        for tag, attrs, key, inner in pat.findall(txt):
            if "data-i18n-attr" in attrs or key not in ID:
                continue
            shown = re.sub(r"<[^>]+>", "", inner)
            shown = (shown.replace("&amp;", "&").replace("&nbsp;", " ")
                          .replace("&lt;", "<").replace("&gt;", ">"))
            shown = re.sub(r"\s+", " ", shown).strip()
            want = re.sub(r"<[^>]+>", "", ID[key])
            want = re.sub(r"\s+", " ", want).strip()
            if not shown or shown == want:
                continue
            # teks cadangan boleh lebih pendek, asal awalannya sama
            if want.startswith(shown.rstrip(".")):
                continue
            drift.append(f"{pg}:{key}")
    ok("teks cadangan selaras", f"{len(ID)} kunci diperiksa") if not drift \
        else bad("teks cadangan menyimpang", ", ".join(drift[:4]))

print("\n" + ("=" * 62))
print("HASIL: SEMUA PEMERIKSAAN LOLOS" if not problems
      else f"HASIL: {len(problems)} MASALAH -> " + ", ".join(problems[:5]))
print("=" * 62)
sys.exit(1 if problems else 0)
