#!/usr/bin/env python3
"""
Pembangun halaman statis ENLab.

Header, footer, dan bagian <head> ditulis sekali di berkas ini lalu disisipkan
ke setiap halaman. Setelah mengubah navigasi atau footer, jalankan:

    python3 tools/build_pages.py

Hasilnya adalah HTML statis biasa (index.html, publications.html,
teaching.html) yang tetap bisa disunting langsung bila diperlukan.
"""

import os
import re
import glob
import json
import html as _html
import subprocess
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://ekanurfani92.github.io/enlab"   # ganti bila memakai domain sendiri
TODAY = datetime.date.today().isoformat()
_DICT_ID = None  # diisi saat dijalankan

# --------------------------------------------------------------------------- #
# Bagian bersama
# --------------------------------------------------------------------------- #

HEAD = """  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0d6e6e" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#051614" media="(prefers-color-scheme: dark)">
  <meta name="author" content="Dr. Eka Nurfani, S.Si., M.Si.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="__CANON__">
  <link rel="icon" href="assets/img/favicon.png" type="image/png" sizes="180x180">
  <link rel="apple-touch-icon" href="assets/img/favicon.png">
  <link rel="manifest" href="site.webmanifest">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="ENLab ITERA">
  <meta property="og:locale" content="id_ID">
  <meta property="og:locale:alternate" content="en_US">
  <meta property="og:url" content="__CANON__">
  <meta property="og:title" content="__OGTITLE__">
  <meta property="og:description" content="__DESC__">
  <meta property="og:image" content="__SITE__/assets/img/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="__OGTITLE__">
  <meta name="twitter:description" content="__DESC__">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Manrope:wght@600;700;800&amp;display=swap">
  <link rel="stylesheet" href="assets/css/style.css">

  <script>
    /* Terapkan tema sebelum render agar tidak berkedip, dan tandai JS aktif
       sehingga konten tetap terlihat bila JavaScript dimatikan. */
    (function () {
      var d = document.documentElement;
      d.classList.add('js');
      try {
        var s = localStorage.getItem('enlab-theme');
        if (s === 'dark' || s === 'light') d.setAttribute('data-theme', s);
      } catch (e) {}
    })();
  </script>
"""


def header(active=""):
    def cur(name):
        return ' aria-current="page"' if active == name else ""

    return """  <a class="skip-link" href="#main" data-i18n="skip">Lompat ke konten utama</a>

  <header class="site-header">
    <div class="container nav-wrap">
      <a class="brand" href="index.html" aria-label="ENLab">
        <img class="brand-logo" src="assets/img/logo-emblem.png" alt="" width="68" height="40">
        <span class="brand-text">
          <strong>ENLab</strong>
          <span data-i18n="brand.sub" data-i18n-html><b>EN</b>ergy Materials and Semiconductor Laboratory</span>
        </span>
      </a>

      <nav class="site-nav" id="site-nav" aria-label="Utama">
        <a href="index.html#about" data-i18n="nav.about">Tentang</a>
        <a href="index.html#research" data-i18n="nav.research">Riset</a>
        <a href="index.html#team" data-i18n="nav.team">Tim</a>
        <a href="index.html#facilities" data-i18n="nav.facilities">Fasilitas</a>
        <a href="publications.html\"""" + cur("pub") + """ data-i18n="nav.publications">Publikasi</a>
        <a href="theses.html\"""" + cur("theses") + """ data-i18n="nav.theses">Tugas Akhir</a>
        <a href="teaching.html\"""" + cur("teach") + """ data-i18n="nav.teaching">Pengajaran</a>
        <a href="index.html#contact" data-i18n="nav.contact">Kontak</a>
      </nav>

      <div class="nav-tools">
        <div class="lang-switch" role="group" aria-label="Bahasa / Language">
          <button type="button" data-lang-btn="id" aria-pressed="true">ID</button>
          <button type="button" data-lang-btn="en" aria-pressed="false">EN</button>
        </div>
        <button type="button" class="icon-btn theme-toggle"
                data-i18n="nav.theme" data-i18n-attr="aria-label"
                aria-label="Ganti mode terang/gelap">
          <svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.4M12 19.6V22M4.2 4.2l1.7 1.7M18.1 18.1l1.7 1.7M2 12h2.4M19.6 12H22M4.2 19.8l1.7-1.7M18.1 5.9l1.7-1.7"/></svg>
          <svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 14.6A8.6 8.6 0 0 1 9.4 3.5a8.6 8.6 0 1 0 11.1 11.1z"/></svg>
        </button>
        <button type="button" class="icon-btn menu-toggle" aria-controls="site-nav" aria-expanded="false"
                data-i18n="nav.menu" data-i18n-attr="aria-label" aria-label="Buka menu navigasi">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 6.5h17M3.5 12h17M3.5 17.5h17"/></svg>
        </button>
      </div>
    </div>
  </header>
"""


