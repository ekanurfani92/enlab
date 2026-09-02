#!/usr/bin/env python3
"""
Menyelaraskan daftar materi kuliah dengan isi folder materi/ yang sebenarnya.

Jalankan setiap kali Anda menambah, menghapus, atau mengganti nama berkas PDF
di dalam folder materi/:

    python3 tools/sync_materi.py

Skrip akan:
  1. Memindai materi/<slug>/*.pdf
  2. Memperbarui daftar berkas pada assets/js/data-courses.js agar persis sama
  3. Menyetel window.MATERI_TERSEDIA secara otomatis: bernilai true hanya bila
     folder materi/ TIDAK lagi dikecualikan di .gitignore

Keterangan mata kuliah (judul, sks, deskripsi) tidak diubah. Judul materi yang
sudah pernah diatur juga dipertahankan; hanya berkas baru yang judulnya
diturunkan dari nama berkas.
"""

import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DATA = "assets/js/data-courses.js"


def load_courses():
    src = f"global.window={{}};require('./{DATA}');console.log(JSON.stringify(window.COURSES));"
    out = subprocess.run(["node", "-e", src], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def diterbitkan(slug):
    """Satu mata kuliah terbit bila foldernya tidak ditahan .gitignore.

    Git sendiri yang menjadi sumber kebenaran, sehingga daftar di situs tidak
    mungkin berbeda dengan berkas yang benar-benar terunggah."""
    try:
        r = subprocess.run(["git", "check-ignore", "-q", f"materi/{slug}"],
                           capture_output=True)
        return r.returncode != 0          # 0 = ditahan, 1 = boleh terbit
    except Exception:
        return False                      # bila git tidak tersedia: tahan (aman)



# Kata yang menandai berkas administratif atau rahasia. Dicocokkan per kata,
# bukan potongan, agar "latihan-soal" tidak ikut tertandai.
KATA_TERLARANG = {
    "rps", "kontrak", "nilai", "dna", "kunci", "jawaban", "rubrik",
    "absensi", "presensi", "uas", "uts", "quiz", "ujian", "penilaian",
}


def berkas_mencurigakan(path):
    kata = set(re.split(r"[^a-z0-9]+", os.path.basename(path).lower()))
    return sorted(kata & KATA_TERLARANG)


def judul_dari_nama(nama):
    t = re.sub(r"\.pdf$", "", nama, flags=re.I)
    t = re.sub(r"^\d+[a-z]?[-_. ]+", "", t)          # buang nomor urut di depan
    t = t.replace("-", " ").replace("_", " ")
    t = re.sub(r"\s+", " ", t).strip()
    kecil = {"dan", "di", "ke", "dari", "untuk", "pada", "yang", "dalam", "serta",
             "the", "of", "and", "in", "for", "on"}
    kata = [w if w.lower() in kecil else (w[:1].upper() + w[1:]) for w in t.split()]
    if kata:
        kata[0] = kata[0][:1].upper() + kata[0][1:]
    return " ".join(kata)


def urutan(nama):
    m = re.match(r"\s*(\d+)", nama)
    return (int(m.group(1)) if m else 999, nama.lower())


def sync_narasumber():
    """Menyelaraskan ukuran berkas pada data-talks.js dengan berkas sebenarnya.

    Judul dan nama acara ditulis tangan karena tidak dapat diturunkan dari nama
    berkas; hanya ukuran yang diperbarui otomatis, ditambah peringatan bila ada
    berkas yang tercantum tetapi hilang, atau tergeletak tetapi belum didaftarkan.
    """
    data = "assets/js/data-talks.js"
    if not os.path.exists(data):
        return
    src = f"global.window={{}};require('./{data}');console.log(JSON.stringify(window.TALKS));"
    talks = json.loads(subprocess.run(["node", "-e", src],
                                      capture_output=True, text=True, check=True).stdout)

    teks = open(data, encoding="utf-8").read()
    diperbarui, hilang = 0, []
    for x in talks:
        if not os.path.exists(x["f"]):
            hilang.append(x["f"])
            continue
        mb = round(os.path.getsize(x["f"]) / 1048576, 2)
        pola = re.compile(r'("f":\s*"' + re.escape(x["f"]) + r'",\s*"s":\s*)([\d.]+)')
        teks, n = pola.subn(lambda m: m.group(1) + repr(mb), teks, count=1)
        if n and float(x["s"]) != mb:
            diperbarui += 1
    open(data, "w", encoding="utf-8").write(teks)

    terdaftar = {x["f"] for x in talks}
    nyasar = sorted(f"narasumber/{f}" for f in os.listdir("narasumber")
                    if f.lower().endswith(".pdf")) if os.path.isdir("narasumber") else []
    nyasar = [f for f in nyasar if f not in terdaftar]

    print(f"  narasumber              : {len(talks)} entri, {diperbarui} ukuran diperbarui")
    for f in hilang:
        print(f"      HILANG  {f}  (tercantum di data-talks.js, berkasnya tidak ada)")
    for f in nyasar:
        print(f"      ?       {f}  (belum didaftarkan di data-talks.js)")


def main():
    courses = load_courses()
    judul_lama = {m["f"]: m["t"] for c in courses for m in c["m"]}

    total, tambah, hapus = 0, [], []
    for c in courses:
        folder = os.path.join("materi", c["slug"])
        berkas = []
        if os.path.isdir(folder):
            berkas = sorted((f for f in os.listdir(folder) if f.lower().endswith(".pdf")),
                            key=urutan)
        baru = []
        for f in berkas:
            path = f"materi/{c['slug']}/{f}"
            mb = round(os.path.getsize(os.path.join(folder, f)) / 1048576, 2)
            baru.append({"t": judul_lama.get(path) or judul_dari_nama(f), "f": path, "s": mb})
            if path not in judul_lama:
                tambah.append(path)
        for m in c["m"]:
            if m["f"] not in {x["f"] for x in baru}:
                hapus.append(m["f"])
        c["m"] = baru
        c["pub"] = diterbitkan(c["slug"])
        total += len(baru)

    # PDF yang tergeletak langsung di materi/ tidak akan pernah terpakai:
    # setiap berkas harus berada di dalam folder mata kuliah.
    nyasar = []
    if os.path.isdir("materi"):
        nyasar = sorted(f for f in os.listdir("materi") if f.lower().endswith(".pdf"))

    slug_sah = {c["slug"] for c in courses}
    folder_asing = []
    if os.path.isdir("materi"):
        for d in sorted(os.listdir("materi")):
            if os.path.isdir(os.path.join("materi", d)) and d not in slug_sah:
                folder_asing.append(d)

    terbit_count = sum(1 for c in courses if c["pub"])
    out = [
        "/* Daftar mata kuliah yang diampu Dr. Eka Nurfani.",
        "   Bagian \"m\" diselaraskan otomatis dengan isi folder materi/.",
        "   Jangan sunting tangan: tambah atau hapus berkas PDF-nya, lalu jalankan",
        "   python3 tools/sync_materi.py */",
        "window.COURSES = [",
    ]
    for c in courses:
        out.append("  " + json.dumps(c, ensure_ascii=False) + ",")
    out.append("];")
    open(DATA, "w", encoding="utf-8").write("\n".join(out) + "\n")

    print(f"  berkas materi terdaftar : {total}")
    print(f"  ditambahkan             : {len(tambah)}")
    for p in tambah[:8]:
        print("      + " + p)
    print(f"  dikeluarkan             : {len(hapus)}")
    for p in hapus[:8]:
        print("      - " + p)
    print(f"  mata kuliah terbit      : {terbit_count} dari {len(courses)}")
    for c in courses:
        if c["pub"]:
            print(f"      terbit  {c['slug']:32s} {len(c['m'])} berkas")
    tertahan = sum(len(c["m"]) for c in courses if not c["pub"])
    if tertahan:
        print(f"      ditahan {'(belum disortir)':32s} {tertahan} berkas")
    sync_narasumber()

    if nyasar:
        print(f"\n  PERHATIAN: {len(nyasar)} berkas PDF tergeletak langsung di materi/")
        print("  dan TIDAK akan tampil di situs. Pindahkan ke folder mata kuliahnya:")
        for f in nyasar[:8]:
            print("      ? materi/" + f)
        print("  Daftar folder yang tersedia ada di materi/BACA-INI.txt")

    if folder_asing:
        print(f"\n  PERHATIAN: folder berikut tidak dikenali dan diabaikan:")
        for d in folder_asing[:8]:
            print("      ? materi/" + d + "/")
        print("  Nama folder harus sama persis dengan slug mata kuliah (lihat BACA-INI.txt).")

    curiga = [(m["f"], berkas_mencurigakan(m["f"]))
              for c in courses if c["pub"]
              for m in c["m"] if berkas_mencurigakan(m["f"])]
    if curiga:
        print(f"\n  PERIKSA LAGI: {len(curiga)} berkas bernama seperti dokumen administratif.")
        print("  Jangan terbitkan RPS bertanda tangan, daftar nilai, soal ujian, atau kunci jawaban.")
        for f, kata in curiga[:8]:
            print(f"      ! {f}   (kata: {', '.join(kata)})")
        print("  Bila berkas ini memang materi belajar, abaikan pesan ini.")

    aneh = [m["f"] for c in courses for m in c["m"]
            if re.search(r"[^A-Za-z0-9/._-]", m["f"])]
    if aneh:
        print(f"\n  Catatan: {len(aneh)} nama berkas memuat spasi atau karakter khusus.")
        print("  Tautannya tetap berfungsi, tetapi nama sederhana lebih rapi di URL.")
        for f in aneh[:5]:
            print("      ~ " + f)
    if tertahan:
        print("\n  Untuk menerbitkan satu mata kuliah, tambahkan barisnya di .gitignore:")
        print("      !materi/<slug>/")
        print("  lalu jalankan skrip ini lagi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
