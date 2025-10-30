"""Aplikasi CLI Student Performance Tracker."""

import os
from tracker import (
    RekapKelas,
    build_markdown_report,
    build_html_report,
    save_text,
)

DATA_DIR = "data"
OUT_DIR = "out"
ATTENDANCE_CSV = os.path.join(DATA_DIR, "attendance.csv")
GRADES_CSV = os.path.join(DATA_DIR, "grades.csv")
OUT_REPORT = os.path.join(OUT_DIR, "report.md")
OUT_HTML = os.path.join(OUT_DIR, "report.html")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)

def print_menu():
    print("\n=== Student Performance Tracker ===")
    print("1) Muat data dari CSV")
    print("2) Tambah mahasiswa")
    print("3) Ubah presensi")
    print("4) Ubah nilai")
    print("5) Lihat rekap")
    print("6) Simpan laporan Markdown")
    print("7) Simpan data ke CSV")
    print("8) Tampilkan mahasiswa dengan nilai < 70")
    print("9) Simpan laporan HTML berwarna")
    print("10) Keluar")

def input_non_empty(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val

def main():
    ensure_dirs()
    rk = RekapKelas()

    while True:
        print_menu()
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            print("Memuat data dari CSV...")
            if os.path.exists(ATTENDANCE_CSV):
                rk.load_attendance_csv(ATTENDANCE_CSV)
                print(" - attendance.csv dimuat.")
            else:
                print(" - attendance.csv tidak ditemukan.")
            if os.path.exists(GRADES_CSV):
                rk.load_grades_csv(GRADES_CSV)
                print(" - grades.csv dimuat.")
            else:
                print(" - grades.csv tidak ditemukan.")

        elif pilihan == "2":
            nim = input_non_empty("NIM: ")
            nama = input_non_empty("Nama: ")
            hadir = input("Hadir (%): ").strip() or "0"
            try:
                rk.tambah_mahasiswa(nim, nama, hadir)
                print("Mahasiswa berhasil ditambahkan.")
            except Exception as e:
                print("Gagal:", e)

        elif pilihan == "3":
            nim = input_non_empty("NIM: ")
            hadir = input_non_empty("Persentase hadir baru: ")
            try:
                rk.set_hadir(nim, hadir)
                print("Presensi berhasil diperbarui.")
            except Exception as e:
                print("Gagal:", e)

        elif pilihan == "4":
            nim = input_non_empty("NIM: ")
            print("Kosongkan jika tidak ingin mengubah kolom tertentu.")
            quiz = input("Quiz: ").strip() or None
            tugas = input("Tugas: ").strip() or None
            uts = input("UTS: ").strip() or None
            uas = input("UAS: ").strip() or None
            try:
                rk.set_penilaian(nim, quiz=quiz, tugas=tugas, uts=uts, uas=uas)
                print("Nilai berhasil diperbarui.")
            except Exception as e:
                print("Gagal:", e)

        elif pilihan == "5":
            records = rk.rekap()
            if not records:
                print("Belum ada data.")
            else:
                print("\n| NIM | Nama | Hadir (%) | Nilai Akhir | Predikat |")
                print("|---|---|---:|---:|:---:|")
                for r in records:
                    print(f"| {r['nim']} | {r['nama']} | {r['hadir']:.1f} | {r['nilai_akhir']:.2f} | {r['predikat']} |")

        elif pilihan == "6":
            records = rk.rekap()
            content = build_markdown_report(records)
            save_text(OUT_REPORT, content)
            print(f"Laporan Markdown disimpan ke {OUT_REPORT}")

        elif pilihan == "7":
            rk.save_attendance_csv(ATTENDANCE_CSV)
            rk.save_grades_csv(GRADES_CSV)
            print("Data berhasil disimpan ke folder data/")

        elif pilihan == "8":
            records = rk.filter_below(70)
            if not records:
                print("Tidak ada mahasiswa dengan nilai < 70.")
            else:
                print("\nMahasiswa dengan nilai < 70:")
                print("| NIM | Nama | Hadir (%) | Nilai Akhir | Predikat |")
                print("|---|---|---:|---:|:---:|")
                for r in records:
                    print(f"| {r['nim']} | {r['nama']} | {r['hadir']:.1f} | {r['nilai_akhir']:.2f} | {r['predikat']} |")

        elif pilihan == "9":
            records = rk.rekap()
            html = build_html_report(records)
            save_text(OUT_HTML, html)
            print(f"Laporan HTML disimpan ke {OUT_HTML}")

        elif pilihan == "10":
            print("Keluar dari aplikasi.")
            break

        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