FOOTER = """  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-about">
          <a class="brand" href="index.html" aria-label="ENLab">
            <img class="brand-logo" src="assets/img/logo-emblem.png" alt="" width="68" height="40">
            <span class="brand-text"><strong>ENLab</strong></span>
          </a>
          <p class="footer-tagline" data-i18n="brand.tagline">Inovasi Material untuk Teknologi Energi dan Semikonduktor</p>
          <p data-i18n="foot.about">Kelompok riset material energi dan semikonduktor di Program Studi Teknik Material, Institut Teknologi Sumatera.</p>
        </div>
        <div>
          <h4 data-i18n="foot.explore">Jelajahi</h4>
          <ul>
            <li><a href="index.html#about" data-i18n="nav.about">Tentang</a></li>
            <li><a href="index.html#research" data-i18n="nav.research">Riset</a></li>
            <li><a href="index.html#team" data-i18n="nav.team">Tim</a></li>
            <li><a href="index.html#facilities" data-i18n="nav.facilities">Fasilitas</a></li>
          </ul>
        </div>
        <div>
          <h4 data-i18n="foot.resource">Sumber Daya</h4>
          <ul>
            <li><a href="publications.html" data-i18n="nav.publications">Publikasi</a></li>
            <li><a href="theses.html" data-i18n="nav.theses">Tugas Akhir</a></li>
            <li><a href="teaching.html" data-i18n="nav.teaching">Pengajaran</a></li>
            <li><a href="https://scholar.google.com/citations?user=5Sz8OyAAAAAJ" target="_blank" rel="noopener">Google Scholar</a></li>
            <li><a href="https://www.scopus.com/authid/detail.uri?authorId=57190941043" target="_blank" rel="noopener">Scopus</a></li>
            <li><a href="https://sinta.kemdikbud.go.id/authors/profile/6659724" target="_blank" rel="noopener">SINTA</a></li>
          </ul>
        </div>
        <div>
          <h4 data-i18n="foot.contact">Kontak</h4>
          <ul>
            <li><a href="mailto:eka.nurfani@mt.itera.ac.id">eka.nurfani@mt.itera.ac.id</a></li>
            <li><a href="https://mt.itera.ac.id" target="_blank" rel="noopener" data-i18n="foot.prodi">Program Studi Teknik Material</a></li>
            <li><a href="https://www.itera.ac.id" target="_blank" rel="noopener" data-i18n="foot.itera">Institut Teknologi Sumatera</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span data-year>__YEAR__</span> ENLab, ITERA. <span data-i18n="foot.rights">Seluruh hak cipta dilindungi.</span></span>
        <span><span data-i18n="foot.updated">Pembaruan terakhir</span>: <time datetime="__TODAY__">__TODAY__</time></span>
      </div>
    </div>
  </footer>

  <script src="assets/js/i18n.js"></script>
  <script src="assets/js/data-publications.js"></script>
  <script src="assets/js/data-courses.js"></script>
  <script src="assets/js/data-grants.js"></script>
  <script src="assets/js/data-theses.js"></script>
  <script src="assets/js/main.js"></script>
"""

JSONLD = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "ResearchOrganization",
        "@id": "__SITE__/#lab",
        "name": "ENLab",
        "alternateName": "ENergy Materials and Semiconductor Laboratory",
        "url": "__SITE__/",
        "description": "Kelompok riset material energi dan semikonduktor di Program Studi Teknik Material, Institut Teknologi Sumatera.",
        "email": "eka.nurfani@mt.itera.ac.id",
        "parentOrganization": {
          "@type": "CollegeOrUniversity",
          "name": "Institut Teknologi Sumatera",
          "url": "https://www.itera.ac.id"
        },
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "Gedung D Ruang D208, Jalan Terusan Ryacudu, Way Huwi",
          "addressLocality": "Jati Agung",
          "addressRegion": "Lampung Selatan, Lampung",
          "postalCode": "35365",
          "addressCountry": "ID"
        },
        "knowsAbout": [
          "Perovskite solar cells", "Dye-sensitized solar cells", "Supercapacitors",
          "Metal oxide thin films", "Photodetectors", "Photocatalysis", "ZnO", "TiO2"
        ]
      },
      {
        "@type": "Person",
        "@id": "__SITE__/#eka-nurfani",
        "name": "Eka Nurfani",
        "honorificPrefix": "Dr.",
        "jobTitle": "Kepala ENLab, Lektor Kepala",
        "email": "eka.nurfani@mt.itera.ac.id",
        "worksFor": { "@id": "__SITE__/#lab" },
        "alumniOf": [
          { "@type": "CollegeOrUniversity", "name": "Universitas Jenderal Soedirman" },
          { "@type": "CollegeOrUniversity", "name": "Institut Teknologi Bandung" }
        ],
        "sameAs": [
          "https://scholar.google.com/citations?user=5Sz8OyAAAAAJ",
          "https://www.scopus.com/authid/detail.uri?authorId=57190941043",
          "https://sinta.kemdikbud.go.id/authors/profile/6659724"
        ]
      }
    ]
  }
  </script>
