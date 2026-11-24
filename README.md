# Situs ENLab

Situs statis **ENLab** - *ENergy Materials and Semiconductor Laboratory*,
Program Studi Teknik Material, Institut Teknologi Sumatera.

**EN** diambil dari inisial pendiri laboratorium sekaligus disandikan pada kata
**EN**ergy dalam nama resminya. Kapitalisasi "ENergy" karena itu disengaja — jangan
diperbaiki menjadi "Energy". Pada subjudul logo, bagian "EN" diberi warna aksen
melalui `data-i18n-html` agar permainan kata itu terbaca.

Dibangun dengan HTML, CSS, dan JavaScript murni — tanpa framework, tanpa proses
build wajib, tanpa basis data. Cukup unggah seluruh isi folder ke layanan hosting
statis mana pun.

---

> **Baru pertama kali merawat situs?** Baca [PANDUAN.md](PANDUAN.md) — panduan
> langkah demi langkah untuk memperbarui situs sendiri, termasuk cara mengunggah
> materi kuliah, menambah publikasi, dan mengatasi masalah yang umum terjadi.

## 1. Melihat situs di komputer sendiri

Membuka `index.html` dengan klik ganda **tidak disarankan** karena berkas PDF dan
beberapa tautan relatif berperilaku berbeda pada protokol `file://`. Jalankan
peladen lokal:

```bash
cd "WEBSITE LAB"
python3 -m http.server 8000
```

Lalu buka <http://localhost:8000>. Hentikan dengan `Ctrl+C`.

---

## 2. Struktur berkas

```
WEBSITE LAB/
├── index.html              Beranda (hero, tentang, riset, tim, fasilitas,
│                           publikasi terbaru, pendanaan, tugas akhir,
│                           pengajaran, galeri, kontak)
├── publications.html       Daftar 57 publikasi + pencarian & filter
├── theses.html             63 judul tugas akhir, dikelompokkan per tahun
├── teaching.html           17 mata kuliah + 25 berkas materi yang dapat diunduh
├── 404.html                Halaman kesalahan
│
├── assets/
│   ├── css/style.css       Seluruh gaya (mode terang & gelap)
│   ├── js/
│   │   ├── i18n.js         Kamus dwibahasa ID/EN  <- ubah teks statis di sini
│   │   ├── data-publications.js   Daftar publikasi
│   │   ├── data-courses.js        Daftar mata kuliah + materi
│   │   ├── data-grants.js         Daftar hibah penelitian
│   │   ├── data-theses.js         Daftar tugas akhir mahasiswa
│   │   └── main.js         Logika: bahasa, tema, navigasi, perender data
│   └── img/                logo, favicon, foto, gambar Open Graph
│
├── logo/                   Berkas logo asli (sumber, jangan dihapus)
│
├── materi/                 Berkas PDF materi kuliah, dikelompokkan per mata kuliah
│
├── dokumen-ta/             Dokumen bimbingan tugas akhir (daftar judul, formulir)
│
├── tools/
│   ├── build_pages.py      Membangun ulang HTML dari potongan bersama
│   ├── page_bodies.py      Isi <main> tiap halaman
│   └── verify.py           Pemeriksa kesehatan situs
│
├── robots.txt, sitemap.xml, site.webmanifest, .nojekyll
└── README.md
```

---

## 3. Memperbarui konten

Setelah setiap perubahan, jalankan pemeriksa:

```bash
python3 tools/verify.py
```

### 3.1 Menambah publikasi baru

Buka `assets/js/data-publications.js`, sisipkan satu objek **di paling atas** daftar:

```js
{ "y": 2026,
  "t": "Judul lengkap artikel",
  "v": "Nama Jurnal",
  "d": "Vol. 12, No. 103421",
  "k": "journal" },
```

Nilai `k`: `journal` (jurnal internasional), `conference` (prosiding),
`national` (jurnal nasional). Filter tahun pada halaman publikasi terisi otomatis.

Angka **57** pada beranda ditulis manual di dua tempat — perbarui bila jumlah berubah:
`tools/page_bodies.py` (statistik hero) dan `assets/js/i18n.js` (kunci `pub.lead`).

