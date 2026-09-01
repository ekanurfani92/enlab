# Panduan Mandiri — Merawat Situs ENLab

Ditulis agar Anda dapat memperbarui situs sendiri, tanpa bantuan siapa pun.
Tidak mengandaikan pengalaman pemrograman.

- Situs   : <https://ekanurfani92.github.io/enlab/>
- Kode    : <https://github.com/ekanurfani92/enlab>
- Folder  : `Google Drive/ITERA-EKA NURFANI/Research/WEBSITE LAB`

---

## 1. Memahami cara kerjanya

Ada tiga tempat, dan isinya harus sama:

```
   FOLDER DI LAPTOP                GITHUB                    SITUS
   (tempat Anda menyunting)   (tempat penyimpanan)     (yang dilihat orang)

   WEBSITE LAB/        --->    github.com/          --->   ekanurfani92
     index.html               ekanurfani92/enlab            .github.io/enlab/
     assets/
     materi/                    [ push ]                  [ otomatis ~1 menit ]
```

Menyunting berkas di laptop **tidak** mengubah situs. Perubahan baru terbit
setelah dikirim ("push") ke GitHub. GitHub lalu membangun ulang situs sendiri.

Yang perlu diingat: situs ini **statis**. Tidak ada basis data dan tidak ada
halaman admin. Semua isi tersimpan sebagai berkas biasa. Menambah publikasi
berarti menyunting sebuah berkas, bukan mengisi formulir.

---

## 2. Tiga cara memperbarui

Pilih yang paling nyaman. Ketiganya menghasilkan hal yang sama.

| Cara | Kapan dipakai | Perlu terminal? |
|---|---|---|
| **A. Lewat situs GitHub** | Perbaikan kecil: salah ketik, ganti satu kalimat | Tidak |
| **B. Satu perintah** | Pemakaian sehari-hari | Ya, satu baris |
| **C. Perintah git satu per satu** | Saat ingin memahami apa yang terjadi | Ya |

### Cara A — lewat situs GitHub (tanpa terminal)

1. Buka <https://github.com/ekanurfani92/enlab>
2. Klik berkas yang ingin diubah, misalnya `assets/js/data-publications.js`
3. Klik ikon pensil (**Edit this file**) di kanan atas
4. Sunting isinya
5. Gulir ke bawah, tulis keterangan singkat, klik **Commit changes**

Menambah berkas: tombol **Add file → Upload files**, lalu seret berkas atau
folder ke halaman itu.

> **Hati-hati.** Cara ini melewatkan pemeriksaan otomatis. Bila hasil suntingan
> salah tulis, situs bisa rusak tanpa peringatan. Untuk perubahan besar,
> gunakan cara B.

### Cara B — satu perintah (disarankan)

Buka Terminal, lalu:

```bash
cd "/Users/novaliapertiwi/Library/CloudStorage/GoogleDrive-eka.nurfani@mt.itera.ac.id/My Drive/ITERA-EKA NURFANI/Research/WEBSITE LAB"

bash tools/publish.sh "tambah publikasi 2026"
```

Perintah itu menjalankan empat langkah berurutan:

1. menyelaraskan daftar materi dengan isi folder `materi/`
2. membangun ulang halaman HTML
3. menjalankan pemeriksaan kesehatan situs
4. mengunggah ke GitHub

**Bila pemeriksaan gagal, pengunggahan dibatalkan** dan situs yang sedang online
tidak tersentuh. Ini pengaman utama Anda.

### Cara C — perintah git satu per satu

Empat perintah ini yang sebenarnya dijalankan oleh cara B:

```bash
git status     # 1. lihat berkas apa saja yang berubah
git add -A     # 2. tandai semua perubahan untuk dikirim
git commit -m "tambah publikasi 2026"   # 3. simpan sebagai satu titik riwayat
git push       # 4. kirim ke GitHub
```

Analoginya: `add` seperti memasukkan dokumen ke dalam amplop, `commit` menyegel
amplop dan memberinya label, `push` mengirim amplop itu ke GitHub. Selama belum
`push`, semuanya masih di laptop Anda.

Sebelum `push`, biasakan menjalankan:

```bash
python3 tools/verify.py
```

---

## 3. Resep praktis

### 3.1 Mengunggah materi kuliah

Ini yang tertunda. Langkahnya:

**Langkah 1 — sortir berkasnya.**
Buka folder `materi/`. Isinya sudah dikelompokkan per mata kuliah:

```
materi/
  karakterisasi-material/    6 berkas
  fisika-dasar-2/            9 berkas
  material-keramik/          4 berkas
  material-sensor/           2 berkas
  fenomena-transpor-material/ 2 berkas
  pengenalan-prodi/          2 berkas
```

