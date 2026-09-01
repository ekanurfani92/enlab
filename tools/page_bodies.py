# -*- coding: utf-8 -*-
"""Isi <main> untuk setiap halaman. Disisipkan oleh build_pages.py."""

INDEX_BODY = """
    <!-- ============ HERO ============ -->
    <section class="hero">
      <div class="container hero-grid">
        <div class="hero-copy reveal">
          <span class="eyebrow" data-i18n="hero.eyebrow">Material Energi - Semikonduktor - Divais</span>
          <h1>
            <span data-i18n="hero.h1a">Material </span><em data-i18n="hero.h1b">Energi</em><span data-i18n="hero.h1c"> dan Semikonduktor</span>
          </h1>
          <p class="hero-lead" data-i18n="hero.lead">
            Kami merancang, mensintesis, dan mengkarakterisasi lapisan tipis serta nanomaterial oksida logam
            untuk sel surya perovskit, DSSC, superkapasitor, fotodetektor swadaya, sensor, dan fotokatalisis.
          </p>
          <p class="hero-affil">
            <span class="chip chip-accent">ITERA</span>
            <span data-i18n="hero.affil">Program Studi Teknik Material, Institut Teknologi Sumatera</span>
          </p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#research" data-i18n="hero.cta1">Jelajahi riset kami</a>
            <a class="btn btn-ghost" href="#contact" data-i18n="hero.cta2">Bergabung dengan lab</a>
          </div>
          <div class="hero-stats">
            <div><strong>57</strong><span data-i18n="hero.stat1">Publikasi ilmiah</span></div>
            <div><strong>19</strong><span data-i18n="hero.stat2">Hibah penelitian</span></div>
            <div><strong>70+</strong><span data-i18n="hero.stat3">Mahasiswa bimbingan</span></div>
            <div><strong>3</strong><span data-i18n="hero.stat4">Paten terdaftar</span></div>
          </div>
        </div>

        <div class="hero-visual reveal d1">
          <div class="logo-plate">
            <img src="assets/img/logo-enlab.svg"
                 alt="Logo ENLab - ENergy Materials and Semiconductor Laboratory"
                 width="977" height="1032" fetchpriority="high">
          </div>
        </div>
      </div>
    </section>

    <!-- ============ TENTANG ============ -->
    <section class="section" id="about">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow" data-i18n="about.eyebrow">Tentang ENLab</span>
          <h2 data-i18n="about.h2">Merekayasa material untuk masa depan energi yang lebih bersih.</h2>
          <p data-i18n="about.p1">ENLab (ENergy Materials and Semiconductor Laboratory) adalah kelompok riset di Program Studi Teknik Material, Institut Teknologi Sumatera.</p>
        </div>
        <p class="section-head reveal d1" data-i18n="about.p2" style="margin-top:-24px">
          Riset kami menjembatani ilmu material, fisika semikonduktor, elektrokimia, dan rekayasa divais.
        </p>
        <div class="grid-3">
          <article class="card card-hover reveal">
            <span class="eyebrow">01</span>
            <h3 style="margin:14px 0 8px" data-i18n="about.m1t">Inovasi</h3>
            <p style="color:var(--muted);font-size:.94rem" data-i18n="about.m1d">Mengembangkan material fungsional dan arsitektur divais dengan peningkatan kinerja yang terukur.</p>
          </article>
          <article class="card card-hover reveal d1">
            <span class="eyebrow">02</span>
            <h3 style="margin:14px 0 8px" data-i18n="about.m2t">Kolaborasi</h3>
            <p style="color:var(--muted);font-size:.94rem" data-i18n="about.m2d">Menghubungkan mahasiswa, peneliti, industri, dan mitra institusi melalui riset yang berdampak.</p>
          </article>
          <article class="card card-hover reveal d2">
            <span class="eyebrow">03</span>
            <h3 style="margin:14px 0 8px" data-i18n="about.m3t">Pendidikan</h3>
            <p style="color:var(--muted);font-size:.94rem" data-i18n="about.m3d">Membangun keterampilan eksperimen, analisis, dan komunikasi ilmiah bagi peneliti muda.</p>
          </article>
        </div>
      </div>
    </section>

    <!-- ============ RISET ============ -->
    <section class="section section-sunk" id="research">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow" data-i18n="res.eyebrow">Bidang Riset</span>
          <h2 data-i18n="res.h2">Dari sintesis material hingga divais fungsional.</h2>
          <p data-i18n="res.lead">Enam tema riset utama yang dikerjakan bersama mahasiswa tugas akhir dan mitra kolaborasi.</p>
        </div>
        <div class="grid-3">
          <article class="card card-hover research-card reveal">
            <div class="ico" aria-hidden="true">&#9728;</div>
            <h3 data-i18n="res.1t">Sel Surya Perovskit</h3>
            <p data-i18n="res.1d">Fabrikasi MAPbI3 pada kondisi udara terbuka dan rekayasa antarmuka TiO2.</p>
            <span class="chip" data-i18n="res.1k">Fotovoltaik</span>
          </article>
          <article class="card card-hover research-card reveal d1">
            <div class="ico" aria-hidden="true">&#9673;</div>
            <h3 data-i18n="res.2t">Sel Surya Tersensitisasi Pewarna</h3>
            <p data-i18n="res.2d">Pewarna alami, fotoanoda semikonduktor, dan elektrolit.</p>
            <span class="chip" data-i18n="res.2k">Energi Surya</span>
          </article>
          <article class="card card-hover research-card reveal d2">
            <div class="ico" aria-hidden="true">&#9889;</div>
            <h3 data-i18n="res.3t">Superkapasitor</h3>
            <p data-i18n="res.3d">Nanorod MnO2, komposit NiO-MnO2, dan penyimpanan energi elektrokimia.</p>
            <span class="chip" data-i18n="res.3k">Penyimpanan Energi</span>
          </article>
          <article class="card card-hover research-card reveal">
            <div class="ico" aria-hidden="true">&#9707;</div>
            <h3 data-i18n="res.4t">Lapisan Tipis &amp; Semikonduktor</h3>
            <p data-i18n="res.4d">ZnO, TiO2, NiO, ITO, dan oksida terdoping melalui spray pyrolysis dan hidrotermal.</p>
            <span class="chip" data-i18n="res.4k">Material Fungsional</span>
          </article>
          <article class="card card-hover research-card reveal d1">
            <div class="ico" aria-hidden="true">&#10022;</div>
            <h3 data-i18n="res.5t">Fotodetektor &amp; Sensor</h3>
            <p data-i18n="res.5d">Fotodetektor swadaya ZnO/p-Si, deteksi UV, dan sensor gas.</p>
            <span class="chip" data-i18n="res.5k">Divais Cerdas</span>
          </article>
          <article class="card card-hover research-card reveal d2">
            <div class="ico" aria-hidden="true">&#9678;</div>
            <h3 data-i18n="res.6t">Fotokatalisis</h3>
            <p data-i18n="res.6d">Heterojunction CeO2/ZnO untuk degradasi polutan organik.</p>
            <span class="chip" data-i18n="res.6k">Material Berkelanjutan</span>
          </article>
        </div>
      </div>
    </section>

    <!-- ============ TIM ============ -->
    <section class="section" id="team">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow" data-i18n="team.eyebrow">Tim Kami</span>
          <h2 data-i18n="team.h2">Riset tumbuh melalui kolaborasi.</h2>
          <p data-i18n="team.lead">Dipimpin oleh Dr. Eka Nurfani bersama mahasiswa sarjana Teknik Material ITERA.</p>
        </div>
        <article class="lead-person reveal">
          <div class="lead-person-photo">
            <img src="assets/img/eka-nurfani.jpg" alt="Dr. Eka Nurfani, S.Si., M.Si." loading="lazy" width="400" height="440">
          </div>
          <div class="lead-person-body">
            <h3>Dr. Eka Nurfani, S.Si., M.Si.</h3>
            <p class="person-role" data-i18n="team.pi.role">Kepala Laboratorium - Lektor Kepala</p>
            <p class="lead-person-field" data-i18n="team.pi.field">Fisika Material - Lapisan Tipis Oksida - Divais Energi</p>
            <p class="lead-person-bio" data-i18n="team.pi.bio">Menyelesaikan S-1 Fisika di Universitas Jenderal Soedirman, lalu S-2 dan S-3 Fisika Material di Institut Teknologi Bandung melalui program PMDSU.</p>
            <div class="person-links">
              <a href="https://scholar.google.com/citations?user=5Sz8OyAAAAAJ" target="_blank" rel="noopener">Scholar</a>
              <a href="https://www.scopus.com/authid/detail.uri?authorId=57190941043" target="_blank" rel="noopener">Scopus</a>
              <a href="https://sinta.kemdikbud.go.id/authors/profile/6659724" target="_blank" rel="noopener">SINTA</a>
            </div>
          </div>
        </article>

        <div class="grid-3" style="margin-top:16px">
          <article class="card card-hover team-group reveal">
            <div class="ico" aria-hidden="true">&#9998;</div>
            <h3 data-i18n="team.slot2t">Mahasiswa Tugas Akhir</h3>
            <p class="person-role" data-i18n="team.slot2r">Sarjana Teknik Material</p>
            <p data-i18n="team.slot2d">Menjalankan riset sel surya perovskit, DSSC, superkapasitor, TCO, dan MXene.</p>
          </article>
          <article class="card card-hover team-group reveal d1">
            <div class="ico" aria-hidden="true">&#8646;</div>
            <h3 data-i18n="team.slot3t">Kolaborator</h3>
            <p class="person-role" data-i18n="team.slot3r">ITERA - ITB - BRIN - Mitra Internasional</p>
            <p data-i18n="team.slot3d">Kolaborasi lintas institusi pada skema RIIM LPDP-BRIN dan Penelitian Fundamental.</p>
          </article>
          <article class="card card-hover team-group reveal d2">
            <div class="ico" aria-hidden="true">&#9733;</div>
            <h3 data-i18n="team.slot4t">Alumni</h3>
            <p class="person-role" data-i18n="team.slot4r">Lulusan sejak 2019</p>
            <p data-i18n="team.slot4d">Lebih dari 70 mahasiswa telah menyelesaikan tugas akhir di laboratorium ini.</p>
          </article>
        </div>
        <p style="margin-top:26px">
          <a class="text-link" href="#contact" data-i18n="team.join">Tertarik bergabung? Lihat cara mendaftar</a>
        </p>
      </div>
    </section>

    <!-- ============ FASILITAS ============ -->
    <section class="section section-sunk" id="facilities">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow" data-i18n="fac.eyebrow">Fasilitas</span>
          <h2 data-i18n="fac.h2">Peralatan fabrikasi, sintesis, dan pengujian.</h2>
          <p data-i18n="fac.lead">Laboratorium mengoperasikan peralatan komersial sekaligus instrumen rakitan sendiri.</p>
        </div>
        <div class="grid-2" style="align-items:start">
          <div style="display:grid;gap:12px">
            <article class="facility reveal"><b>01</b><div><h3 data-i18n="fac.1t">Fabrikasi Lapisan Tipis</h3><p data-i18n="fac.1d">Spin coater Ossila, spray pyrolysis berbasis nebulizer, hot plate, dan tungku.</p></div></article>
            <article class="facility reveal d1"><b>02</b><div><h3 data-i18n="fac.2t">Sintesis Material</h3><p data-i18n="fac.2d">Autoclave hidrotermal 100 mL, preparasi prekursor, sonikasi, dan perlakuan panas.</p></div></article>
            <article class="facility reveal d2"><b>03</b><div><h3 data-i18n="fac.3t">Pengujian Divais</h3><p data-i18n="fac.3d">Stasiun J-V dengan simulator surya LED rakitan sendiri dan sel elektrokimia kustom.</p></div></article>
          </div>
          <div style="display:grid;gap:12px">
            <article class="facility reveal d1"><b>04</b><div><h3 data-i18n="fac.4t">Karakterisasi Material</h3><p data-i18n="fac.4d">Akses ke XRD, SEM, UV-Vis DRS, dan voltametri siklik.</p></div></article>
            <article class="facility reveal d2"><b>05</b><div><h3 data-i18n="fac.5t">Instrumen Rakitan Sendiri</h3><p data-i18n="fac.5d">Spin coater, stasiun simulator J-V berbasis LED, dan stasiun light soaking dirancang di laboratorium.</p></div></article>
            <div class="card reveal d3" style="background:var(--surface-3);border-color:transparent">
              <span class="eyebrow">ITERA</span>
              <p style="margin-top:12px;color:var(--muted);font-size:.93rem" data-i18n="fac.cta">Ajukan informasi penggunaan fasilitas</p>
              <p style="margin-top:14px"><a class="text-link" href="#contact" data-i18n="contact.email">Surel</a></p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ PUBLIKASI (cuplikan) ============ -->
    <section class="section" id="publications">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow" data-i18n="pub.eyebrow">Publikasi</span>
          <h2 data-i18n="pub.h2">Luaran riset terpilih.</h2>
          <p data-i18n="pub.lead">57 artikel pada jurnal internasional bereputasi, jurnal nasional, dan prosiding konferensi sejak 2015.</p>
        </div>
        <ul class="pub-list reveal" id="pub-latest"></ul>
        <p style="margin-top:24px">
          <a class="btn btn-ghost" href="publications.html" data-i18n="pub.all">Lihat seluruh publikasi</a>
        </p>
      </div>
    </section>

    <!-- ============ PENDANAAN ============ -->
    <section class="section" id="funding">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow" data-i18n="grant.eyebrow">Pendanaan</span>
          <h2 data-i18n="grant.h2">Hibah penelitian terkini.</h2>
          <p data-i18n="grant.lead">Riset laboratorium didukung pendanaan nasional dan internal institusi.</p>
        </div>
        <ul class="pub-list reveal" id="grant-list"></ul>
        <p class="pub-count" style="margin-top:18px" data-i18n="grant.all">Riwayat lengkap tersedia pada CV</p>
      </div>
    </section>

    <!-- ============ PENGAJARAN (cuplikan) ============ -->
    <section class="section section-sunk" id="teaching">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow" data-i18n="teach.eyebrow">Pengajaran</span>
          <h2 data-i18n="teach.h2">Materi kuliah terbuka untuk mahasiswa.</h2>
          <p data-i18n="teach.lead">Slide kuliah yang disusun sendiri oleh dosen pengampu dapat diunduh bebas.</p>
        </div>
        <div class="grid-3">
          <article class="card card-hover reveal">
            <span class="chip chip-neutral">3 sks</span>
            <h3 style="margin:14px 0 8px">Karakterisasi Material</h3>
            <p style="color:var(--muted);font-size:.93rem">SEM, TEM, XRD, XRF, UV-Vis, PL, dan voltametri siklik.</p>
          </article>
          <article class="card card-hover reveal d1">
            <span class="chip chip-neutral">4 sks</span>
            <h3 style="margin:14px 0 8px">Fisika Dasar II</h3>
            <p style="color:var(--muted);font-size:.93rem">Elektrostatika, magnetostatika, gelombang EM, dan fisika modern.</p>
          </article>
          <article class="card card-hover reveal d2">
            <span class="chip chip-neutral">3 sks</span>
            <h3 style="margin:14px 0 8px">Material Elektronik, Optik dan Magnetik</h3>
            <p style="color:var(--muted);font-size:.93rem">Hantaran listrik, struktur pita energi, sifat optik, dan aplikasi divais.</p>
          </article>
        </div>
        <p style="margin-top:24px">
          <a class="btn btn-primary" href="teaching.html" data-i18n="teach.all">Buka halaman materi kuliah</a>
        </p>
      </div>
    </section>

    <!-- ============ ALUR KERJA ============ -->
    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow" data-i18n="gal.eyebrow">Alur Kerja</span>
          <h2 data-i18n="gal.h2">Dari prekursor ke divais.</h2>
        </div>
        <ol class="flow reveal">
          <li class="flow-step">
            <span class="flow-num">01</span>
            <b data-i18n="gal.1">Sintesis Material</b>
            <span data-i18n="gal.1s">Hidrotermal &amp; sol-gel</span>
          </li>
          <li class="flow-step">
            <span class="flow-num">02</span>
            <b data-i18n="gal.2">Fabrikasi Lapisan Tipis</b>
            <span data-i18n="gal.2s">Spin coating &amp; spray pyrolysis</span>
          </li>
          <li class="flow-step">
            <span class="flow-num">03</span>
            <b data-i18n="gal.4">Karakterisasi</b>
            <span data-i18n="gal.4s">XRD, SEM, UV-Vis</span>
          </li>
          <li class="flow-step">
            <span class="flow-num">04</span>
            <b data-i18n="gal.3">Pengujian Divais</b>
            <span data-i18n="gal.3s">Pengukuran J-V &amp; light soaking</span>
          </li>
        </ol>
        <div class="flow-aside reveal d1">
          <div>
            <b data-i18n="gal.5">Riset Mahasiswa</b>
            <span data-i18n="gal.5s">Tugas akhir sarjana</span>
          </div>
          <div>
            <b data-i18n="gal.6">Diskusi Ilmiah</b>
            <span data-i18n="gal.6s">Seminar &amp; bimbingan</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ KONTAK ============ -->
    <section class="section section-sunk" id="contact">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow" data-i18n="contact.eyebrow">Kontak</span>
          <h2 data-i18n="contact.h2">Kunjungi laboratorium kami.</h2>
        </div>
        <div class="contact-grid">
          <ul class="contact-list reveal">
            <li>
              <i aria-hidden="true">&#9873;</i>
              <div>
                <b data-i18n="contact.addr">Alamat</b>
                <span data-i18n="contact.addrv">Gedung D Ruang D208, Program Studi Teknik Material, Institut Teknologi Sumatera, Jalan Terusan Ryacudu, Way Huwi, Jati Agung, Lampung Selatan 35365</span>
              </div>
            </li>
            <li>
              <i aria-hidden="true">&#9993;</i>
              <div>
                <b data-i18n="contact.email">Surel</b>
                <a href="mailto:eka.nurfani@mt.itera.ac.id">eka.nurfani@mt.itera.ac.id</a>
              </div>
            </li>
            <li>
              <i aria-hidden="true">&#9679;</i>
              <div>
                <b data-i18n="contact.profile">Profil peneliti</b>
                <span>
                  <a href="https://scholar.google.com/citations?user=5Sz8OyAAAAAJ" target="_blank" rel="noopener">Google Scholar</a> &middot;
                  <a href="https://www.scopus.com/authid/detail.uri?authorId=57190941043" target="_blank" rel="noopener">Scopus</a> &middot;
                  <a href="https://sinta.kemdikbud.go.id/authors/profile/6659724" target="_blank" rel="noopener">SINTA</a>
                </span>
              </div>
            </li>
          </ul>
          <div class="map-embed reveal d1">
            <iframe
              src="https://www.google.com/maps?q=Institut+Teknologi+Sumatera&amp;z=15&amp;output=embed"
              title="Peta lokasi Institut Teknologi Sumatera"
              loading="lazy" referrerpolicy="no-referrer-when-downgrade"
              allowfullscreen></iframe>
          </div>
        </div>

        <div class="cta reveal" style="margin-top:40px">
          <div>
            <span class="eyebrow" data-i18n="cta.eyebrow">Mari Berkolaborasi</span>
            <h2 data-i18n="cta.h2">Tertarik meneliti, berkolaborasi, atau bergabung dengan ENLab?</h2>
            <p data-i18n="cta.p">Kami menerima mahasiswa tugas akhir, peneliti, mitra akademik, dan kolaborator industri.</p>
          </div>
          <div class="cta-actions">
            <a class="btn btn-light" href="mailto:eka.nurfani@mt.itera.ac.id" data-i18n="cta.mail">Kirim email</a>
            <a class="btn btn-outline-light" href="#main" data-i18n="cta.top">Kembali ke atas</a>
          </div>
        </div>
      </div>
    </section>
"""

