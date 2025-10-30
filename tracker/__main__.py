"""Entry point agar bisa dijalankan langsung dengan `python -m tracker`."""
from tracker import RekapKelas, build_markdown_report, save_text
import os

def main():
    print("=== Menjalankan student_performance_tracker ===")

    rk = RekapKelas()

    # Tambahkan beberapa contoh mahasiswa
    rk.tambah_mahasiswa("230101001", "Ana", 92)
    rk.set_penilaian("230101001", quiz=90, tugas=85, uts=88, uas=92)

    rk.tambah_mahasiswa("230101002", "Bimo", 80)
    rk.set_penilaian("230101002", quiz=70, tugas=75, uts=68, uas=72)

    rk.tambah_mahasiswa("230101003", "Citra", 60)
    rk.set_penilaian("230101003", quiz=50, tugas=60, uts=55, uas=58)

    # Buat laporan otomatis
    records = rk.rekap()
    os.makedirs("out", exist_ok=True)
    content = build_markdown_report(records)
    save_text("out/report.md", content)

    print("📄 Laporan berhasil dibuat di: out/report.md")
    print("Mahasiswa yang tercantum:", len(records), "orang.")

if __name__ == "__main__":
    main()