### 3.2 Menambah materi kuliah

1. Letakkan berkas PDF di `materi/<slug-mata-kuliah>/nama-berkas.pdf`
   (huruf kecil, tanpa spasi).
2. Tambahkan entri pada array `"m"` mata kuliah terkait di `assets/js/data-courses.js`:

```js
{ "t": "Judul Materi", "f": "materi/karakterisasi-material/8-ftir.pdf", "s": 2.4 }
```

`s` adalah ukuran berkas dalam MB (ditampilkan agar mahasiswa tahu besar unduhan).

Untuk memperkecil PDF yang besar:

```bash
gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=keluaran.pdf masukan.pdf
```

### 3.3 Mengubah teks yang tampil di halaman

Semua teks statis ada di `assets/js/i18n.js`. Setiap kunci **wajib ada pada kedua
bahasa** (`id` dan `en`) — `tools/verify.py` akan menolak bila salah satu hilang.

### 3.4 Logo dan warna

Logo asli tersimpan di `logo/logo-ENLab.png`, dengan versi vektornya di
`logo/logo-ENLab.svg` (lengkap sampai garis hijau, tanpa tagline; tersedia juga
sebagai `.pdf` dan PNG 3000 px untuk slide dan cetak). Berkas turunan yang
dipakai situs:

| Berkas | Dipakai untuk |
|---|---|
| `assets/img/logo-emblem.png` | Lambang di header dan footer (latar transparan) |
| `assets/img/logo-enlab.svg` | Logo penuh (vektor) pada hero |
| `assets/img/favicon.png` | Ikon tab peramban |

Palet situs diambil langsung dari logo: navy `#042c68`, biru `#0a4f96`,
hijau `#248430`, dan jingga `#f7a909`. Nilainya ada di bagian *Tokens* pada
`assets/css/style.css`. Bila logo diganti, sesuaikan warna di sana.

> **Catatan mode gelap.** Garis putih pada panel surya dan bagian dalam molekul
> adalah bagian dari desain logo, bukan latar. Karena itu logo tidak bisa
> ditempel langsung di atas latar gelap — CSS memberinya alas putih pada mode
> gelap (`.brand-logo` dan `.logo-plate`). Jangan hapus aturan itu.

### 3.5 Mengganti kotak galeri dengan foto

Pada `tools/page_bodies.py`, bagian galeri, ganti kelas warna dengan gambar:

```html
<div class="tile" style="background-image:url('assets/img/lab-1.jpg')">
```

Ukuran anjuran 1200x800 piksel, format JPG, di bawah 300 KB. Lalu jalankan
`python3 tools/build_pages.py`.

### 3.6 Mengubah navigasi atau footer

Sunting `tools/build_pages.py` lalu jalankan:

```bash
python3 tools/build_pages.py
```

Berkas HTML akan ditulis ulang. Bila lebih nyaman menyunting HTML langsung,
silakan — hasilnya tetap HTML statis biasa — tetapi ingat perubahan itu akan
tertimpa bila skrip dijalankan lagi.

---

### 3.7 Menambah tugas akhir mahasiswa

Buka `assets/js/data-theses.js`, sisipkan satu objek **di paling atas** daftar:

```js
  { "y": 2027, "n": "Nama Lengkap Mahasiswa",
    "t": { "id": "Judul tugas akhir dalam Bahasa Indonesia",
           "en": "Thesis title in English" } },
```

Keterangan: `y` tahun kelulusan, `n` nama mahasiswa, `t` judul dalam dua bahasa.
Hanya ketiga hal itu yang tampil di situs.

Pengelompokan per tahun, pilihan tahun pada filter, dan angka pada beranda
terisi otomatis. NIM sengaja tidak dicantumkan. Setelah menyunting, jalankan
`python3 tools/build_pages.py` agar teks cadangan pada `theses.html` dan
beranda ikut diperbarui.

---

## 4. Menerbitkan ke internet (gratis)

### Pilihan A — GitHub Pages (disarankan)

Permanen, gratis, mendukung domain sendiri, dan menyimpan riwayat perubahan.

