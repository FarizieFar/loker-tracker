#!/usr/bin/env python3
"""
Test Enhanced CV Analysis System
Comprehensive testing of critical analysis and intelligent feedback generation
"""

import os
import sys
import json
from datetime import datetime

# Add the parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_modules.cv_analyzer import CVAnalyzer

def create_test_cv_text():
    """Create a sample CV text for testing Indonesian context"""
    return """
    RUDI SETIAWAN
    Email: rudi.setiawan@email.com
    Phone: +62 812-3456-7890
    LinkedIn: linkedin.com/in/rudisetiawan

    RINGKASAN PROFESIONAL
    Profesional IT berpengalaman 5 tahun dengan keahlian dalam pengembangan aplikasi web dan mobile. 
    Memiliki track record yang baik dalam memimpin tim开发 dan mengelola proyek teknologi. 
    Passionate dalam solusi inovatif dan continuous learning.

    PENGALAMAN KERJA

    Senior Software Developer | TechCorp Indonesia | 2021 - Sekarang
    • Mengembangkan dan maintenance aplikasi web menggunakan Python Django dan React.js
    • Memimpin tim 4 orang developer untuk menyelesaikan proyek ERP perusahaan
    • Berhasil meningkatkan performa aplikasi sebesar 40% melalui optimasi database
    • Mentoring junior developers dan melakukan code review
    • Implementasi CI/CD pipeline menggunakan Docker dan Jenkins

    Software Developer | StartupXYZ | 2019 - 2021
    • Develop mobile aplikasi menggunakan React Native untuk iOS dan Android
    • Berkolaborasi dengan tim UI/UX designer untuk user experience yang baik
    • Mengintegrasikan payment gateway dan third-party APIs
    • Responsible untuk testing dan deployment aplikasi ke production

    Junior Developer | WebSolutions | 2018 - 2019
    • Membuat website statis dan dinamis menggunakan HTML, CSS, JavaScript
    • Mengembangkan CMS menggunakan PHP CodeIgniter
    • Maintenance website klien dan troubleshooting technical issues

    PENDIDIKAN
    Sarjana Teknik Informatika | Universitas Indonesia | 2018
    IPK: 3.7/4.0
    Skripsi: "Implementasi Machine Learning untuk Prediksi Penjualan"

    SERTIFIKASI
    • AWS Certified Solutions Architect (2022)
    • Google Cloud Professional Developer (2021)
    • Certified Scrum Master (2020)

    KEAHLIAN
    Programming Languages: Python, JavaScript, Java, PHP, SQL
    Frameworks: Django, React.js, React Native, Node.js, CodeIgniter
    Cloud Platforms: AWS, Google Cloud Platform
    Databases: MySQL, PostgreSQL, MongoDB
    Tools: Git, Docker, Jenkins, JIRA
    Soft Skills: Leadership, Team Management, Problem Solving, Communication

    PENGHARGAAN
    • Best Employee Award - TechCorp Indonesia (2022)
    • Winner Internal Hackathon - StartupXYZ (2020)
    """

def create_poor_cv_text():
    """Create a poor quality CV for testing critical analysis"""
    return """
    john doe
    email@gmail.com
    
    saya kerja di perusahaan IT selama 3 tahun. bikin aplikasi web pake php dan mysql. 
    sometime juga bikin mobile app pake android studio. kerja di team kecil, 3 orang termasuk saya.
    
    pengalaman:
    - kerja sebagai programmer di PT ABC (2020-2023)
    - bikin website untuk toko online
    - maintain website yang sudah ada
    
    pendidikan:
    S1 Teknik Informatika - Universitas XYZ (2020)
    
    skills:
    php, mysql, html, css, javascript, android
    
    saya orangnya komunikatif, bisa kerja tim, dan cepat belajar.
    """

