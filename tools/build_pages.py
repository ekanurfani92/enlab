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
  <meta name="theme-color" content="#0a4f96" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#050e1c" media="(prefers-color-scheme: dark)">
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


def page(filename, lang_title_key, og_title, desc, body, active="", extra_head=""):
    canon = SITE_URL + "/" + ("" if filename == "index.html" else filename)
    head = (HEAD
            .replace("__CANON__", canon)
            .replace("__OGTITLE__", og_title)
            .replace("__DESC__", desc)
            .replace("__SITE__", SITE_URL))
    foot = FOOTER.replace("__YEAR__", str(datetime.date.today().year)).replace("__TODAY__", TODAY)

    html = (
        "<!DOCTYPE html>\n"
        '<html lang="id">\n'
        "<head>\n"
        + head
        + '  <title data-i18n="' + lang_title_key + '">' + og_title + "</title>\n"
        + '  <meta name="description" content="' + desc + '">\n'
        + extra_head.replace("__SITE__", SITE_URL)
        + "</head>\n"
        "<body>\n"
        + header(active)
        + "\n"
        + '  <main id="main">\n'
        + body
        + "  </main>\n\n"
        + foot
        + "</body>\n</html>\n"
    )
    html = fill_fallbacks(html, _DICT_ID)

    path = os.path.join(ROOT, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path, len(html)


if __name__ == "__main__":
    _DICT_ID = _dictionary_id()

    from page_bodies import INDEX_BODY, PUBLICATIONS_BODY, TEACHING_BODY

    pages = [
        page("index.html", "meta.title.home",
             "ENLab | Laboratorium Material Energi dan Semikonduktor ITERA",
             "Kelompok riset material energi dan semikonduktor: sel surya perovskit, DSSC, superkapasitor, "
             "fotodetektor, dan fotokatalisis di Program Studi Teknik Material, Institut Teknologi Sumatera.",
             INDEX_BODY, active="home", extra_head=JSONLD),
        page("publications.html", "meta.title.pub",
             "Publikasi | ENLab ITERA",
             "Daftar lengkap 57 publikasi ilmiah Dr. Eka Nurfani dan tim ENLab ITERA pada jurnal "
             "internasional bereputasi, jurnal nasional, dan prosiding konferensi sejak 2015.",
             PUBLICATIONS_BODY, active="pub"),
        page("teaching.html", "meta.title.teach",
             "Pengajaran & Materi Kuliah | ENLab ITERA",
             "Materi kuliah Teknik Material ITERA yang dapat diunduh: Karakterisasi Material, "
             "Material Keramik, Material Sensor, Fenomena Transpor Material, dan Fisika Dasar II.",
             TEACHING_BODY, active="teach"),
    ]
    for p, n in pages:
        print("  " + os.path.basename(p).ljust(22) + str(n).rjust(7) + " bita")