1. Buat akun di <https://github.com>.
2. Buat repositori baru bernama `en-lab` (atau nama lain), setel **Public**.
3. Unggah berkas. Cara termudah tanpa perintah: pada halaman repositori pilih
   **Add file - Upload files**, seret seluruh isi folder `WEBSITE LAB`
   (bukan foldernya, melainkan isinya), lalu **Commit changes**.

   Melalui terminal:

   ```bash
   cd "WEBSITE LAB"
   git init
   git add .
   git commit -m "Situs ENLab"
   git branch -M main
   git remote add origin https://github.com/<nama-akun>/en-lab.git
   git push -u origin main
   ```

4. Buka **Settings - Pages**. Pada *Source* pilih **Deploy from a branch**,
   branch `main`, folder `/ (root)`, lalu **Save**.
5. Tunggu satu hingga dua menit. Situs terbit di
   `https://<nama-akun>.github.io/en-lab/`.

> **Penting setelah alamat final diketahui.** Ganti alamat contoh
> `https://en-lab.github.io` menjadi alamat sebenarnya pada tiga berkas:
> `tools/build_pages.py` (variabel `SITE_URL`), `robots.txt`, dan `sitemap.xml`.
> Lalu jalankan `python3 tools/build_pages.py`. Tanpa langkah ini, tautan
> kanonik dan pratinjau Open Graph akan menunjuk alamat yang keliru.

Batas GitHub Pages: 1 GB per repositori, 100 MB per berkas, 100 GB lalu lintas
per bulan. Folder `materi/` saat ini sekitar 33 MB — masih sangat lapang.

### Mengapa bukan Google Sites

Google Sites gratis dan mudah, tetapi **tidak dapat menampung situs ini**. Google
Sites hanya menerima blok siap pakai dari editornya; HTML, CSS, dan JavaScript
sendiri hanya bisa disisipkan melalui gawai *Embed* di dalam bingkai kecil.
Bila berpindah ke sana, yang hilang adalah: tombol dwibahasa, mode gelap,
pencarian dan filter publikasi, desain khusus, serta kendali SEO (meta Open Graph,
JSON-LD, sitemap). Situs juga tidak bisa dipindahkan ke layanan lain di kemudian hari.

Google Sites cocok bila situs dibuat dari nol oleh orang yang tidak ingin menyentuh
berkas sama sekali. Untuk situs yang sudah jadi seperti ini, GitHub Pages lebih tepat.

### Pilihan B — Netlify Drop (paling cepat)

Buka <https://app.netlify.com/drop>, seret folder `WEBSITE LAB` ke halaman itu.
Situs langsung terbit. Untuk memperbarui, seret ulang folder tersebut.

### Pilihan C — Cloudflare Pages

Lalu lintas tak terbatas dan tercepat diakses dari Indonesia.
Buka <https://pages.cloudflare.com>, hubungkan ke repositori GitHub,
kosongkan *build command*, dan setel *output directory* ke `/`.

### Domain sendiri

Bila ITERA menyediakan subdomain (misalnya `en-lab.itera.ac.id`), minta pengelola
TIK membuat rekaman `CNAME` yang menunjuk ke `<nama-akun>.github.io`.
Lalu isi kolom *Custom domain* pada **Settings - Pages**.

---

## 5. Yang masih perlu dilengkapi

- [ ] **Foto kegiatan laboratorium** untuk menggantikan enam kotak galeri berwarna.
- [ ] **Anggota tim** — tiga kartu (mahasiswa, kolaborator, alumni) masih berupa
      keterangan umum. Nama mahasiswa yang sedang berjalan belum dicantumkan;
      tambahkan hanya atas persetujuan yang bersangkutan.
- [ ] **Nomor telepon** sengaja tidak dipublikasikan. Bila ingin ditampilkan,
      gunakan nomor kantor prodi, bukan nomor pribadi.
- [ ] **Tautan DOI** — judul publikasi kini mengarah ke pencarian Google Scholar.
      Bila DOI tersedia, tambahkan kolom `"doi"` pada data dan gunakan sebagai
      tautan langsung.