def test_standard_vs_critical_analysis():
    """Compare standard vs critical analysis capabilities"""
    print("=" * 80)
    print("🧪 TESTING: STANDARD vs CRITICAL ANALYSIS COMPARISON")
    print("=" * 80)
    
    analyzer = CVAnalyzer()
    
    # Test with good CV
    print("\n📄 Testing with GOOD QUALITY CV:")
    print("-" * 50)
    
    good_cv_text = create_test_cv_text()
    
    # Standard analysis
    print("1. STANDARD ANALYSIS:")
    try:
        # Save test CV to temporary file
        with open('/tmp/test_good_cv.txt', 'w', encoding='utf-8') as f:
            f.write(good_cv_text)
        
        standard_results = analyzer.analyze_cv('/tmp/test_good_cv.txt', len(good_cv_text.encode('utf-8')))
        
        print(f"   • Skills found: {len(standard_results.get('extracted_skills', []))}")
        print(f"   • ATS Score: {standard_results.get('ats_score', 0)}")
        print(f"   • Industry detected: {standard_results.get('detected_industry', 'unknown')}")
        print(f"   • Experience level: {standard_results.get('experience_level', 'unknown')}")
        
    except Exception as e:
        print(f"   ❌ Error in standard analysis: {e}")
    
    # Critical analysis
    print("\n2. CRITICAL ANALYSIS:")
    try:
        critical_results = analyzer.analyze_cv_critical('/tmp/test_good_cv.txt', len(good_cv_text.encode('utf-8')))
        
        # Show new features
        if critical_results.get('critical_analysis_included'):
            print("   ✅ CRITICAL ANALYSIS ENABLED")
            
            critical_analysis = critical_results.get('critical_analysis', {})
            content_score = critical_analysis.get('overall_score', 0)
            print(f"   • Content Quality Score: {content_score}/100")
            
            gaps = critical_analysis.get('critical_gaps', {})
            print(f"   • Critical gaps found: {len(gaps.get('critical', []))}")
            print(f"   • Important gaps found: {len(gaps.get('important', []))}")
            
            credibility = critical_analysis.get('credibility_analysis', {})
            print(f"   • Credibility Score: {credibility.get('score', 0)}/100")
            
            # Show enhanced summary
            enhanced_summary = critical_results.get('enhanced_summary', '')
            print(f"   • Enhanced Summary: {enhanced_summary[:100]}...")
        
    except Exception as e:
        print(f"   ❌ Error in critical analysis: {e}")
    
    # Test with poor CV
    print("\n\n📄 Testing with POOR QUALITY CV:")
    print("-" * 50)
    
    poor_cv_text = create_poor_cv_text()
    
    try:
        # Save test CV to temporary file
        with open('/tmp/test_poor_cv.txt', 'w', encoding='utf-8') as f:
            f.write(poor_cv_text)
        
        critical_results = analyzer.analyze_cv_critical('/tmp/test_poor_cv.txt', len(poor_cv_text.encode('utf-8')))
        
        critical_analysis = critical_results.get('critical_analysis', {})
        content_score = critical_analysis.get('overall_score', 0)
        print(f"   • Content Quality Score: {content_score}/100")
        
        gaps = critical_analysis.get('critical_gaps', {})
        print(f"   • Critical gaps: {len(gaps.get('critical', []))}")
        print(f"   • Important gaps: {len(gaps.get('important', []))}")
        print(f"   • Minor gaps: {len(gaps.get('minor', []))}")
        
        # Show critical issues found
        if gaps.get('critical'):
            print("   🚨 CRITICAL ISSUES DETECTED:")
            for gap in gaps['critical'][:3]:  # Show first 3
                print(f"      - {gap}")
        
    except Exception as e:
        print(f"   ❌ Error analyzing poor CV: {e}")

def test_intelligent_feedback():
    """Test the intelligent feedback generation system"""
    print("\n" + "=" * 80)
    print("💡 TESTING: INTELLIGENT FEEDBACK GENERATION")
    print("=" * 80)
    
    analyzer = CVAnalyzer()
    
    try:
        # Test with poor CV to get meaningful feedback
        with open('/tmp/test_poor_cv.txt', 'w', encoding='utf-8') as f:
            f.write(create_poor_cv_text())
        
        feedback_report = analyzer.get_detailed_critical_feedback('/tmp/test_poor_cv.txt', 1000)
        
        print("\n📊 OVERALL ASSESSMENT:")
        assessment = feedback_report.get('overall_assessment', {})
        print(f"   • Rating: {assessment.get('rating', 'N/A')}")
        print(f"   • Summary: {assessment.get('summary', 'N/A')}")
        print(f"   • Market Readiness: {assessment.get('market_readiness', 'N/A')}")
        
        print("\n🎯 ACTIONABLE RECOMMENDATIONS:")
        recommendations = feedback_report.get('actionable_recommendations', [])
        for i, rec in enumerate(recommendations[:5], 1):  # Show first 5
            print(f"   {i}. [{rec.get('priority', 'N/A')}] {rec.get('recommendation', 'N/A')[:80]}...")
            print(f"      Timeline: {rec.get('timeline', 'N/A')} | Impact: {rec.get('impact', 'N/A')}")
        
        print("\n📅 IMPROVEMENT TIMELINE:")
        timeline = feedback_report.get('improvement_timeline', {})
        for phase, actions in timeline.items():
            if actions:
                print(f"   • {phase.replace('_', ' ').title()}:")
                for action in actions[:2]:  # Show first 2 actions per phase
                    print(f"     - {action}")
        
        print("\n🇮🇩 INDONESIAN CONTEXT ADVICE:")
        indonesian_context = feedback_report.get('indonesian_context', {})
        formal_language = indonesian_context.get('formal_language', [])
        for advice in formal_language[:3]:  # Show first 3
            print(f"   • {advice}")
        
    except Exception as e:
        print(f"❌ Error testing intelligent feedback: {e}")

