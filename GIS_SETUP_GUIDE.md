# Panduan Setup Google Places API untuk Loker Tracker

## Overview
Integrasi GIS telah ditambahkan ke aplikasi Loker Tracker untuk memberikan autocomplete lokasi otomatis menggunakan Google Places API. User sekarang dapat mengetik lokasi dengan suggestions yang akurat tanpa perlu mengetik manual.

## Fitur yang Ditambahkan
- ✅ **Autocomplete Lokasi**: Suggestions otomatis saat mengetik nama kota/lokasi
- ✅ **Auto-populate Alamat**: Field alamat akan terisi otomatis saat lokasi dipilih
- ✅ **Data Indonesia**: Dibatasi pada lokasi di Indonesia saja
- ✅ **User-Friendly**: Indikator visual untuk menunjukkan autocomplete tersedia
- ✅ **Database Tidak Berubah**: Semua integrasi dilakukan di frontend

## Cara Mendapatkan Google Places API Key

### Step 1: Buka Google Cloud Console
1. Kunjungi [Google Cloud Console](https://console.cloud.google.com/)
2. Login dengan akun Google Anda
3. Buat project baru atau pilih project yang sudah ada

### Step 2: Enable Google Places API
1. Buka menu **"APIs & Services"** → **"Library"**
2. Cari **"Places API"**
3. Klik pada **"Places API"** → **"Enable"**

### Step 3: Buat API Key
1. Buka menu **"APIs & Services"** → **"Credentials"**
2. Klik **"+ CREATE CREDENTIALS"** → **"API Key"**
3. Copy API key yang muncul

### Step 4: Restrict API Key (Recommended)
1. Klik pada API key yang baru dibuat
2. Di bagian **"Application restrictions"**, pilih **"HTTP referrers"**
3. Tambahkan domain Anda (contoh: `https://yourdomain.com/*`)
4. Di bagian **"API restrictions"**, pilih **"Restrict key"**
5. Centang **"Places API"**
6. Klik **"Save"**

## Konfigurasi di Aplikasi

### Step 1: Update Base Template
Buka file `templates/base.html` dan ganti `YOUR_GOOGLE_PLACES_API_KEY` dengan API key Anda:

```html
<!-- Ganti YOUR_GOOGLE_PLACES_API_KEY dengan API key Anda -->
<script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_PLACES_API_KEY&libraries=places&callback=initGooglePlaces"></script>
```

**Contoh:**
```html
<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB1234567890abcdefghijklmnopqrstuvwxyz&libraries=places&callback=initGooglePlaces"></script>
```

## Testing Fitur GIS

### Test Autocomplete
1. Buka halaman **"Tambah Lamaran"**
2. Klik pada field **"Lokasi"**
3. Mulai ketik nama kota (contoh: "jakarta", "bandung", "surabaya")
4. Anda akan melihat dropdown suggestions muncul
5. Pilih salah satu suggestion
6. Field alamat akan terisi otomatis dengan alamat lengkap

### Test di Halaman Edit
1. Buka halaman **"Edit"** untuk lamaran yang sudah ada
2. Klik pada field **"Lokasi"**
3. Test autocomplete functionality sama seperti di halaman add

## Troubleshooting

### Autocomplete Tidak Muncul
**Kemungkinan Penyebab:**
1. API key belum dikonfigurasi
2. API key tidak valid atau expired
3. Google Places API belum di-enable
4. Quota limit tercapai

**Solusi:**
1. Pastikan API key sudah diganti di `templates/base.html`
2. Check Google Cloud Console untuk memastikan Places API enabled
3. Periksa quota usage di Google Cloud Console
4. Pastikan domain restrictions tidak memblokir akses

### Console Error
**Error: "Google Maps JavaScript API failed to load"**
- API key bermasalah atau belum dikonfigurasi

**Error: "You must use an API key to authenticate each request"**
- API key tidak valid atau tidak memiliki permission

### Suggestions Tidak Relevan
- Google Places API secara default akan memberikan suggestions global
- Filter sudah dikonfigurasi untuk Indonesia (`componentRestrictions: { country: 'id' }`)
- Jika masih ada suggestions tidak relevan, itu normal karena Google Places API mencari berdasarkan pola ketik

## Biaya dan Quota

### Google Places API Pricing
- **Free Tier**: $200 credit per bulan
- **Autocomplete**: $17 per 1000 requests
- **Details**: $32 per 1000 requests (kita tidak menggunakan ini)

### Estimasi Penggunaan
Untuk aplikasi loker tracker:
- **User input lokasi**: Sekitar 5-10 requests per user per bulan
- **Biaya per bulan**: Sekitar $0.08 - $0.17 per user
- **Dengan 100 user**: $8 - $17 per bulan

### Monitoring Usage
1. Buka Google Cloud Console
2. Menu **"APIs & Services"** → **"Quotas"**
3. Filter dengan **"Places API"**
4. Monitor daily usage dan costs

## Keamanan

### API Key Security
- ✅ Selalu restrict API key dengan domain
- ✅ Jangan share API key di public repositories
- ✅ Monitor usage secara regular
- ✅ Set billing alerts untuk mencegah overcharge

### Data Privacy
- Lokasi yang diketik user dikirim ke Google Places API
- Tidak ada data lokasi yang disimpan di server kita
- Hanya data final (hasil pilihan user) yang disimpan di database

## Fitur Lanjutan (Opsional)

### Enhanced Location Data
Jika Anda ingin menyimpan data lokasi lebih detail (koordinat, komponen alamat), bisa ditambahkan:

```javascript
// Extended fields untuk data lokasi yang lebih lengkap
const autocomplete = new google.maps.places.Autocomplete(input, {
    types: ['(cities)'],
    componentRestrictions: { country: 'id' },
    fields: ['formatted_address', 'address_components', 'geometry', 'place_id']
});
```

### Map Picker Integration
Jika ingin menambahkan map picker untuk memilih lokasi secara visual, bisa integrasikan Google Maps JavaScript API.

## Support

Jika ada masalah dengan implementasi GIS:
1. Check browser console untuk error messages
2. Verify API key configuration
3. Test di Google Cloud Console dengan API testing
4. Monitor quota dan billing usage

---

**Catatan**: Implementasi GIS ini tidak mengubah struktur database sama sekali dan backward compatible dengan data existing.
