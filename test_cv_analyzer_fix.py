#!/usr/bin/env python3
"""
Test untuk memverifikasi perbaikan CVAnalyzer.analyze_cv() missing argument
"""

import sys
import os
import tempfile
import traceback
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, '/Users/marianaulfahhoesny/Documents/PORTOFOLIO WEB/loker-tracker')

def test_cv_analyzer_method_signature():
    """Test untuk memastikan method signature CVAnalyzer.analyze_cv()"""
    try:
        from ai_modules.cv_analyzer import CVAnalyzer
        
        cv_analyzer = CVAnalyzer()
        
        # Check method exists
        assert hasattr(cv_analyzer, 'analyze_cv'), "Method analyze_cv tidak ditemukan"
        
        # Check method signature
        import inspect
        sig = inspect.signature(cv_analyzer.analyze_cv)
        params = list(sig.parameters.keys())
        
        print(f"✅ Method signature: {sig}")
        print(f"✅ Parameters: {params}")
        
        # Should have: self, file_path, file_size
        assert 'file_path' in params, "Parameter 'file_path' tidak ditemukan"
        assert 'file_size' in params, "Parameter 'file_size' tidak ditemukan"
        
        print("✅ Method signature CVAnalyzer.analyze_cv() CORRECT")
        return True
        
    except Exception as e:
        print(f"❌ Error checking method signature: {str(e)}")
        traceback.print_exc()
        return False

def test_cv_analyzer_with_correct_params():
    """Test CVAnalyzer dengan parameter yang benar"""
    try:
        from ai_modules.cv_analyzer import CVAnalyzer
        
        cv_analyzer = CVAnalyzer()
        
        # Create a temporary CV file
        cv_content = """
        John Doe
        Email: john.doe@email.com
        Phone: +1234567890
        
        Experience:
        - Software Engineer at Tech Corp (2020-2023)
        - Junior Developer at Startup Inc (2018-2020)
        
        Skills:
        - Python
        - JavaScript
        - React
        - Node.js
        - SQL
        
        Education:
        - Bachelor of Computer Science, University of Technology (2018)
        """
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(cv_content)
            temp_file_path = f.name
        
        try:
            # Test dengan parameter yang benar: file_path dan file_size
            file_size = len(cv_content)
            print(f"📝 Testing CVAnalyzer.analyze_cv() dengan:")
            print(f"   - file_path: {temp_file_path}")
            print(f"   - file_size: {file_size}")
            
            # Call method dengan parameter yang benar
            result = cv_analyzer.analyze_cv(temp_file_path, file_size)
            
            print(f"✅ CVAnalyzer.analyze_cv() berhasil dipanggil!")
            print(f"✅ Result type: {type(result)}")
            
            # Check if result contains expected keys
            expected_keys = ['extracted_skills', 'experience_level', 'education_level', 'ats_score', 'completeness_score']
            for key in expected_keys:
                if key in result:
                    print(f"✅ Result contains '{key}': {result[key]}")
                else:
                    print(f"⚠️  Result missing '{key}'")
            
            print("✅ CVAnalyzer.analyze_cv() bekerja dengan parameter yang benar!")
            return True
            
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)
        
    except Exception as e:
        print(f"❌ Error testing CVAnalyzer dengan parameter benar: {str(e)}")
        traceback.print_exc()
        return False

def test_cv_analyzer_with_wrong_params():
    """Test CVAnalyzer dengan parameter yang salah (seperti sebelum perbaikan)"""
    try:
        from ai_modules.cv_analyzer import CVAnalyzer
        
        cv_analyzer = CVAnalyzer()
        
        cv_content = "Test CV content"
        
        print("🧪 Testing CVAnalyzer.analyze_cv() dengan parameter salah (seperti sebelum perbaikan)...")
        
        try:
            # Ini akan gagal karena hanya memberikan 1 parameter
            result = cv_analyzer.analyze_cv(cv_content)
            print("❌ Unexpected: Method berhasil dipanggil dengan parameter salah!")
            return False
        except TypeError as e:
            print(f"✅ Expected error terjadi: {str(e)}")
            print("✅ Ini menunjukkan bahwa method benar-benar membutuhkan 2 parameter")
            return True
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        traceback.print_exc()
        return False

def test_app_py_integration():
    """Test integrasi di app.py setelah perbaikan"""
    try:
        print("🔗 Testing integrasi di app.py...")
        
        # Check if app.py contains the correct call
        app_py_path = '/Users/marianaulfahhoesny/Documents/PORTOFOLIO WEB/loker-tracker/app.py'
        
        with open(app_py_path, 'r') as f:
            content = f.read()
        
        # Check for the corrected line
        if 'cv_analyzer.analyze_cv(file_path, len(cv_content))' in content:
            print("✅ app.py contains correct method call: cv_analyzer.analyze_cv(file_path, len(cv_content))")
            return True
        elif 'cv_analyzer.analyze_cv(cv_content)' in content:
            print("❌ app.py still contains old method call: cv_analyzer.analyze_cv(cv_content)")
            return False
        else:
            print("⚠️  Could not find method call in app.py")
            return False
        
    except Exception as e:
        print(f"❌ Error checking app.py integration: {str(e)}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 TESTING CVANALYZER.ANALYZE_CV() FIX")
    print("=" * 50)
    print(f"📅 Test date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Method Signature Check", test_cv_analyzer_method_signature),
        ("Correct Parameters Test", test_cv_analyzer_with_correct_params),
        ("Wrong Parameters Test", test_cv_analyzer_with_wrong_params),
        ("App.py Integration Check", test_app_py_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
                
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print(f"\n📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! CVAnalyzer.analyze_cv() fix is working correctly!")
    else:
        print("⚠️  Some tests failed. Please review the results above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