- [ ] **Alamat situs final** pada `SITE_URL`, `robots.txt`, dan `sitemap.xml`.
- [ ] **Logo versi vektor (SVG)** bila tersedia, agar tajam di layar beresolusi tinggi.

---

## 6. Catatan hak cipta dan privasi

Berkas dalam `materi/` hanya berisi slide yang disusun sendiri oleh dosen
pengampu (bertanda `[EN]`, `[EKA]`, atau `[eka]` pada arsip asli). Buku teks dan
materi pihak ketiga **tidak** disertakan karena tidak boleh disebarluaskan;
mahasiswa dapat mengaksesnya melalui perpustakaan ITERA.

**Pengecualian — tiga foto berlisensi bebas.** Deck Semikonduktor Minggu 1
(`materi/semikonduktor/01-sejarah-dan-perkembangan-material-semikonduktor.pdf`)
memuat tiga foto pihak ketiga yang lisensinya mengizinkan penyebarluasan publik.
Atribusinya tercetak pada slide masing-masing, dan diulang di sini sebagaimana
disyaratkan lisensinya:

| Slide | Foto | Lisensi | Atribusi |
|---|---|---|---|
| 7 | Tabung osilasi Fleming, 1904 | Domain publik | J. A. Fleming, *The Thermionic Valve*, The Wireless Press, London, 1919. Wikimedia Commons, `File:Fleming_valves.jpg` |
| 8 | ENIAC | Domain publik (karya pegawai Pemerintah Federal AS) | U.S. Army, Ballistic Research Laboratory. Wikimedia Commons, `File:Eniac.jpg` |
| 13 | Intel 4004 | **CC BY-SA 4.0** | Foto Thomas Nguyen, 2016. Wikimedia Commons, `File:Intel_C4004.jpg` |

Selebihnya gambar pada deck itu dibuat sendiri dengan TikZ/pgfplots. Gambar dari
Museum TEL dan dari buku Dimitrijev (Oxford University Press) sengaja dikeluarkan
dan diganti, sebab izinnya tidak mencakup penerbitan publik. Rinciannya ada pada
`KULIAH/Semikonduktor/2026-2027 Gasal/slides/SUMBER-GAMBAR.md`.

**Foto berlisensi bebas lainnya.** Deck Semikonduktor Minggu 5 dan 6 serta
Material Elektronik, Optik dan Magnetik Minggu 5 memuat foto dari Wikimedia
Commons. Atribusinya tercetak di bawah tiap foto; yang berlisensi BY/BY-SA
diulang di sini sebagaimana disyaratkan lisensinya:

