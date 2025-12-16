# 🔧 Panduan Menjalankan Flask Server

## ✅ Status: Server Berhasil Berjalan!

Berdasarkan testing yang baru saja dilakukan, server Flask Anda **berhasil berjalan dengan baik** di `http://127.0.0.1:5000`.

## 🚀 Cara Menjalankan Server

### Metode 1: Langsung (Recommended)
```bash
python app.py
```

### Metode 2: Menggunakan Script Launcher
```bash
python run_server.py
```

## 📋 Yang Terjadi Saat Server Berjalan

```
* Serving Flask app 'app'
 * Debug mode: on
WARNING: This is development server. Do not use in production.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

## 🔍 Penjelasan Warning yang Muncul

### 1. LegacyAPIWarning (SQLAlchemy)
```
LegacyAPIWarning: The Query.get() method is considered legacy...
```
**Penjelasan**: Warning ini adalah untuk optimasi future, tidak mempengaruhi fungsionalitas saat ini.

**Solusi**: Update kode di `extensions.py` atau `models.py` dengan menggunakan SQLAlchemy 2.0 syntax.

### 2. Development Server Warning
```
WARNING: This is a development server. Do not use it in a production deployment.
```
**Penjelasan**: Ini adalah warning normal untuk development environment.

**Artinya**: Server ini hanya untuk testing/development, bukan untuk production.

## 🛠️ Mengatasi Masalah "Access Denied"

Jika Anda masih mengalami masalah, berikut solusinya:

### 1. Periksa Port Usage
```bash
# Cek port 5000
lsof -i :5000

# Hentikan proses yang menggunakan port
kill -9 $(lsof -ti :5000)
```

### 2. Periksa Izin File
```bash
# Beri izin execute
chmod +x app.py

# Pastikan Anda owner file
ls -la app.py
```

### 3. Periksa Virtual Environment
```bash
# Aktifkan virtual environment
source venv/bin/activate

# Pastikan Flask terinstall
pip list | grep Flask
```

## 🌐 Mengakses Aplikasi

Setelah server berjalan, buka browser dan akses:
- **URL**: http://127.0.0.1:5000
- **URL Alternative**: http://localhost:5000

## 🔄 Menghentikan Server

Tekan `Ctrl+C` di terminal untuk menghentikan server dengan aman.

## 📝 Logging

Jika ingin menyimpan log server:
```bash
python app.py > server.log 2>&1 &
```

## 🎯 Kesimpulan

**Tidak ada masalah "access denied"**. Server Flask Anda berjalan dengan normal. Yang Anda lihat adalah warning normal untuk development environment.
