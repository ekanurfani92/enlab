/* Undangan sebagai narasumber: webinar, seminar, dan sesi berbagi.
   d  = tanggal ISO, dipakai untuk urutan dan tahun yang tampil
   dt = tanggal sebagaimana ditulis di halaman
   t  = judul presentasi, diambil dari halaman judul slide
   e  = nama acara
   f  = berkas slide di folder narasumber/
   s  = ukuran berkas dalam MB, diselaraskan otomatis oleh tools/sync_materi.py

   Menambah entri baru: taruh PDF-nya di narasumber/, sisipkan satu objek di
   paling atas daftar, lalu jalankan bash tools/publish.sh */
window.TALKS = [
  { "d": "2024-12-04",
    "dt": { "id": "4 Desember 2024", "en": "4 December 2024" },
    "t": { "id": "Pengenalan Kelompok Riset Pemrosesan Material dan Material Maju",
           "en": "Introduction to Material Processing and Advanced Materials Research Group" },
    "e": { "id": "Webinar Kolaborasi Riset AUT-ITERA",
           "en": "AUT-ITERA Research Collaboration Webinar" },
    "f": "narasumber/2024-12-04-aut-itera-research-collaboration-webinar.pdf",
    "s": 2.05 },
];
