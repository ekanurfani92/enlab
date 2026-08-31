#!/usr/bin/env bash
#
# Menerbitkan perubahan situs ENLab dengan satu perintah.
#
#   bash tools/publish.sh "keterangan singkat perubahan"
#
# Urutan yang dijalankan:
#   1. Menyelaraskan daftar materi dengan isi folder materi/
#   2. Membangun ulang halaman HTML
#   3. Menjalankan tujuh pemeriksaan kesehatan situs
#   4. Mengunggah ke GitHub (situs diperbarui otomatis ~1 menit kemudian)
#
# Bila pemeriksaan gagal, pengunggahan DIBATALKAN agar situs yang sedang
# online tidak ikut rusak.

set -euo pipefail
cd "$(dirname "$0")/.."

PESAN="${1:-Perbarui isi situs}"

echo "1/4  Menyelaraskan daftar materi"
python3 tools/sync_materi.py | sed 's/^/     /'

echo
echo "2/4  Membangun ulang halaman"
python3 tools/build_pages.py | sed 's/^/     /'

echo
echo "3/4  Memeriksa"
if ! python3 tools/verify.py > /tmp/enlab-verify.log 2>&1; then
  echo
  echo "     PEMERIKSAAN GAGAL - pengunggahan dibatalkan."
  echo "     Situs yang sedang online tidak terpengaruh. Rinciannya:"
  echo
  sed 's/^/     /' /tmp/enlab-verify.log
  exit 1
fi
grep -c "OK" /tmp/enlab-verify.log | xargs -I{} echo "     {} pemeriksaan lolos"

echo
echo "4/4  Mengunggah"
git add -A
if git diff --cached --quiet; then
  echo "     Tidak ada perubahan. Tidak ada yang perlu diunggah."
  exit 0
fi
git diff --cached --stat | tail -1 | sed 's/^/     /'
git commit -q -m "$PESAN"
git push -q
echo
echo "Selesai. Situs diperbarui dalam sekitar satu menit:"
echo "  https://ekanurfani92.github.io/enlab/"