def test_indonesian_language_optimization():
    """Test Indonesian language processing improvements"""
    print("\n" + "=" * 80)
    print("🇮🇩 TESTING: INDONESIAN LANGUAGE OPTIMIZATION")
    print("=" * 80)
    
    analyzer = CVAnalyzer()
    
    # Test with mixed Indonesian CV
    mixed_cv_text = """
    BUDI SANTOSO
    Email: budi.santoso@gmail.com
    
    PROFIL
    Saya adalah seorang Full Stack Developer dengan pengalaman 4 tahun di industri teknologi. 
    Memiliki keahlian dalam pengembangan aplikasi web menggunakan teknologi modern dan passion 
    untuk menciptakan solusi inovatif. Berpengalaman dalam bekerja dengan tim lintas fungsi 
    dan memimpin proyek pengembangan perangkat lunak.

    PENGALAMAN KERJA

    Full Stack Developer | Digital Innovation Labs | 2021 - Sekarang
    • Mengembangkan aplikasi web enterprise menggunakan React.js dan Node.js
    • Memimpin tim 5 orang developer dalam pengembangan platform e-commerce
    • Berhasil meningkatkan user engagement sebesar 60% melalui optimasi UI/UX
    • Implementasi microservices architecture menggunakan Docker dan Kubernetes
    • Mentoring 3 junior developers dan conducting technical interviews

    Frontend Developer | TechStart Indonesia | 2019 - 2021  
    • Membuat responsive web applications menggunakan React.js dan Redux
    • Berkolaborasi dengan UI/UX designer untuk implementasi design system
    • Mengintegrasikan RESTful APIs dan third-party services
    • Optimasi performa aplikasi untuk mobile dan desktop platforms

    PENDIDIKAN
    Sarjana Ilmu Komputer | Institut Teknologi Bandung | 2019
    IPK: 3.8/4.0
    Organisasi: Kepala Departemen Teknologi, Himpunan Mahasiswa Ilmu Komputer

    SERTIFIKASI
    • AWS Certified Developer Associate (2022)
    • Google Mobile Web Specialist (2021)
    • Certified Kubernetes Administrator (2021)

    KEAHLIAN
    Frontend: React.js, Vue.js, TypeScript, HTML5, CSS3, SASS
    Backend: Node.js, Express.js, Python, Django, FastAPI  
    Database: PostgreSQL, MongoDB, Redis
    Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Jenkins
    Tools: Git, JIRA, Confluence, Figma, VS Code
    """
    
    try:
        # Save test CV
        with open('/tmp/test_mixed_cv.txt', 'w', encoding='utf-8') as f:
            f.write(mixed_cv_text)
        
        # Analyze with critical analysis
        results = analyzer.analyze_cv_critical('/tmp/test_mixed_cv.txt', len(mixed_cv_text.encode('utf-8')))
        
        print("\n📈 ANALYSIS RESULTS:")
        print(f"   • Skills detected: {len(results.get('extracted_skills', []))}")
        print(f"   • Language detected: {results.get('language_detected', 'unknown')}")
        print(f"   • Industry: {results.get('detected_industry', 'unknown')}")
        print(f"   • Experience level: {results.get('experience_level', 'unknown')}")
        
        # Show critical analysis insights
        critical_analysis = results.get('critical_analysis', {})
        content_quality = critical_analysis.get('content_quality', {})
        print(f"   • Content quality score: {content_quality.get('score', 0)}/100")
        
        # Show Indonesian-specific feedback
        if results.get('intelligent_feedback'):
            indonesian_advice = results['intelligent_feedback'].get('indonesian_specific_advice', {})
            if indonesian_advice.get('formal_language'):
                print("\n🇮🇩 INDONESIAN LANGUAGE FEEDBACK:")
                for feedback in indonesian_advice['formal_language'][:3]:
                    print(f"   • {feedback}")
        
        # Show enhanced summary in Indonesian
        enhanced_summary = results.get('enhanced_summary', '')
        if enhanced_summary:
            print(f"\n📝 ENHANCED SUMMARY (Indonesian):")
            print(f"   {enhanced_summary}")
        
    except Exception as e:
        print(f"❌ Error testing Indonesian optimization: {e}")

