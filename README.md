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
│                           publikasi terbaru, pendanaan, pengajaran, galeri, kontak)
├── publications.html       Daftar 57 publikasi + pencarian & filter
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
│   │   └── main.js         Logika: bahasa, tema, navigasi, perender data
│   └── img/                logo, favicon, foto, gambar Open Graph
│
├── logo/                   Berkas logo asli (sumber, jangan dihapus)
│
├── materi/                 Berkas PDF materi kuliah, dikelompokkan per mata kuliah
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

Logo asli tersimpan di `logo/logo-ENLab.png`. Tiga berkas turunan dibuat darinya
dan dipakai situs:

| Berkas | Dipakai untuk |
|---|---|
| `assets/img/logo-emblem.png` | Lambang di header dan footer (latar transparan) |
| `assets/img/logo-enlab.png` | Logo penuh pada hero dan gambar Open Graph |
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
      keterangan umum. Nama mahasiswa sengaja tidak dicantumkan; tambahkan hanya
      atas persetujuan yang bersangkutan.
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

Data nilai, daftar hadir, dan nama mahasiswa bimbingan tidak dimuat di situs ini.

---

## 7. Sumber data

Konten situs disusun dari dokumen resmi di Google Drive:

| Bagian | Sumber |
|---|---|
| Profil, publikasi, hibah, paten, penghargaan | `CV Eka/2025-03-07 Biodata Eka Nurfani.docx` |
| Daftar peralatan dan bahan | `Research/LIST ALAT DAN BAHAN LAB EN (uptdate Sep 2025).xlsx` |
| Instrumen rakitan sendiri | `Research/Design Spin Coater Home Made`, `Design Stasiun JV Simulator LED Home Made`, `Design Stasiun Light Soaking Home Made` |
| Materi kuliah | `KULIAH/<mata kuliah>/` |
| Foto profil | `Foto Eka 3x4 BG_biru.png` |
| Logo dan palet warna | `WEBSITE LAB/logo/logo-ENLab.png` |