Hapus berkas yang tidak ingin diterbitkan. Tambahkan yang baru bila ada.
**Tidak perlu menyunting berkas JavaScript apa pun** — daftarnya diselaraskan
otomatis pada langkah 3.

**Langkah 2 — izinkan mata kuliah itu terbit.**
Penerbitan diatur **per mata kuliah**, sehingga Anda dapat menerbitkan satu
mata kuliah sambil menyortir sisanya dengan tenang.

Buka `.gitignore`, tambahkan satu baris di bawah bagian penanda:

```
!materi/karakterisasi-material/
```

Ganti `karakterisasi-material` dengan slug mata kuliah yang dituju (daftar
lengkapnya ada di `materi/BACA-INI.txt`). Tanda seru berarti "kecualikan dari
penahanan".

**Langkah 3 — terbitkan.**

```bash
bash tools/publish.sh "terbitkan materi kuliah"
```

Skrip akan mendaftar ulang berkas yang benar-benar ada, menyalakan tautan
unduh, memeriksa, lalu mengunggah.

**Menambah materi baru di kemudian hari:** untuk mata kuliah yang sudah
pernah terbit, cukup taruh PDF di foldernya lalu jalankan
`bash tools/publish.sh "tambah materi"`. Tidak perlu menyentuh `.gitignore` lagi.

**Memeriksa apa saja yang akan terbit** tanpa mengunggah apa pun:

```bash
python3 tools/sync_materi.py
```

Perintah itu menampilkan mata kuliah mana yang terbit, mana yang masih
ditahan, dan berapa berkasnya.

**Memperkecil PDF yang besar** (di atas ~5 MB):

```bash
gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=hasil.pdf asli.pdf
```

### 3.2 Menambah publikasi baru

Buka `assets/js/data-publications.js`. Sisipkan satu baris **di paling atas**
daftar, tepat setelah `window.PUBLICATIONS = [`:

```js
  {"y": 2026, "t": "Judul lengkap artikel", "v": "Nama Jurnal", "d": "Vol. 12, No. 103421", "k": "journal"},
```

Keterangan: `y` tahun, `t` judul, `v` nama jurnal, `d` volume/nomor,
`k` jenis — isi dengan `journal` (jurnal internasional), `conference`
(prosiding), atau `national` (jurnal nasional).

Perhatikan: setiap teks diapit tanda kutip ganda, antar bagian dipisah koma,
dan baris diakhiri koma. Filter tahun di halaman publikasi terisi sendiri.

Jangan lupa memperbarui angka **57** pada dua tempat: statistik di
`tools/page_bodies.py` dan kalimat `pub.lead` di `assets/js/i18n.js`.

### 3.3 Mengubah tulisan di halaman

Semua tulisan ada di `assets/js/i18n.js`, dalam dua bahasa.

```js
"about.h2": "Merekayasa material untuk masa depan energi yang lebih bersih.",
```

Setiap kunci **wajib ada di kedua bahasa** (`id:` dan `en:`). Bila salah satu
hilang, `verify.py` akan menolak. Jangan mengubah nama kunci di sebelah kiri —
itu penanda yang dipakai halaman HTML.

### 3.4 Mengganti kotak galeri dengan foto

1. Simpan foto ke `assets/img/`, misalnya `lab-sintesis.jpg`
   (anjuran: 1200×800 piksel, di bawah 300 KB)
2. Buka `tools/page_bodies.py`, cari bagian galeri
3. Ubah `<div class="tile tile-1">` menjadi:

```html
<div class="tile tile-1" style="background-image:url('assets/img/lab-sintesis.jpg')">
```

4. Jalankan `bash tools/publish.sh "tambah foto galeri"`

### 3.5 Mengubah navigasi, header, atau footer

Ada di `tools/build_pages.py`. Setelah menyunting, halaman HTML harus dibangun
ulang — `publish.sh` sudah melakukannya untuk Anda.

---

### 3.6 Menambah tugas akhir mahasiswa

Buka `assets/js/data-theses.js`. Sisipkan satu objek **di paling atas** daftar,
tepat setelah `window.THESES = [`:

```js
  { "y": 2027, "n": "Nama Lengkap Mahasiswa",
    "t": { "id": "Judul tugas akhir dalam Bahasa Indonesia",
           "en": "Thesis title in English" } },
```

Keterangan:

- `y` — tahun kelulusan; daftar dikelompokkan sendiri per tahun.
- `n` — nama lengkap mahasiswa (NIM tidak dicantumkan di situs).
- `t` — judul tugas akhir, versi Bahasa Indonesia dan Inggris.