"""



def _courses():
    """Daftar mata kuliah dibaca dari sumber yang sama dengan yang dipakai situs."""
    src = ("global.window={};require('./assets/js/data-courses.js');"
           "console.log(JSON.stringify(window.COURSES));")
    out = subprocess.run(["node", "-e", src], cwd=ROOT,
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def _theses():
    """Daftar tugas akhir dibaca dari sumber yang sama dengan yang dipakai situs."""
    src = ("global.window={};require('./assets/js/data-theses.js');"
           "console.log(JSON.stringify(window.THESES));")
    out = subprocess.run(["node", "-e", src], cwd=ROOT,
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def theses_fallback(theses, dic):
    """Cadangan HTML statis daftar tugas akhir.

    main.js menggambar ulang bagian ini dari window.THESES, tetapi teks di sini
    yang dibaca mesin pencari dan pengunjung tanpa JavaScript.
    """
    esc = lambda x: _html.escape(x, quote=False)
    years = sorted({x["y"] for x in theses}, reverse=True)
    out = []
    for y in years:
        rows = [x for x in theses if x["y"] == y]
        items = "".join(
            '\n            <li class="thesis"><h3>%s</h3>'
            '<p class="thesis-by">%s</p></li>'
            % (esc(x["t"]["id"]), esc(x["n"]))
            for x in rows)
        out.append(
            '\n        <section class="thesis-group reveal">'
            '\n          <div class="thesis-group-head"><h2>%d</h2>'
            '<span class="thesis-group-n">%s</span></div>'
            '\n          <ul class="thesis-list">%s\n          </ul>'
            '\n        </section>' % (y, esc(dic["thesis.group.n"].replace("{n}", str(len(rows)))), items))
    return "".join(out) + "\n      "


def _q(path):
    """Menyandikan tiap ruas jalur agar nama berkas bertanda baca tetap sah."""
    from urllib.parse import quote
    return "/".join(quote(seg) for seg in path.split("/"))


def size_label(mb):
    """Berkas kecil ditulis dalam KB; "0 MB" terbaca seperti berkas rusak."""
    if not mb:
        return ""
    return f"{round(mb * 1024)} KB" if mb < 1 else f"{mb:.1f} MB"


def course_body(c, dic):
    """Isi halaman satu mata kuliah.

    Teks Bahasa Indonesia ditulis langsung ke HTML sebagai cadangan bagi mesin
    pencari dan pengunjung tanpa JavaScript; main.js menggambar ulang bagian
    ini dari window.COURSES saat bahasa diganti.
    """
    esc = lambda x: _html.escape(x, quote=False)
    chips = ['<span class="chip chip-code">%s</span>' % esc(c["kode"])] if c.get("kode") else []
    if c.get("sks"):
        chips.append('<span class="chip chip-neutral">%s %s</span>'
                     % (esc(c["sks"]), esc(dic["teach.sks"])))
    chips.append('<span class="chip chip-neutral">%s</span>' % esc(c["prodiName"]["id"]))
    if c.get("pub") and c["m"]:
        chips.append('<span class="chip">%d %s</span>' % (len(c["m"]), esc(dic["teach.materials"])))

    if c.get("pub") and c["m"]:
        items = "".join(
            '\n            <li><a class="material" href="%s" target="_blank" rel="noopener">'
            '<span class="pdf-ico">PDF</span><div><b>%s</b></div>'
            '<small>%s</small></a></li>'
            % (_q(m["f"]), esc(m["t"]), size_label(m["s"])) for m in c["m"])
        materials = '<ul class="material-list">%s\n          </ul>' % items
    else:
        materials = '<p class="no-material">%s</p>' % esc(dic["teach.nomaterial"])

    note = ('\n          <p class="course-note">%s</p>' % esc(c["note"]["id"])) if c.get("note") else ""

    return """
    <section class="page-head">
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <a href="index.html" data-i18n="nav.home">Beranda</a>
          <span aria-hidden="true">/</span>
          <a href="teaching.html" data-i18n="nav.teaching">Pengajaran</a>
          <span aria-hidden="true">/</span>
          <span data-course-title>__TITLE__</span>
        </nav>
        <h1 data-course-title>__TITLE__</h1>
        <div class="course-meta" id="course-chips" style="margin-top:14px">__CHIPS__</div>
      </div>
    </section>

    <section class="section" style="padding-top:clamp(30px,4vw,48px)">
      <div class="container">
        <div id="course-page" data-course="__SLUG__" class="course-body course-body-page">
          <p>__DESC__</p>__NOTE__
          __MATERIALS__
        </div>
        <p style="margin-top:32px">
          <a class="btn btn-ghost" href="teaching.html" data-i18n="teach.back">Kembali ke daftar mata kuliah</a>
        </p>
      </div>
    </section>
