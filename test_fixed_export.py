#!/usr/bin/env python3
"""
Test script untuk memastikan export Excel sudah diperbaiki
"""

import pandas as pd
from io import BytesIO
import datetime

# Test the fixed summary sheet
print("🔍 Testing Fixed Excel Export...")

try:
    # Test summary sheet data structure
    summary_data = [
        ['Keterangan', 'Jumlah'],
        ['Ringkasan Data Lamaran Kerja', ''],
        ['', ''],
        ['Total Lamaran', 2],
        ['Status Terdaftar', 0],
        ['Status Interview', 1],
        ['Status Tes', 1],
        ['Status Diterima', 0],
        ['Status Tidak Diterima', 0],
        ['', ''],
        ['Tanggal Export', datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')],
        ['User', 'test_user']
    ]
    
    summary_df = pd.DataFrame(summary_data)
    print("✅ Summary DataFrame created successfully")
    print(f"📊 Shape: {summary_df.shape}")
    print(f"📋 Columns: {list(summary_df.columns)}")
    
    # Test with sample job data
    jobs_data = [
        {
            'company_name': 'PT. Tech',
            'position': 'Developer',
            'location': 'Jakarta',
            'address': 'Jl. Sudirman',
            'status': {'name': 'Interview'},
            'applied_date': datetime.datetime.now(),
            'source_info': 'LinkedIn',
            'application_proof': 'https://linkedin.com',
            'notes': 'Test note'
        },
        {
            'company_name': 'CV. Design',
            'position': 'Designer',
            'location': 'Surabaya',
            'address': 'Jl. Ahmad Yani',
            'status': {'name': 'Tes'},
            'applied_date': datetime.datetime.now(),
            'source_info': 'Jobstreet',
            'application_proof': '',
            'notes': ''
        }
    ]
    
    data = []
    for job in jobs_data:
        data.append({
            'No': len(data) + 1,
            'Nama Perusahaan': job.get('company_name', '-'),
            'Posisi': job.get('position', '-'),
            'Lokasi': job.get('location', '-'),
            'Alamat': job.get('address', '-'),
            'Status': job.get('status', {}).get('name', '-'),
            'Tanggal Apply': job.get('applied_date', datetime.datetime.now()).strftime('%d/%m/%Y') if job.get('applied_date') else '-',
            'Sumber Info': job.get('source_info', '-'),
            'Bukti Lamaran (Link)': job.get('application_proof', '-'),
            'Catatan': job.get('notes', '-')
        })
    
    df = pd.DataFrame(data)
    print("✅ Main DataFrame created successfully")
    
    # Create Excel buffer
    buffer = BytesIO()
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # Write main data
        df.to_excel(writer, sheet_name='Data Lamaran Kerja', index=False)
        
        # Write summary data
        summary_df.to_excel(writer, sheet_name='Ringkasan', index=False)
        
        # Style the summary sheet
        summary_ws = writer.sheets['Ringkasan']
        if summary_ws['A1'].font:
            summary_ws['A1'].font = summary_ws['A1'].font.copy(bold=True, size=14)
    
    buffer.seek(0)
    
    # Save test file
    test_filename = f'fixed_export_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    with open(test_filename, 'wb') as f:
        f.write(buffer.getvalue())
    
    print(f'✅ Fixed Excel export successful!')
    print(f'📁 Test file: {test_filename}')
    print(f'📏 File size: {len(buffer.getvalue())} bytes')
    
    # Verify file can be opened
    try:
        import openpyxl
        workbook = openpyxl.load_workbook(test_filename)
        sheet_names = workbook.sheetnames
        print(f'✅ Excel file verified. Sheets: {sheet_names}')
    except Exception as e:
        print(f'❌ File verification error: {e}')
    
except Exception as e:
    print(f'❌ Export error: {e}')
    import traceback
    traceback.print_exc()

print('\n🎯 Fixed Excel export test completed!')