PUBLICATIONS_BODY = """
    <section class="page-head">
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <a href="index.html" data-i18n="nav.home">Beranda</a>
          <span aria-hidden="true">/</span>
          <span data-i18n="nav.publications">Publikasi</span>
        </nav>
        <h1 data-i18n="pub.page.h1">Publikasi</h1>
        <p data-i18n="pub.page.lead">Daftar lengkap artikel ilmiah Dr. Eka Nurfani dan tim ENLab.</p>
        <p class="pub-count" style="margin-top:22px;margin-bottom:8px" data-i18n="pub.profiles">Profil peneliti</p>
        <p style="display:flex;gap:10px;flex-wrap:wrap">
          <a class="btn btn-ghost btn-sm" href="https://scholar.google.com/citations?user=5Sz8OyAAAAAJ" target="_blank" rel="noopener">Google Scholar</a>
          <a class="btn btn-ghost btn-sm" href="https://www.scopus.com/authid/detail.uri?authorId=57190941043" target="_blank" rel="noopener">Scopus</a>
          <a class="btn btn-ghost btn-sm" href="https://sinta.kemdikbud.go.id/authors/profile/6659724" target="_blank" rel="noopener">SINTA</a>
        </p>
      </div>
    </section>

    <section class="section" style="padding-top:clamp(30px,4vw,48px)">
      <div class="container">
        <div class="filters">
          <label class="sr-only" for="pub-search" data-i18n="pub.search">Cari judul atau nama jurnal</label>
          <input type="search" id="pub-search" data-i18n="pub.search" data-i18n-attr="placeholder"
                 placeholder="Cari judul atau nama jurnal...">
          <label class="sr-only" for="pub-year" data-i18n="pub.year.all">Semua tahun</label>
          <select id="pub-year"></select>
          <div class="filter-pills">
            <button type="button" data-kind="all" aria-pressed="true" data-i18n="pub.filter.all">Semua</button>
            <button type="button" data-kind="journal" aria-pressed="false" data-i18n="pub.filter.journal">Jurnal internasional</button>
            <button type="button" data-kind="conference" aria-pressed="false" data-i18n="pub.filter.conference">Prosiding konferensi</button>
            <button type="button" data-kind="national" aria-pressed="false" data-i18n="pub.filter.national">Jurnal nasional</button>
          </div>
        </div>

        <p class="pub-count" id="pub-count"></p>
        <ul class="pub-list" id="pub-list"></ul>
      </div>
    </section>
"""

