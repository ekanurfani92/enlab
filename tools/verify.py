#!/usr/bin/env python3
"""
Pemeriksa kesehatan situs ENLab. Jalankan setelah menyunting konten:

    python3 tools/verify.py

Memeriksa: kelengkapan terjemahan, tautan dan aset lokal, keberadaan berkas
materi kuliah, kesahihan JSON-LD & manifest, struktur HTML, dan aksesibilitas dasar.
"""

import os, re, json, glob, subprocess, sys
from html.parser import HTMLParser
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
# Halaman mata kuliah di mk/ ikut diperiksa; jumlahnya mengikuti data-courses.js.
PAGES = (["index.html", "publications.html", "theses.html", "teaching.html", "404.html"]
         + sorted(glob.glob("mk/*.html")))
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
        raw = unquote(m.split("#")[0].split("?")[0])
        if not raw:
            continue
        # Jalur relatif dihitung dari letak halamannya, bukan dari akar repo,
        # supaya "../assets/..." pada halaman di mk/ ikut terperiksa benar.
        tgt = (raw.lstrip("/") if m.startswith("/")
               else os.path.normpath(os.path.join(os.path.dirname(p), raw)))
        if not os.path.exists(tgt):
            broken.append(f"{p} -> {m}")
ok("seluruh tautan lokal hidup") if not broken else bad("tautan rusak", "; ".join(broken[:3]))

# ---- 3. berkas materi kuliah ----------------------------------------------
print("\n3. Materi kuliah")
cj = open("assets/js/data-courses.js", encoding="utf-8").read()
body = cj[cj.index("window.COURSES"):]
refs = re.findall(r'"f": ?"([^"]+)"', body)
missing = [r for r in refs if not os.path.exists(r)]
ok("berkas materi tersedia", f"{len(refs)} berkas") if not missing else bad("berkas hilang", "; ".join(missing[:3]))

# Penerbitan diatur per mata kuliah. Kolom "pub" pada data harus sejalan
# dengan keputusan git, agar daftar di situs tidak pernah menjanjikan berkas
# yang sebenarnya tidak ikut terunggah.
_courses = json.loads(subprocess.run(
    ["node", "-e", "global.window={};require('./assets/js/data-courses.js');"
                   "console.log(JSON.stringify(window.COURSES));"],
    capture_output=True, text=True, check=True).stdout)

def _ditahan(slug):
    return subprocess.run(["git", "check-ignore", "-q", f"materi/{slug}"],
                          capture_output=True).returncode == 0

_beda = []
for _c in _courses:
    if bool(_c.get("pub")) == _ditahan(_c["slug"]):
        _beda.append(_c["slug"])
_terbit = [c for c in _courses if c.get("pub")]
_n_terbit = sum(len(c["m"]) for c in _terbit)
if _beda:
    bad("status terbit tidak sinkron", ", ".join(_beda[:3]) + " (jalankan tools/sync_materi.py)")
else:
    ok("status terbit sinkron",
       f"{len(_terbit)} mata kuliah terbit, {_n_terbit} berkas")

_TERLARANG = {"rps", "kontrak", "nilai", "dna", "kunci", "jawaban", "rubrik",
              "absensi", "presensi", "uas", "uts", "quiz", "ujian", "penilaian"}
_curiga = []
for _c in _courses:
    for _m in _c["m"]:
        _kata = set(re.split(r"[^a-z0-9]+", os.path.basename(_m["f"]).lower()))
        if _kata & _TERLARANG:
            _curiga.append((_m["f"], bool(_c.get("pub"))))
_akan_terbit = [f for f, pub in _curiga if pub]
if _akan_terbit:
    bad("berkas administratif akan terbit", "; ".join(_akan_terbit[:3]))
elif _curiga:
    print("  \033[33mCATATAN\033[0m nama mirip dokumen administratif (masih ditahan): "
          + ", ".join(f for f, _ in _curiga[:3]))
else:
    ok("tidak ada berkas administratif")

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
