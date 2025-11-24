# 🛡️ ByteShield - System Cleaner & Virus Scanner

**Aplikasi desktop Windows untuk membersihkan file sampah dan scan virus**

Author: Hafis  
Version: 1.0  
Platform: Windows 10/11

---

## 📋 Fitur Utama

✅ **Pembersihan File Sampah**
- Membersihkan folder TEMP dan TMP
- Membersihkan Windows\Temp
- Membersihkan Windows\Prefetch
- Log detail file yang dihapus

✅ **Windows Defender Quick Scan**
- Menjalankan quick scan antivirus bawaan Windows
- Deteksi otomatis lokasi MpCmdRun.exe
- Status scan real-time

✅ **Mode Gabungan**
- Bersihkan + Scan dalam satu klik
- Otomatis menjalankan kedua proses berurutan

✅ **GUI Modern**
- Antarmuka user-friendly dengan Tkinter
- Log proses real-time dengan color coding
- Progress bar untuk feedback visual
- Threading untuk mencegah freeze

---

## 🚀 Cara Menggunakan

### Opsi 1: Jalankan Script Python

```bash
python byteshield_gui.py
```

> **Note**: Jalankan sebagai Administrator untuk hasil optimal

### Opsi 2: Build ke .EXE

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build aplikasi (tanpa console):
```bash
pyinstaller --onefile --noconsole --name ByteShield byteshield_gui.py
```

3. File .exe akan ada di folder `dist/`

4. (Opsional) Tambahkan icon custom:
```bash
pyinstaller --onefile --noconsole --icon=icon.ico --name ByteShield byteshield_gui.py
```

---

## 📁 Folder yang Dibersihkan

ByteShield akan membersihkan folder-folder berikut:

| Folder | Deskripsi |
|--------|-----------|
| `%TEMP%` | Folder temporary user |
| `%TMP%` | Folder temporary sistem |
| `C:\Windows\Temp` | Folder temporary Windows |
| `C:\Windows\Prefetch` | File prefetch aplikasi |

---

## 🎨 Screenshot GUI

Aplikasi ini memiliki:
- **Header** dengan logo dan nama aplikasi
- **3 Tombol utama** untuk fitur berbeda
- **Progress bar** untuk visual feedback
- **Log area** dengan color coding:
  - 🟢 **Hijau** = Informasi
  - 🟡 **Kuning** = Warning
  - 🔴 **Merah** = Error
  - 🟢 **Hijau Bold** = Success

---

## ⚙️ Requirements

- **Python**: 3.7 atau lebih baru
- **OS**: Windows 10/11
- **Library**: Hanya standard library (tkinter, os, shutil, subprocess, threading, pathlib)
- **Admin Rights**: Direkomendasikan untuk pembersihan optimal

---

## 🔧 Troubleshooting

### Windows Defender tidak ditemukan
- Pastikan Windows Defender terinstall
- Jalankan aplikasi sebagai Administrator
- Cek apakah antivirus pihak ketiga tidak menonaktifkan Defender

### Beberapa file tidak terhapus
- Normal jika beberapa file sedang digunakan oleh sistem
- Tutup aplikasi yang sedang berjalan
- Restart komputer lalu coba lagi

### GUI freeze
- Ini tidak seharusnya terjadi (sudah ada threading)
- Jika terjadi, tunggu proses selesai atau restart aplikasi

---

## 📝 Catatan Penting

⚠️ **Peringatan:**
- Aplikasi ini akan **menghapus permanent** file di folder temp
- Pastikan tidak ada file penting di folder tersebut
- Selalu **backup** data penting sebelum membersihkan

✅ **Tips:**
- Jalankan pembersihan secara berkala (mingguan)
- Tutup aplikasi lain sebelum membersihkan
- Scanning virus akan lebih efektif jika Windows Defender up-to-date

---

## 📄 License

Free to use and modify.

---

## 👨‍💻 Developer

Created with ❤️ by **Hafis**

Jika ada bug atau saran, silakan hubungi developer!