| Deck | Foto | Lisensi | Atribusi (Wikimedia Commons) |
|---|---|---|---|
| Semikonduktor Mg 5 | Wafer GaAs 2" | CC BY-SA 3.0 | La2O3, 2014, `File:Gallium Arsenide (GaAs) 2" wafer.jpg` |
| Semikonduktor Mg 5 | LED biru GaN | CC BY 3.0 | Hi-Res Images of Chemical Elements, 2011, `File:Blue LEDs in front of a white painted wall.jpg` |
| Semikonduktor Mg 6 | Batang polisilikon | CC BY-SA 3.0 | Warut Roonguthai, 2007, `File:Polycrystalline silicon rod.jpg` |
| Semikonduktor Mg 6 | Ingot Si Czochralski | CC BY-SA 4.0 | Massimiliano Lincetto, 2008, `File:Silicon single crystal.jpg` |
| Semikonduktor Mg 6 | Wafer berpola | CC BY 2.0 | .RGB. (Flickr), 2012, `File:IMaGe 30988 – Silicon Wafer.jpg` |
| Semikonduktor Mg 6 | Tungku difusi, implanter ion, stepper | CC BY-SA 3.0 | Guillaume Paumier, 2007 (LAAS-CNRS), `File:Centrotherm diffusion furnace at LAAS 0489.jpg`, `File:Ion implantation machine at LAAS 0522.jpg`, `File:EVG-620 & MA-150 steppers at LAAS (FDLS 2007) 0430.jpg` |

Foto lain pada deck tersebut berstatus domain publik atau CC0 (Semikonduktor:
TimVickers, Enricoros, G. E. Meyers 1956; MEOM Mg 5: Steffen Maisch, ArticCynda,
Smial, Georg Pik, Peter Hebels, Antonín Ryska, Petey21, Retired electrician,
Armstrong1113149, ISCIX-Ex, Ypsilon from Finland, Ravenperch, MatteX). Rinciannya
ada pada `SUMBER-GAMBAR.md` (Semikonduktor) dan `slides/gambar.csv` (MEOM).

**Foto pada deck Fisika Dasar TPB (sejak 17 Oktober 2026).** Pertemuan 1–15
memuat foto dari Wikimedia Commons; atribusinya tercetak di bawah tiap foto.
Yang berlisensi BY/BY-SA diulang di sini:

| Deck | Lisensi | Atribusi (Wikimedia Commons) |
|---|---|---|
| Fisika Dasar TPB P1 | CC BY-SA 3.0 | LPLT, `File:Mètre-étalon Paris.JPG` |
| Fisika Dasar TPB P1 | CC BY-SA 3.0 | ArtMechanic, `File:Messschieber.jpg` |
| Fisika Dasar TPB P2 | CC BY-SA 3.0 | MichaelMaggs, `File:Falling ball.jpg` |
| Fisika Dasar TPB P2, P7 | CC BY-SA 3.0 | MichaelMaggs, suntingan Richard Bartz, `File:Bouncing ball strobe edit.jpg` |
| Fisika Dasar TPB P3 | CC BY-SA 4.0 | Paul W, `File:Calshot velodrome.jpg` (dipotong) |
| Fisika Dasar TPB P4 | CC BY 2.0 | Sheila Sund, `File:Newton's Cradle (15221366308).jpg` |
| Fisika Dasar TPB P4 | CC BY 2.0 | Jeremy Thompson, `File:Loop Coaster MOMOnGA vertical loop - Yomiuriland.jpg` (dipotong) |
| Fisika Dasar TPB P5 | CC BY-SA 4.0 | Trude Bergheim Mikkelsen, `File:Slotted-headstock-classical-guitar.JPG` |
| Fisika Dasar TPB P5 | CC BY-SA 3.0 | Roger McLassus, `File:2006-01-14 Surface waves.jpg` |
| Fisika Dasar TPB P6 | CC BY-SA 2.0 | Rebecca Partington, `File:Melting - Flickr - Trinity.jpg` |
| Fisika Dasar TPB P6 | CC BY-SA 3.0 | Passivhaus Institut, `File:Passivhaus thermogram gedaemmt ungedaemmt.png` |
| Fisika Dasar TPB P6 | CC BY-SA 3.0 | Menchi, `File:Clinical thermometer 38.7.JPG` |
| Fisika Dasar TPB P7 | CC BY-SA 4.0 | GT1976, `File:2018-10-22 (835) Bridge expansion joint at Donaubrücke in Krems an der Donau, Austria.jpg` |
| Fisika Dasar TPB P9 | CC BY 2.0 | David Maciulaitis, `File:Boulton & Watt steam engine, Sydney Powerhouse Museum, 2014 (15240699214).jpg` |
| Fisika Dasar TPB P9 | CC BY-SA 2.0 | JThomas, `File:Cooling towers, Drax power station - geograph.org.uk - 2275301.jpg` |

Foto lainnya berstatus domain publik atau CC0 (NIST, NASA, NHTSA, U.S. Navy,
lukisan Kneller, Sustermans, dan Boilly, litograf Fenzl, K. Venkataramana,
Retaildesigner). Rinciannya ada pada `PPT-fisdas-1-latex/gambar.csv`.

Pertemuan 10–15 (terbit 24 November 2026; nomor berkas = minggu RPS, sehingga
deck yang semula bernomor 8 kini bernomor 9):

