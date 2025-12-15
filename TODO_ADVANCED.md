# Plan Implementasi Fitur Advanced Loker Tracker

## 📋 Informasi yang Dikumpulkan
- Aplikasi Flask dengan database SQLite sudah ada
- Perlu menambah 4 fitur advanced: export, redesign tabel, logo perusahaan, dan notes
- Harus menggunakan font Poppins dan warna yang tidak berlebih

## 🎯 Plan Detail Implementasi

### 1. **EXPORT FEATURES (PDF & Excel)**
   - **Dependencies**: Install `reportlab` untuk PDF dan `openpyxl` untuk Excel
   - **Routes**: Buat `/export/pdf` dan `/export/excel` 
   - **Templates**: PDF template dengan layout profesional
   - **Buttons**: Tambahkan export buttons di dashboard
   - **Format**: Include semua data (company, position, status, date, dll)

### 2. **TABLE REDESIGN + POPPINS FONT**
   - **Font**: Update Google Fonts ke Poppins
   - **Color Scheme**: Warna subtle dan profesional (biru-abu-abu)
   - **Typography**: Better hierarchy dengan Poppins weights
   - **Spacing**: Optimize padding dan margins
   - **Visual**: Clean, modern, tidak berlebihan

### 3. **COMPANY LOGO FEATURE**
   - **Database**: Tambah field `logo_url` (VARCHAR(255))
   - **Form**: Input field untuk logo URL (optional)
   - **Display**: Logo di tabel dengan fallback initials
   - **Modal**: Preview logo dalam modal khusus
   - **Styling**: Logo dengan border radius dan shadow

### 4. **ADDITIONAL NOTES FIELD**
   - **Database**: Tambah field `notes` (TEXT, nullable)
   - **Form**: Textarea untuk notes (tidak wajib)
   - **Display**: Notes di tabel dengan styling yang rapi
   - **Limit**: Truncate jika terlalu panjang dengan expand option

## 📁 Files yang Akan Diedit/Created:
1. `models.py` - Tambah field logo_url dan notes
2. `app.py` - Routes untuk export PDF/Excel + handle fields baru
3. `templates/add.html` - Input logo URL + notes textarea
4. `templates/edit.html` - Edit logo URL + notes textarea  
5. `templates/index.html` - Display logo + notes + export buttons
6. `static/style.css` - Poppins font + redesign tabel
7. `templates/pdf_report.html` - PDF template (NEW)
8. `requirements.txt` - Tambah dependencies export

## 🔄 Follow-up Steps:
1. Install dependencies (reportlab, openpyxl)
2. Generate database migration
3. Create PDF template dengan layout profesional
4. Test export functionality
5. Implement redesign dengan Poppins font
6. Test responsiveness dan user experience

---
**Status**: Menunggu konfirmasi user untuk proceed