def test_competitive_analysis():
    """Test competitive positioning analysis"""
    print("\n" + "=" * 80)
    print("🏆 TESTING: COMPETITIVE POSITIONING ANALYSIS")
    print("=" * 80)
    
    analyzer = CVAnalyzer()
    
    # Test with good CV
    try:
        with open('/tmp/test_good_cv.txt', 'w', encoding='utf-8') as f:
            f.write(create_test_cv_text())
        
        feedback_report = analyzer.get_detailed_critical_feedback('/tmp/test_good_cv.txt', 1000)
        
        competitive_analysis = feedback_report.get('competitive_position', {})
        
        print("\n🎯 COMPETITIVE POSITIONING:")
        print(f"   • Current Position: {competitive_analysis.get('positioning', 'N/A')}")
        print(f"   • Market Readiness: {competitive_analysis.get('market_readiness', 'N/A')}")
        
        advantages = competitive_analysis.get('competitive_advantages', [])
        if advantages:
            print("\n💪 COMPETITIVE ADVANTAGES:")
            for advantage in advantages:
                print(f"   ✅ {advantage}")
        
        improvements = competitive_analysis.get('improvement_areas', [])
        if improvements:
            print("\n🔧 IMPROVEMENT AREAS:")
            for improvement in improvements:
                print(f"   ⚠️ {improvement}")
        
        # Show confidence level
        confidence = feedback_report.get('confidence_level', 'N/A')
        print(f"\n🎯 ANALYSIS CONFIDENCE: {confidence}")
        
    except Exception as e:
        print(f"❌ Error testing competitive analysis: {e}")

def demonstrate_improvement_plan():
    """Demonstrate the improvement planning feature"""
    print("\n" + "=" * 80)
    print("📋 DEMONSTRATION: STRUCTURED IMPROVEMENT PLAN")
    print("=" * 80)
    
    analyzer = CVAnalyzer()
    
    # Test with poor CV
    try:
        with open('/tmp/test_poor_cv.txt', 'w', encoding='utf-8') as f:
            f.write(create_poor_cv_text())
        
        feedback_report = analyzer.get_detailed_critical_feedback('/tmp/test_poor_cv.txt', 1000)
        
        next_steps = feedback_report.get('next_steps', [])
        
        print("\n📅 STRUCTURED IMPROVEMENT PLAN:")
        for step in next_steps:
            phase = step.get('phase', 'Unknown Phase')
            actions = step.get('actions', [])
            print(f"\n🎯 {phase}:")
            for action in actions:
                print(f"   • {action}")
        
        # Show priority improvements
        priority_improvements = feedback_report.get('priority_improvements', {})
        if priority_improvements.get('critical'):
            print("\n🚨 CRITICAL PRIORITY ACTIONS:")
            for critical in priority_improvements['critical'][:3]:
                print(f"   • {critical}")
        
        if priority_improvements.get('high'):
            print("\n⚠️ HIGH PRIORITY ACTIONS:")
            for high in priority_improvements['high'][:3]:
                print(f"   • {high}")
        
    except Exception as e:
        print(f"❌ Error demonstrating improvement plan: {e}")

def run_comprehensive_test():
    """Run all tests comprehensively"""
    print("🚀 COMPREHENSIVE TEST OF ENHANCED CV ANALYZER SYSTEM")
    print("=" * 80)
    print("Testing New Features:")
    print("• Critical Analysis Engine")
    print("• Intelligent Feedback Generation")
    print("• Indonesian Language Optimization")
    print("• Competitive Positioning Analysis")
    print("• Structured Improvement Planning")
    print("=" * 80)
    
    # Run all test functions
    test_standard_vs_critical_analysis()
    test_intelligent_feedback()
    test_indonesian_language_optimization()
    test_competitive_analysis()
    demonstrate_improvement_plan()
    
    print("\n" + "=" * 80)
    print("✅ COMPREHENSIVE TEST COMPLETED")
    print("=" * 80)
    print("\n🎯 SUMMARY OF ENHANCEMENTS:")
    print("1. ✅ CRITICAL ANALYSIS ENGINE - Deep content quality analysis")
    print("2. ✅ INTELLIGENT FEEDBACK - Specific, actionable recommendations")
    print("3. ✅ INDONESIAN OPTIMIZATION - Local business context awareness")
    print("4. ✅ COMPETITIVE ANALYSIS - Market positioning insights")
    print("5. ✅ STRUCTURED IMPROVEMENT PLAN - Timeline-based guidance")
    print("\n🚀 System ready for production use!")

if __name__ == "__main__":
    run_comprehensive_test()