Hanya tahun, nama, dan judul yang ditampilkan di situs.

Setelah menyunting, jalankan `python3 tools/build_pages.py` supaya teks cadangan
pada `theses.html` dan cuplikan di beranda ikut diperbarui.

---

## 4. Memeriksa sebelum menerbitkan

**Melihat situs di laptop:**

```bash
python3 -m http.server 8000
```

Lalu buka <http://localhost:8000>. Hentikan dengan `Ctrl+C`.
Jangan membuka `index.html` dengan klik ganda — berkas PDF dan sebagian
tautan berperilaku berbeda pada mode itu.

**Menjalankan pemeriksaan:**

```bash
python3 tools/verify.py
```

Tujuh hal yang diperiksa:

1. terjemahan lengkap di kedua bahasa
2. semua tautan dan gambar tidak rusak
3. berkas materi ada dan saklarnya sinkron
4. data terstruktur (JSON-LD, manifest) sah
5. struktur HTML tidak ada tag yang lupa ditutup
6. aksesibilitas dan SEO dasar
7. tulisan di HTML sama dengan kamus terjemahan

---

## 5. Kalau ada yang salah

**Situs tidak berubah setelah diunggah.**
Tunggu satu sampai dua menit. Lalu muat ulang paksa: `Cmd + Shift + R`.
Bila masih sama, periksa <https://github.com/ekanurfani92/enlab/actions> —
tanda silang merah berarti pembangunan gagal.

**`verify.py` melaporkan kegagalan.**
Bacalah barisnya; pesan menyebut berkas dan masalahnya. Perbaiki, lalu
jalankan lagi. Selama belum lolos, jangan `push`.

**Salah mengunggah berkas.**
Hapus berkasnya dari folder, lalu jalankan `publish.sh` lagi. Perlu diingat:
berkas yang pernah terbit tetap tersimpan di riwayat GitHub. Bila yang terunggah
bersifat rahasia, jangan cukup menghapusnya — beri tahu saya atau hapus seluruh
repositori dan buat ulang.

**`git push` ditolak.**
Artinya ada perubahan di GitHub yang belum ada di laptop, biasanya karena Anda
sempat menyunting lewat situs GitHub. Jalankan:

```bash
git pull --rebase
git push
```

**Ingin membatalkan perubahan yang belum diunggah.**

```bash
git restore .        # buang semua suntingan yang belum di-commit
```

**Ingin melihat apa saja yang pernah diubah.**

```bash
git log --oneline
```

---

## 6. Daftar istilah

| Istilah | Artinya |
|---|---|
| **repository / repo** | Folder proyek beserta seluruh riwayat perubahannya |
| **commit** | Satu titik simpan berlabel keterangan |
| **push** | Mengirim commit dari laptop ke GitHub |
| **pull** | Mengambil perubahan dari GitHub ke laptop |
| **GitHub Pages** | Layanan gratis yang menyajikan berkas repo sebagai situs |
| **statis** | Situs tanpa basis data; seluruh isi berupa berkas biasa |
| **i18n** | Singkatan *internationalization*; sistem dwibahasa situs ini |
| **slug** | Nama pendek tanpa spasi untuk URL, mis. `material-keramik` |

---

## 7. Aturan yang sebaiknya tidak dilanggar

- **Jangan hapus** aturan CSS yang memberi alas putih pada logo di mode gelap
  (`.brand-logo`, `.logo-plate`). Garis putih pada panel surya dan molekul
  adalah bagian desain logo, bukan latar — tanpa alas itu logo tampak rusak.
- **Jangan tulis "Energy"** menggantikan "ENergy" pada nama resmi. Kapitalisasi
  itu menyandikan inisial pendiri laboratorium.
- **Jangan sunting tangan** bagian `"m"` pada `data-courses.js`; jalankan
  `python3 tools/sync_materi.py`.
- **Jangan unggah** buku teks atau materi pihak ketiga, RPS bertanda tangan,
  daftar nilai, absensi, soal ujian, kunci jawaban, atau rubrik penilaian.
  Hanya slide dan bahan belajar karya sendiri. Latihan soal beserta
  pembahasannya boleh, selama bukan soal ujian yang dinilai.
  Pemeriksa akan **membatalkan pengunggahan** bila menemukan nama berkas
  seperti `rps`, `nilai`, `uas`, `kunci`, `jawaban`, atau `rubrik`.
- **Jangan cantumkan** nama mahasiswa tanpa persetujuan yang bersangkutan.
