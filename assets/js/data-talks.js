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
  { "d": "2026-10-31",
    "dt": { "id": "31 Oktober 2026", "en": "31 October 2026" },
    "t": { "id": "Konversi dan Penyimpanan Energi Surya: Perspektif Teknik Material",
           "en": "Solar Energy Conversion and Storage: A Materials Engineering Perspective" },
    "e": { "id": "Studium Generale Program Studi Teknik Material ITERA",
           "en": "Materials Engineering Studium Generale, ITERA" },
    "f": "narasumber/2026-10-31-studium-generale-teknik-material.pdf",
    "s": 2.79 },
  { "d": "2025-02-10",
    "dt": { "id": "10 Februari 2025", "en": "10 February 2025" },
    "t": { "id": "Pengalaman Mendapatkan Pendanaan RIIM Kompetisi Gelombang 3",
           "en": "Securing RIIM Kompetisi Wave 3 Research Funding" },
    "e": { "id": "Sharing Session Penulisan Proposal RIIM",
           "en": "RIIM Proposal Writing Sharing Session" },
    "f": "narasumber/2025-02-10-sharing-session-penulisan-proposal-riim.pdf",
    "s": 0.47 },
  { "d": "2024-12-04",
    "dt": { "id": "4 Desember 2024", "en": "4 December 2024" },
    "t": { "id": "Pengenalan Kelompok Riset Pemrosesan Material dan Material Maju",
           "en": "Introduction to Material Processing and Advanced Materials Research Group" },
    "e": { "id": "Webinar Kolaborasi Riset AUT-ITERA",
           "en": "AUT-ITERA Research Collaboration Webinar" },
    "f": "narasumber/2024-12-04-aut-itera-research-collaboration-webinar.pdf",
    "s": 2.05 },
];
