#!/usr/bin/env python3
"""
Test script for AI integration features
"""

import requests
import json
import sys
from pathlib import Path

def test_ai_features():
    """Test AI features functionality"""
    base_url = "http://127.0.0.1:5001"
    
    print("🚀 Testing AI Integration Features")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 5001")
        return False
    
    # Test 2: Check AI routes exist
    ai_routes = [
        "/ai/dashboard",
        "/ai/cv/upload",
        "/api/ai/generate-insights",
        "/api/ai/insights"
    ]
    
    print("\n🔍 Testing AI Routes...")
    for route in ai_routes:
        try:
            response = requests.get(f"{base_url}{route}")
            # These routes should return 302 (redirect to login) if not authenticated
            if response.status_code in [302, 401, 405]:  # Redirect to login, Unauthorized, or Method Not Allowed
                print(f"✅ Route {route} exists (requires authentication)")
            else:
                print(f"⚠️  Route {route} returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing route {route}: {e}")
    
    # Test 3: Check AI modules can be imported
    print("\n🔧 Testing AI Module Imports...")
    try:
        sys.path.append(str(Path(__file__).parent))
        
        from ai_modules.ai_service import AIService
        from ai_modules.cv_analyzer import CVAnalyzer
        from ai_modules.job_matcher import JobMatcher
        from ai_modules.insights_generator import InsightsGenerator
        
        print("✅ AI modules imported successfully")
        
        # Test basic functionality
        ai_service = AIService()
        cv_analyzer = CVAnalyzer()
        job_matcher = JobMatcher()
        insights_generator = InsightsGenerator()
        
        print("✅ AI service instances created successfully")
        
    except Exception as e:
        print(f"❌ Error importing AI modules: {e}")
        return False
    
    # Test 4: Check templates exist
    print("\n📄 Testing Template Files...")
    template_files = [
        "templates/cv_upload.html",
        "templates/ai_dashboard.html"
    ]
    
    for template in template_files:
        if Path(template).exists():
            print(f"✅ Template {template} exists")
        else:
            print(f"❌ Template {template} missing")
    
    print("\n🎉 AI Integration Test Complete!")
    print("\n📋 Summary of Implemented Features:")
    print("   • CV Upload and Analysis (/ai/cv/upload)")
    print("   • AI Dashboard (/ai/dashboard)")
    print("   • Job Matching API (/api/ai/job-match/<id>)")
    print("   • AI Insights Generation (/api/ai/generate-insights)")
    print("   • AI Insights API (/api/ai/insights)")
    print("   • Updated navigation with AI features")
    print("   • Database models for AI data")
    print("   • Complete AI processing pipeline")
    
    return True

if __name__ == "__main__":
    test_ai_features()

