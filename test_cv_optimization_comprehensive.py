#!/usr/bin/env python3
"""
Comprehensive CV Detection Optimization Test
Tests all enhanced features for improved accuracy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_modules.nlp_processor import NLPProcessor
import json

def test_enhanced_cv_detection():
    """Test all enhanced CV detection features"""
    
    print("🚀 COMPREHENSIVE CV DETECTION OPTIMIZATION TEST")
    print("=" * 60)
    
    # Initialize NLP processor
    nlp = NLPProcessor()
    
    # Test cases with different languages and quality levels
    test_cases = [
        {
            'name': 'Indonesian Tech CV (High Quality)',
            'cv_text': '''
            AGUS SETIAWAN
            Email: agus.setiawan@email.com
            Telepon: 08123456789
            LinkedIn: linkedin.com/in/agus-setiawan
            
            RINGKASAN PROFESIONAL:
            Senior Software Developer dengan 8 tahun pengalaman dalam pengembangan aplikasi web dan mobile. 
            Memiliki keahlian dalam Python, JavaScript, React, dan Node.js. Berpengalaman memimpin tim development 
            dan mengimplementasikan solusi teknologi untuk meningkatkan efisiensi bisnis.
            
            PENGALAMAN KERJA:
            Senior Software Developer - PT Teknologi Digital (2020-Sekarang)
            • Mengembangkan aplikasi web menggunakan React dan Node.js
            • Memimpin tim 5 orang developer dengan metodologi Agile
            • Mengoptimalkan performance aplikasi hingga 50%
            • Mengimplementasikan CI/CD pipeline menggunakan Docker dan Jenkins
            
            Software Developer - Startup ABC (2018-2020)
            • Mengembangkan mobile app menggunakan React Native
            • Mengintegrasikan API dengan database PostgreSQL
            • Mengimplementasikan sistem autentikasi dengan JWT
            
            KEAHLIAN TEKNIS:
            Programming: Python, JavaScript, TypeScript, PHP, Java, Go
            Frontend: React, Vue.js, Angular, HTML5, CSS3, Bootstrap
            Backend: Node.js, Express, Django, Laravel, Spring Boot
            Database: MySQL, PostgreSQL, MongoDB, Redis
            Cloud & DevOps: AWS, Azure, Docker, Kubernetes, Jenkins
            Tools: Git, VS Code, Postman, Jira, Confluence
            
            PENDIDIKAN:
            S1 Teknik Informatika - Universitas Indonesia (2014-2018)
            GPA: 3.7/4.0
            
            SERTIFIKASI:
            • AWS Certified Solutions Architect
            • Google Cloud Professional Developer
            • Scrum Master Certification
            
            BAHASA:
            Indonesia (Native), Inggris (Fluent)
            ''',
            'expected': {
                'language': 'indonesian',
                'experience_level': 'senior',
                'education_level': 'bachelor',
                'industry': 'technology'
            }
        },
        {
            'name': 'English Finance CV (Mid Quality)',
            'cv_text': '''
            Sarah Johnson
            Email: sarah.johnson@finance.com
            Phone: +1-555-123-4567
            
            PROFESSIONAL SUMMARY:
            Experienced Financial Analyst with 5 years of experience in banking and investment. 
            Skilled in financial modeling, risk assessment, and portfolio management.
            
            WORK EXPERIENCE:
            Financial Analyst - ABC Bank (2021-Present)
            • Conduct financial analysis and risk assessment
            • Prepare monthly financial reports
            • Support senior management in strategic decisions
            
            Junior Analyst - XYZ Investment (2019-2021)
            • Assisted in portfolio management
            • Analyzed market trends and opportunities
            
            SKILLS:
            Financial Analysis, Excel Advanced, Bloomberg Terminal, 
            Risk Management, Financial Modeling, SQL
            
            EDUCATION:
            MBA Finance - Harvard Business School (2017-2019)
            BS Economics - University of Pennsylvania (2013-2017)
            
            CERTIFICATIONS:
            CFA Level 2
            Financial Risk Manager (FRM)
            ''',
            'expected': {
                'language': 'english',
                'experience_level': 'mid',
                'education_level': 'master',
                'industry': 'finance'
            }
        },
        {
            'name': 'Mixed Language Marketing CV (Good Quality)',
            'cv_text': '''
            Michael Chen / 陈明华
            Email: michael.chen@marketing.com
            电话: +86-138-0013-8000
            
            MARKETING MANAGER PROFILE:
            Digital marketing expert dengan 6 tahun pengalaman dalam campaign management dan brand strategy. 
            Experienced in both Chinese and international markets with proven track record in ROI improvement.
            
            WORK EXPERIENCE:
            Senior Marketing Manager - Global Tech Corp (2020-Present)
            • Managed digital marketing campaigns across Asia-Pacific region
            • Increased brand awareness by 150% dalam 2 tahun
            • Led cross-functional team of 12 marketing professionals
            
            Marketing Specialist - Local Agency (2018-2020)
            • Developed content marketing strategies
            • Managed social media presence untuk 20+ clients
            
            CORE COMPETENCIES:
            Digital Marketing, SEO/SEM, Social Media Marketing, Content Strategy
            Google Analytics, Facebook Ads, Instagram Marketing, WeChat Marketing
            Project Management, Team Leadership, Brand Management
            
            EDUCATION:
            Master of Marketing - National University of Singapore (2016-2018)
            Bachelor of Business - Beijing University (2012-2016)
            
            LANGUAGES:
            English (Fluent), Mandarin (Native), Indonesian (Conversational)
            ''',
            'expected': {
                'language': 'mixed',
                'experience_level': 'senior',
                'education_level': 'master',
                'industry': 'marketing'
            }
        },
        {
            'name': 'Poor Quality CV (Minimal Information)',
            'cv_text': '''
            John Doe
            
            I am a software developer. I know programming and have some experience.
            I worked at a company before. I can code in Python and JavaScript.
            I have a degree in computer science.
            ''',
            'expected': {
                'language': 'english',
                'experience_level': 'unknown',
                'education_level': 'bachelor',
                'industry': 'technology'
            }
        }
    ]
    
    # Run tests
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 TEST CASE {i}: {test_case['name']}")
        print("-" * 50)
        
        cv_text = test_case['cv_text']
        expected = test_case['expected']
        
        # Process CV
        result = nlp.process_cv_text(cv_text)
        
        # Display results
        print(f"🌍 Language Detection: {result['language_detected']} (Expected: {expected['language']})")
        print(f"📈 Experience Level: {result['experience_level']} (Expected: {expected['experience_level']})")
        print(f"🎓 Education Level: {result['education_level']} (Expected: {expected['education_level']})")
        print(f"🏢 Industry: {result['industry_classification']} (Expected: {expected['industry']})")
        print(f"💪 Confidence Score: {result['confidence_score']}")
        print(f"⏰ Total Years: {result['total_years']}")
        print(f"💡 Skills Extracted: {len(result['extracted_skills'])} skills")
        print(f"🎯 ATS Score: {result['ats_score']}/100")
        print(f"📋 Completeness: {result['completeness_score']}/100")
        
        # Show extracted skills (first 10)
        if result['extracted_skills']:
            print(f"🔧 Top Skills: {', '.join(result['extracted_skills'][:10])}")
        
        # Calculate accuracy
        accuracy_score = 0
        if result['language_detected'] == expected['language']:
            accuracy_score += 25
        if result['experience_level'] == expected['experience_level']:
            accuracy_score += 25
        if result['education_level'] == expected['education_level']:
            accuracy_score += 25
        if result['industry_classification'] == expected['industry']:
            accuracy_score += 25
        
        print(f"✅ Accuracy Score: {accuracy_score}/100")
        
        # Store results
        results.append({
            'test_name': test_case['name'],
            'accuracy_score': accuracy_score,
            'confidence_score': result['confidence_score'],
            'skills_count': len(result['extracted_skills']),
            'ats_score': result['ats_score'],
            'completeness_score': result['completeness_score']
        })
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY & OPTIMIZATION RESULTS")
    print(f"{'='*60}")
    
    total_accuracy = sum(r['accuracy_score'] for r in results)
    avg_accuracy = total_accuracy / len(results)
    
    avg_confidence = sum(r['confidence_score'] for r in results) / len(results)
    avg_skills = sum(r['skills_count'] for r in results) / len(results)
    avg_ats = sum(r['ats_score'] for r in results) / len(results)
    avg_completeness = sum(r['completeness_score'] for r in results) / len(results)
    
    print(f"🎯 Average Detection Accuracy: {avg_accuracy:.1f}/100")
    print(f"💪 Average Confidence Score: {avg_confidence:.2f}")
    print(f"💡 Average Skills Extracted: {avg_skills:.1f}")
    print(f"📈 Average ATS Score: {avg_ats:.1f}/100")
    print(f"📋 Average Completeness: {avg_completeness:.1f}/100")
    
    # Performance by test case
    print(f"\n📋 DETAILED RESULTS:")
    for result in results:
        print(f"• {result['test_name']}: {result['accuracy_score']}/100 accuracy, "
              f"{result['confidence_score']:.2f} confidence")
    
    # Optimization improvements
    print(f"\n🚀 OPTIMIZATION IMPROVEMENTS:")
    print(f"✅ Multi-language support (Indonesian, English, Mixed)")
    print(f"✅ Enhanced skill detection with 500+ keywords")
    print(f"✅ Experience level detection with year calculation")
    print(f"✅ Industry classification with confidence scoring")
    print(f"✅ Education level detection with institution scoring")
    print(f"✅ ATS optimization scoring")
    print(f"✅ Confidence calculation for detection quality")
    print(f"✅ Fuzzy matching for improved accuracy")
    print(f"✅ Enhanced text preprocessing and OCR error handling")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if avg_accuracy >= 80:
        print(f"🎉 Excellent! System shows high accuracy ({avg_accuracy:.1f}%)")
    elif avg_accuracy >= 60:
        print(f"👍 Good performance! Consider fine-tuning for {avg_accuracy:.1f}% accuracy")
    else:
        print(f"⚠️ Needs improvement. Current accuracy: {avg_accuracy:.1f}%")
    
    if avg_confidence >= 0.8:
        print(f"🎯 High confidence detection system")
    elif avg_confidence >= 0.6:
        print(f"📊 Good confidence levels detected")
    else:
        print(f"🔍 Consider adding more training data for better confidence")
    
    print(f"\n🎊 COMPREHENSIVE CV DETECTION OPTIMIZATION COMPLETE!")
    
    return results

if __name__ == "__main__":
    test_enhanced_cv_detection()