""".replace("__TITLE__", esc(c["t"]["id"])) \
   .replace("__CHIPS__", "".join(chips)) \
   .replace("__SLUG__", c["slug"]) \
   .replace("__DESC__", esc(c["d"]["id"])) \
   .replace("__NOTE__", note) \
   .replace("__MATERIALS__", materials)


def write_sitemap(courses):
    urls = [(SITE_URL + "/", "1.0"),
            (SITE_URL + "/publications.html", "0.8"),
            (SITE_URL + "/theses.html", "0.8"),
            (SITE_URL + "/teaching.html", "0.8")]
    urls += [(SITE_URL + "/mk/" + c["slug"] + ".html", "0.7")
             for c in courses if c.get("pub")]
    body = "".join(
        "  <url>\n"
        "    <loc>%s</loc>\n"
        "    <lastmod>%s</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        "    <priority>%s</priority>\n"
        "  </url>\n" % (loc, TODAY, pr) for loc, pr in urls)
    out = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + body + "</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(out)
    return len(urls)


def _dictionary_id():
    """Membaca kamus Bahasa Indonesia dari assets/js/i18n.js melalui Node."""
    src = ("global.window={};require('./assets/js/i18n.js');"
           "console.log(JSON.stringify(window.I18N.id));")
    out = subprocess.run(["node", "-e", src], cwd=ROOT,
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


_FILL = re.compile(r'(<(\w+)\b([^>]*\bdata-i18n="([^"]+)"[^>]*)>)(.*?)(</\2>)', re.S)


def fill_fallbacks(doc, dic):
    """Mengisi teks di dalam HTML dari kamus.

    Teks inilah yang dibaca mesin pencari dan pengunjung yang mematikan
    JavaScript. Dengan mengisinya dari sumber yang sama dengan yang dipakai
    JavaScript, isi halaman tidak mungkin lagi berbeda antara keduanya.
    """
    def rep(m):
        open_tag, _tag, attrs, key, _inner, close = m.groups()
        if "data-i18n-attr" in attrs or key not in dic:
            return m.group(0)
        val = dic[key]
        if "data-i18n-html" in attrs:
            return open_tag + val + close
        return open_tag + _html.escape(val, quote=False) + close

    return _FILL.sub(rep, doc)


_REL = re.compile(r'(\b(?:href|src)=")([^"]+)(")')


def retarget(doc, prefix):
    """Menaikkan jalur relatif satu tingkat untuk halaman di dalam subfolder.

    Header, footer, dan <head> ditulis untuk halaman di akar situs. Halaman
    mata kuliah berada di mk/, jadi setiap jalur relatif diberi awalan "../".
    """
    if not prefix:
        return doc

    def rep(m):
        pre, url, post = m.groups()
        if url.startswith(("http://", "https://", "//", "#", "mailto:", "data:", "/", prefix)):
            return m.group(0)
        return pre + prefix + url + post

    return _REL.sub(rep, doc)


def page(filename, lang_title_key, og_title, desc, body, active="", extra_head="",
         html_attr="", robots=None):
    canon = SITE_URL + "/" + ("" if filename == "index.html" else filename)
    head = (HEAD
            .replace("__CANON__", canon)
            .replace("__OGTITLE__", og_title)
            .replace("__DESC__", desc)
            .replace("__SITE__", SITE_URL))
    if robots:
        head = head.replace('<meta name="robots" content="index, follow">',
                            '<meta name="robots" content="%s">' % robots)
    foot = FOOTER.replace("__YEAR__", str(datetime.date.today().year)).replace("__TODAY__", TODAY)

    prefix = "../" * filename.count("/")
    head, foot, body = (retarget(x, prefix) for x in (head, foot, body))

    html = (
        "<!DOCTYPE html>\n"
        '<html lang="id"' + html_attr + ">\n"
        "<head>\n"
        + head
        + ('  <title data-i18n="' + lang_title_key + '">' if lang_title_key else "  <title>")
        + og_title + "</title>\n"
        + '  <meta name="description" content="' + desc + '">\n'
        + retarget(extra_head.replace("__SITE__", SITE_URL), prefix)
        + "</head>\n"
        "<body>\n"
        + retarget(header(active), prefix)
        + "\n"
        + '  <main id="main">\n'
        + body
        + "  </main>\n\n"
        + foot
        + "</body>\n</html>\n"
    )
    html = fill_fallbacks(html, _DICT_ID)

    path = os.path.join(ROOT, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path, len(html)


if __name__ == "__main__":
    _DICT_ID = _dictionary_id()

    from page_bodies import INDEX_BODY, PUBLICATIONS_BODY, THESES_BODY, TEACHING_BODY

    theses = _theses()

    pages = [
        page("index.html", "meta.title.home",
             "ENLab | Laboratorium Material Energi dan Semikonduktor ITERA",
             "Kelompok riset material energi dan semikonduktor: sel surya perovskit, DSSC, superkapasitor, "
             "fotodetektor, dan fotokatalisis di Program Studi Teknik Material, Institut Teknologi Sumatera.",
             INDEX_BODY.replace(
                 "__LATEST__",
                 theses_fallback([x for x in theses
                                  if x["y"] == max(t["y"] for t in theses)], _DICT_ID)),
             active="home", extra_head=JSONLD),
        page("publications.html", "meta.title.pub",
             "Publikasi | ENLab ITERA",
             "Daftar lengkap 57 publikasi ilmiah Dr. Eka Nurfani dan tim ENLab ITERA pada jurnal "
             "internasional bereputasi, jurnal nasional, dan prosiding konferensi sejak 2015.",
             PUBLICATIONS_BODY, active="pub"),
        page("theses.html", "meta.title.theses",
             "Tugas Akhir Mahasiswa | ENLab ITERA",
             "Daftar judul tugas akhir mahasiswa bimbingan Dr. Eka Nurfani di ITERA sejak 2019, "
             "dikelompokkan per tahun kelulusan: sel surya perovskit, DSSC, superkapasitor, "
             "fotodetektor, dan fotokatalisis.",
             THESES_BODY.replace("__FALLBACK__", theses_fallback(theses, _DICT_ID)),
             active="theses"),
        page("teaching.html", "meta.title.teach",
             "Pengajaran & Materi Kuliah | ENLab ITERA",
             "Materi kuliah Dr. Eka Nurfani di ITERA yang dapat diunduh: Fisika Dasar (TPB), "
             "Fisika Dasar II, Material Elektronik Optik Magnetik, Karakterisasi Material, "
             "Semikonduktor, dan Material Nano.",
             TEACHING_BODY, active="teach"),
    ]
    # Satu halaman per mata kuliah, agar tiap kelas punya tautan sendiri.
    # Mata kuliah yang tidak lagi diampu ("aktif": false) dilewati, dan
    # halaman lamanya dihapus agar tidak tertinggal di situs.
    courses = [c for c in _courses() if c.get("aktif") is not False]
    aktif_slug = {c["slug"] for c in courses}
    for f in sorted(glob.glob(os.path.join(ROOT, "mk", "*.html"))):
        if os.path.basename(f)[:-5] not in aktif_slug:
            os.remove(f)
            print("  " + os.path.relpath(f, ROOT).ljust(38) + "dihapus".rjust(7))
    for c in courses:
        judul = c["t"]["id"]
        ringkas = c["d"]["id"]
        if len(ringkas) > 155:
            ringkas = ringkas[:152].rsplit(" ", 1)[0] + "..."
        pages.append(page(
            "mk/" + c["slug"] + ".html", "",
            _html.escape(judul, quote=True) + " | ENLab ITERA",
            _html.escape(ringkas, quote=True),
            course_body(c, _DICT_ID), active="teach",
            html_attr=' data-base="../"',
            robots=None if c.get("pub") else "noindex, follow"))

    n_url = write_sitemap(courses)

    for p, n in pages:
        print("  " + os.path.relpath(p, ROOT).ljust(38) + str(n).rjust(7) + " bita")
    print("  " + "sitemap.xml".ljust(38) + str(n_url).rjust(7) + " url")