| Deck | Lisensi | Atribusi (Wikimedia Commons) |
|---|---|---|
| Fisika Dasar TPB P11 | CC BY-SA 3.0 de | Reinhard Manthey, `File:Old-fashioned light bulb.jpg` |
| Fisika Dasar TPB P12 | CC BY-SA 4.0 | MikeRun, Vera Wurmsdobler, `File:Bar-magnet-iron-filings max.jpg` |
| Fisika Dasar TPB P12 | CC BY 3.0 | Bidgee, `File:Pole mounted Transformer.jpg` |
| Fisika Dasar TPB P13, 15 | CC BY-SA 4.0 | Pksois23, `File:Thin Film Interference Soap Bubble.jpg` |
| Fisika Dasar TPB P13 | CC BY 4.0 | Mariojan photo, `File:Diesel fuel on wet asphalt mj1.jpg` |
| Fisika Dasar TPB P13 | CC BY-SA 4.0 | Graham Beards, `File:Young's slits.jpg` |
| Fisika Dasar TPB P14 | CC BY-SA 3.0 | Meganbeckett27, `File:Pencil in glass of water showing refraction (cropped).JPG` |
| Fisika Dasar TPB P14 | CC BY-SA 2.0 | Neil Theasby, `File:Convex traffic mirror by a bend at Ford - geograph.org.uk - 6059314.jpg` |
| Fisika Dasar TPB P14 | CC BY-SA 4.0 | AntanO, `File:Convex lens (magnifying glass) and upside-down image.jpg` |
| Fisika Dasar TPB P14 | CC BY-SA 2.5 | Eric Rolph at English Wikipedia, `File:Double-alaskan-rainbow.jpg` |
| Fisika Dasar TPB P14 | CC BY-SA 3.0 | BigRiz, `File:Fibreoptic.jpg` |
| Fisika Dasar TPB P15 | CC BY-SA 3.0 | Kabelleger / David Gubler (http://www.bahnbilder.ch), `File:VRB H 1-2 bei Freibergen.jpg` |
| Fisika Dasar TPB P15 | CC BY-SA 2.0 | Bob Harvey, `File:Substation transformer - geograph.org.uk - 5573682.jpg` |
| Fisika Dasar TPB P12 | CC BY 3.0 | Jan Ainali, `File:MRI-Philips.JPG` |
| Fisika Dasar TPB P12 | CC BY 2.5 | S.J. de Waard, `File:Cut-away version of an electric motor (1).JPG` |
| Fisika Dasar TPB P12 | CC BY-SA 3.0 | Wtshymanski, `File:Induction Cooktop Rolling Boil Cropped.jpg` |
| Fisika Dasar TPB P12 | CC BY-SA 3.0 | Sebastian Terfloth, `File:Wirbelstrombremse aktiv.jpg` |
| Fisika Dasar TPB P12 | CC BY 2.0 | Honda CB77 Restoration (Flickr), `File:Ignition coils.jpg` |
| Fisika Dasar TPB P12 | CC BY 2.0 | Stefan Andrej Shambora, `File:High voltage transmission towers and lines.jpg` |

Foto lain pada Pertemuan 10–15 berstatus domain publik atau CC0 (NOAA Photo Library, John G. Trump, Charles-Augustin de Coulomb, Walter Larden, Retired electrician, Ron Clausen, Evan-Amos, Emspangler at English Wikiversity, Original: unknown, Christian Albrecht Jensen, Thomas Phillips, United States Air Force photo by Senior Airman Joshua Strang, Alfred T. Palmer, Unidentified photographer. Smithsonian Institution from United States, After Thomas Lawrence, Ulfbastel, Elcap, John B. Livingood, Tyler C.).

**Foto pada deck Karakterisasi Material (sejak 24 November 2026).** Minggu 9–14
memuat foto dari Wikimedia Commons; atribusinya tercetak di bawah tiap foto
(`\sumberfoto`). Selebihnya gambar dibuat sendiri dengan TikZ/pgfplots, dan
citra AFM serta spektrum FTIR studi kasus adalah data sintetis buatan sendiri.
Yang berlisensi BY/BY-SA diulang di sini:

| Deck | Lisensi | Atribusi (Wikimedia Commons) |
|---|---|---|
| Karakterisasi Material Mg 9 | CC BY-SA 4.0 | Tadeáš Bednarz, `File:Scanning electron microscope - UFCH JH (2020) 01.jpg` |
| Karakterisasi Material Mg 9 | CC BY-SA 3.0 | Zephyris, `File:SEMStubs.jpg` |
| Karakterisasi Material Mg 9 | CC BY-SA 4.0 | Brandon Antonio Segura Torres & Priscilla Vieto Bonilla, `File:Muestras bañadas en oro para el SEM.jpg` |
| Karakterisasi Material Mg 9 | CC BY-SA 4.0 | PaulT (Gunther Tschuch), `File:Hitachi S-2400 SEM 15.jpg` |
| Karakterisasi Material Mg 9 | CC BY-SA 4.0 | ErwinMeier, `File:Schottky-Emitter 01.jpg` |
| Karakterisasi Material Mg 9 | CC BY 4.0 | ZhanserikKT, `File:ZnO nanorods.tif` |
| Karakterisasi Material Mg 9 | CC BY 4.0 | Luciasauter, `File:REM EDX 11.png` |
| Karakterisasi Material Mg 9 | CC BY 4.0 | Kanet Abubakir, `File:EDS elemental mapping.png` |
| Karakterisasi Material Mg 10 | CC BY-SA 3.0 | Hannes Grobe, `File:X-ray tube-co hg.jpg` |
| Karakterisasi Material Mg 10 | CC BY-SA 4.0 | Warrenmck, `File:XYZ stage powder diffraction of solid sample.jpg` |
| Karakterisasi Material Mg 10 | CC BY-SA 3.0 | Tizeff, `File:Laue-Cubic-Disoriented.PNG` |
| Karakterisasi Material Mg 10 | CC BY-SA 3.0 | Kuebi = Armin Kübelbeck, `File:Debye-Scherrer-Kamera 01.jpg` |
| Karakterisasi Material Mg 11 | CC BY-SA 3.0 | Zureks, `File:Atomic force microscope by Zureks.jpg` |
| Karakterisasi Material Mg 11 | CC BY 2.5 | Kristian Mølhave, `File:Typical AFM cantilever.jpg` |
| Karakterisasi Material Mg 11 | CC BY-SA 4.0 | Mehrabanian, `File:AFM 3D Topography Image of Silver Nanoparticles on Chitosan Film.tif` |
| Karakterisasi Material Mg 11 | CC BY-SA 4.0 | Krischkrisch, `File:LB Film 1.5mN 2048 height extracted.jpg` |
| Karakterisasi Material Mg 11 | CC BY-SA 4.0 | Matthias A. Fenner, `File:DNA Origami Triangular.png` |
| Karakterisasi Material Mg 12 | CC BY 4.0 | Wang, F., Zhang, L., Zhang, X., Li, H. and Wu, S., `File:FTIR spectrometer.png` |
| Karakterisasi Material Mg 12 | CC BY-SA 4.0 | Keshavana, `File:FTIR Spectrometer + ATR.jpg` |
| Karakterisasi Material Mg 12 | CC BY-SA 4.0 | Willmichaels1012, `File:ATR accessory.jpg` |
| Karakterisasi Material Mg 12 | CC BY-SA 3.0 | Cepheiden, `File:Infraredspectroscopy - transmission with Kbr pellets.jpg` |
| Karakterisasi Material Mg 12 | CC BY-SA 3.0 | Izmaelt, `File:IR Spectrum of Tris(acetylacetonato)iron(III).png` |
| Karakterisasi Material Mg 13 | CC BY-SA 4.0 | Retama, `File:Spectrophotometer cuvettes.JPG` |
| Karakterisasi Material Mg 13 | CC BY-SA 2.5 | Hannes Grobe/AWI, `File:Fluorescent minerals hg.jpg` |
| Karakterisasi Material Mg 13 | CC BY-SA 3.0 | Didier Descouens, `File:Calcite-Maroc-UV.jpg` |
| Karakterisasi Material Mg 14 | CC BY-SA 4.0 | Rgarrigan, `File:Micromanipulator Semiautomatic Probe Station.jpg` |
| Karakterisasi Material Mg 14 | CC BY-SA 4.0 | Radiotrefoil, `File:Multicrystalline silicon wafer with thin film iridescence.jpg` |
| Karakterisasi Material Mg 14 | CC BY-SA 4.0 | Radiotrefoil, `File:4 inch float zone n-type silicon wafer with amorphous silicon thin film heterojunction structure.png` |
| Karakterisasi Material Mg 14 | CC BY 3.0 | Tomasz Sienicki, `File:Digital universal multimeter (ubt).jpeg` |

Foto lain berstatus domain publik atau CC0 (Elcap, XanaG, Wilhelm Röntgen, Limojoe at Czech Wikipedia, NIST, Joseph Stroscio et. al., TimVickers, NASA, Bullis, W. Murray).
Deck Minggu 12 (FTIR) juga memuat tabel frekuensi gugus yang dipilih dari
LibreTexts, "Infrared Spectroscopy Absorption Table" (CC BY-NC-SA 4.0), dengan
sumber tercetak pada slidenya. Rinciannya ada pada
`KULIAH/Karakterisasi Material/2026-2027 Ganjil/slides/gambar.csv`. Deck
Karakterisasi Material lama (sebelum 2026/2027) tetap tidak diterbitkan.

**Gambar dari publikasi sendiri digambar ulang.** Plot Tauc (MEOM Mg 4) dan
kurva *J*–*V* (MEOM Mg 6) berasal dari M. A. Al Qadri dkk., *J. Electron. Mater.*
(2024), doi:10.1007/s11664-024-11386-1, Gbr. 5 dan 6. Karena hak cipta terbitan
dialihkan ke penerbit, gambar aslinya tidak ikut terbit; sejak 5 Oktober 2026
keduanya digambar ulang dengan pgfplots dari nilai yang dilaporkan paper, dengan
sitasi lengkap pada slidenya.

Data nilai, daftar hadir, dan naskah tugas akhir mahasiswa tidak dimuat di situs
ini. Pengecualiannya adalah dua dokumen bimbingan pada `dokumen-ta/`, yang
diterbitkan atas permintaan dosen pembimbing:

| Berkas | Isi | Data pribadi |
|---|---|---|
| `simpulan-judul-ta-2026.pdf` | Ketetapan 13 judul TA 2026 per kode topik | Nama panggilan mahasiswa bimbingan; **tanpa** NIM, kontak, nilai, atau berkas naskah |
| `surat-pernyataan-keseriusan-ta.pdf` | Formulir komitmen bimbingan | Tidak ada — seluruh isian masih kosong |

Nama pada dokumen pertama berada pada tingkat keterbukaan yang sama dengan
halaman `theses.html`, yang memang menampilkan nama dan judul tugas akhir
mahasiswa bimbingan. Bila suatu saat daftar itu perlu ditutup namanya, ganti
berkasnya dengan versi berkode topik saja dan jalankan ulang
`tools/publish.sh` — tautan di `theses.html` tidak perlu diubah.
Halaman **Tugas Akhir** memuat nama dan judul tugas akhir lulusan — keduanya
bersifat publik sebagaimana tercantum pada repositori tugas akhir ITERA. NIM,
nilai, dan berkas naskah tidak dicantumkan.

---

## 7. Sumber data

Konten situs disusun dari dokumen resmi di Google Drive:

| Bagian | Sumber |
|---|---|
| Profil, publikasi, hibah, paten, penghargaan | `CV Eka/2025-03-07 Biodata Eka Nurfani.docx` |
| Daftar peralatan dan bahan | `Research/LIST ALAT DAN BAHAN LAB EN (uptdate Sep 2025).xlsx` |
| Instrumen rakitan sendiri | `Research/Design Spin Coater Home Made`, `Design Stasiun JV Simulator LED Home Made`, `Design Stasiun Light Soaking Home Made` |
| Materi kuliah | `KULIAH/<mata kuliah>/` |
| Judul tugas akhir dan nama lulusan | `Research/Bimbingan TA/<tahun> <nama>/` (halaman sampul naskah TA) |
| Foto profil | `Foto Eka 3x4 BG_biru.png` |
| Logo dan palet warna | `WEBSITE LAB/logo/logo-ENLab.png` |