TEACHING_BODY = """
    <section class="page-head">
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <a href="index.html" data-i18n="nav.home">Beranda</a>
          <span aria-hidden="true">/</span>
          <span data-i18n="nav.teaching">Pengajaran</span>
        </nav>
        <h1 data-i18n="teach.page.h1">Pengajaran &amp; Materi Kuliah</h1>
        <p data-i18n="teach.page.lead">Mata kuliah yang diampu Dr. Eka Nurfani di Institut Teknologi Sumatera.</p>
        <p class="pub-count" id="course-count" style="margin-top:16px"></p>
      </div>
    </section>

    <section class="section" style="padding-top:clamp(30px,4vw,48px)">
      <div class="container">
        <div class="card" style="background:var(--surface-3);border-color:transparent;margin-bottom:32px">
          <strong style="font-family:var(--font-head)" data-i18n="teach.notice.t">Catatan hak cipta</strong>
          <p style="color:var(--muted);font-size:.92rem;margin-top:8px" data-i18n="teach.notice.d">
            Materi di halaman ini adalah slide yang disusun sendiri oleh dosen pengampu.
          </p>
        </div>

        <h2 style="font-size:1.35rem;margin-bottom:18px" data-i18n="teach.group.mt">Program Studi Teknik Material</h2>
        <div id="courses-mt" style="display:grid;gap:12px;margin-bottom:48px"></div>

        <h2 style="font-size:1.35rem;margin-bottom:18px" data-i18n="teach.group.other">Tahap Persiapan Bersama &amp; Program Studi Lain</h2>
        <div id="courses-other" style="display:grid;gap:12px"></div>
      </div>
    </section>
"""
