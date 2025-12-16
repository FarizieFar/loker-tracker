#!/usr/bin/env python3
"""
Script untuk menjalankan Flask server dengan penanganan error yang lebih baik
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

def kill_existing_processes():
    """Hentikan proses Flask yang sedang berjalan"""
    try:
        # Hentikan proses yang menggunakan port 5000
        result = subprocess.run(['lsof', '-ti', ':5000'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGTERM)
                    print(f"Berhentiin proses {pid}")
                    time.sleep(1)
                except ProcessLookupError:
                    pass
    except FileNotFoundError:
        print("lsof tidak ditemukan, lewati penghentian proses")

def check_port():
    """Periksa apakah port 5000 sudah digunakan"""
    try:
        result = subprocess.run(['lsof', '-i', ':5000'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("❌ Port 5000 sedang digunakan!")
            print("Proses yang menggunakan port:")
            print(result.stdout)
            return False
        else:
            print("✅ Port 5000 tersedia")
            return True
    except FileNotFoundError:
        print("⚠️  lsof tidak ditemukan, tidak dapat memeriksa port")
        return True

def check_permissions():
    """Periksa izin file dan direktori"""
    current_dir = Path.cwd()
    
    # Periksa izin direktori saat ini
    if not os.access(current_dir, os.R_OK | os.W_OK | os.X_OK):
        print("❌ Tidak ada izin write di direktori saat ini")
        return False
    
    # Periksa izin file app.py
    app_file = current_dir / "app.py"
    if not app_file.exists():
        print("❌ File app.py tidak ditemukan")
        return False
    
    if not os.access(app_file, os.R_OK):
        print("❌ Tidak ada izin read untuk app.py")
        return False
    
    print("✅ Izin file dan direktori OK")
    return True

def setup_environment():
    """Setup environment yang diperlukan"""
    # Pastikan virtual environment aktif
    venv_path = Path.cwd() / "venv"
    if venv_path.exists():
        print("✅ Virtual environment ditemukan")
    else:
        print("⚠️  Virtual environment tidak ditemukan")

def run_flask_server():
    """Jalankan Flask server"""
    try:
        print("\n🚀 Memulai Flask server...")
        print("=" * 50)
        
        # Set environment variables
        env = os.environ.copy()
        env['FLASK_APP'] = 'app.py'
        env['FLASK_ENV'] = 'development'
        
        # Jalankan Flask
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print("✅ Flask server dimulai!")
        print("🌐 Server berjalan di: http://127.0.0.1:5000")
        print("⏹️  Tekan Ctrl+C untuk menghentikan server")
        print("=" * 50)
        
        # Tampilkan output server
        try:
            for line in process.stdout:
                print(line.rstrip())

        except KeyboardInterrupt:
            print("\n\n⏹️  Menghentikan server...")
            process.terminate()
            process.wait()
            print("✅ Server berhasil dihentikan")
    except Exception as e:
        print(f"❌: {e}")
        return False
    
    return True

def main():
    """Fungsi utama"""
    print("🔧 Flask Server Launcher")
    print("=" * 50)
    
    # Periksa dan perbaiki masalah
    if not check_permissions():
        print("\n💡 Solusi:")
        print("1. Pastikan Anda berada di direktori yang benar")
        print("2. Periksa izin file dengan: chmod +x app.py")
        return
    
    if not check_port():
        print("\n💡 Solusi untuk masalah port:")
        print("1. Tunggu sebentar agar proses selesai")
        print("2. Restart komputer jika perlu")
        print("3. Gunakan port lain dengan mengubah app.py")
        return
    
    setup_environment()
    
    # Hentikan proses existing
    kill_existing_processes()
    
    # Jalankan server
    run_flask_server()

if __name__ == "__main__":
    main()
