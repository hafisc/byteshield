<div align="center">

# 🛡️ ByteShield

### *Your System's Best Friend* 💪

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/hafisc/byteshield)
[![Python](https://img.shields.io/badge/python-3.7+-brightgreen.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Made with Love](https://img.shields.io/badge/made%20with-❤️-red.svg)](https://github.com/hafisc)

**System Optimizer & Virus Scanner dengan UI Dark Mode yang Aesthetic** ✨

[Features](#-fitur-utama) • [Installation](#-installation) • [Usage](#-cara-pakai) • [Screenshots](#-preview) • [Contributing](#-contributing)

</div>

---

## 🌟 Apa Sih ByteShield?

ByteShield adalah aplikasi **desktop cleaner & antivirus** untuk Windows yang didesain dengan tampilan **modern cyberpunk dark mode**. Cocok buat kamu yang pengen sistem tetap **clean, fast, and secure** tanpa ribet! 

**No bloatware, no ads, just pure optimization** 🚀

---

## ✨ Fitur Utama

### 🧹 **Bersihin Sampah**
Hapus file cache/temp yang cuma buang-buang storage doang. Target:
- `%TEMP%` - User temporary files
- `C:\Windows\Temp` - System temp
- `C:\Windows\Prefetch` - Prefetch cache
- Dan masih banyak lagi!

### 🔍 **Cek Virus**
Quick scan pakai **Windows Defender** tanpa perlu buka Security Center. Tinggal klik, beres!

### ⚡ **Gas Semuanya**
One-click optimize: Clean + Scan sekaligus. Hemat waktu, efisien maksimal.

### 💻 **System Info**
Lihat detail sistem kamu dalam satu dashboard:
- OS Version
- CPU/Processor
- RAM Usage
- Disk Space

### 🎨 **UI/UX Premium**
- **Dark Mode Cyberpunk** theme
- **Sidebar Navigation** yang sleek
- **Terminal-style logs** dengan color coding
- **Hover effects** yang smooth
- **Auto system scan** pas pertama kali buka

---

## 🎯 Kenapa Harus ByteShield?

| Feature | ByteShield | CCleaner | Windows Built-in |
|---------|-----------|----------|------------------|
| 🆓 Free | ✅ | ⚠️ Limited | ✅ |
| 🎨 Modern UI | ✅ | ❌ | ❌ |
| 🚀 Lightweight | ✅ | ❌ | ✅ |
| 🔒 No Ads | ✅ | ❌ | ✅ |
| 💾 One-Click Clean | ✅ | ✅ | ❌ |
| 🔍 Integrated Scan | ✅ | ⚠️ Paid | ⚠️ Separate |

---

## 📦 Installation

### Opsi 1: Download .EXE (Recommended)

1. Download file `.exe` dari [Releases](https://github.com/hafisc/byteshield/releases)
2. Jalankan `ByteShield.exe`
3. Done! ✅

> ⚠️ **Note**: Jalankan sebagai **Administrator** untuk hasil optimal

### Opsi 2: Run from Source

```bash
# Clone repository
git clone https://github.com/hafisc/byteshield.git
cd byteshield

# Install dependencies (optional, untuk info sistem lebih detail)
pip install psutil wmi

# Run aplikasi
python byteshield_gui.py
```

### Opsi 3: Build Sendiri

```bash
# Install PyInstaller
pip install pyinstaller

# Build ke .exe
pyinstaller --onefile --noconsole --name ByteShield byteshield_gui.py

# File .exe ada di folder dist/
```

---

## � Cara Pakai

1. **Buka ByteShield** (jalankan sebagai Admin)
2. **Pilih fitur** di sidebar:
   - 🧹 Bersihin Sampah
   - 🔍 Cek Virus
   - ⚡ Gas Semuanya (Clean + Scan)
   - 💻 System Info (lihat detail sistem)
3. **Watch the magic happen** di terminal output
4. **Done!** Sistem kamu udah bersih ✨

---

## 📸 Preview

> **Coming Soon**: Screenshots akan ditambahkan!

**Features Overview:**
- ✅ Sidebar Navigation
- ✅ Terminal Output dengan color coding
- ✅ System Info Dashboard
- ✅ Progress bar untuk visual feedback
- ✅ Auto system scan saat startup

---

## ⚙️ Tech Stack

- **Language**: Python 3.7+
- **GUI**: Tkinter (built-in)
- **Platform**: Windows 10/11
- **Dependencies**: 
  - Standard library (tkinter, os, shutil, subprocess, threading)
  - Optional: `psutil`, `wmi` (untuk system info lebih detail)

---

## 🐛 Troubleshooting

### Windows Defender tidak ditemukan
- Pastikan Windows Defender aktif
- Jalankan aplikasi sebagai **Administrator**

### System Info menampilkan "Unknown"
Install library tambahan:
```bash
pip install psutil wmi
```

### Beberapa file tidak terhapus
- Normal jika file sedang digunakan
- Tutup aplikasi yang berjalan dulu
- Restart PC lalu coba lagi

---

## 🤝 Contributing

Pull requests are welcome! Untuk perubahan besar, silakan buka issue dulu buat diskusi.

1. Fork this repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 Changelog

### v2.0 (Current)
- ✨ Redesign UI total dengan Dark Mode Cyberpunk theme
- 🎨 Tambah Sidebar Navigation
- 💻 Fitur System Info page yang bisa diklik
- 🚀 Auto system scan saat startup
- ⚡ Hover effects pada semua tombol
- 📝 Terminal dengan color coding yang lebih jelas

### v1.0
- 🎉 Initial release
- 🧹 Basic cleaning functionality
- 🔍 Windows Defender integration

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Hafis**

- GitHub: [@hafisc](https://github.com/hafisc)
- Project Link: [https://github.com/hafisc/byteshield](https://github.com/hafisc/byteshield)

---

## 💖 Support

Kalau projek ini berguna, kasih ⭐ dong! It means a lot 🙏

---

<div align="center">

**Made with ❤️ and lots of ☕**

*Stay Safe, Stay Clean!* 🛡️

</div>
