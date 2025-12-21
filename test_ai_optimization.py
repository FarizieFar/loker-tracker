#!/usr/bin/env python3
"""
Comprehensive Test Suite untuk AI Optimization
Memverifikasi semua fitur AI yang telah dioptimalkan
"""

import sys
import os
import tempfile
import traceback
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, '/Users/marianaulfahhoesny/Documents/PORTOFOLIO WEB/loker-tracker')

def test_expanded_skill_database():
    """Test expanded skill database coverage"""
    try:
        from ai_modules.nlp_processor import NLPProcessor
        
        nlp = NLPProcessor()
        
        # Check skill categories count
        skill_categories = list(nlp.skill_keywords.keys())
        print(f"✅ Skill Categories Found: {len(skill_categories)}")
        print(f"✅ Categories: {', '.join(skill_categories[:10])}...")
        
        # Test skill extraction across industries
        test_cases = {
            'technology': 'Python programming, React development, AWS cloud computing, Docker containers',
            'finance': 'Financial modeling, Bloomberg terminal, CFA certification, risk management',
            'healthcare': 'Patient care, medical coding, HIPAA compliance, clinical research',
            'marketing': 'Digital marketing, SEO, Google Ads, social media campaigns',
            'design': 'UI/UX design, Figma, Adobe Creative Suite, brand design'
        }
        
        results = {}
        for industry, text in test_cases.items():
            skills = nlp.extract_skills(text)
            results[industry] = len(skills)
            print(f"✅ {industry.title()} skills extracted: {skills}")
        
        total_skills_extracted = sum(results.values())
        print(f"✅ Total skills extracted across industries: {total_skills_extracted}")
        
        # Verify comprehensive coverage
        assert len(skill_categories) >= 15, "Should have at least 15 skill categories"
        assert total_skills_extracted >= 20, "Should extract at least 20 skills total"
        
        print("✅ EXPANDED SKILL DATABASE: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Expanded Skill Database Test Failed: {str(e)}")
        traceback.print_exc()
        return False

def test_enhanced_ats_scoring():
    """Test enhanced ATS scoring system"""
    try:
        from ai_modules.nlp_processor import NLPProcessor
        
        nlp = NLPProcessor()
        
        # Test CV with comprehensive content
        comprehensive_cv = """
        John Doe
        Email: john.doe@email.com
        Phone: +1234567890
        
        Professional Summary
        Experienced software engineer with 5+ years in full-stack development
        
        Experience
        Senior Software Engineer at Tech Corp (2020-2023)
        - Developed scalable web applications using Python and React
        - Led a team of 3 developers and delivered 15+ projects
        - Improved system performance by 40% through optimization
        
        Junior Developer at Startup Inc (2018-2020)
        - Built REST APIs using Django and PostgreSQL
        - Implemented automated testing and CI/CD pipelines
        
        Education
        Bachelor of Computer Science, University of Technology (2018)
        GPA: 3.8/4.0
        
        Skills
        Programming: Python, JavaScript, React, Node.js, Django
        Cloud: AWS, Docker, Kubernetes
        Tools: Git, Jenkins, JIRA
        Soft Skills: Leadership, Communication, Problem Solving
        
        Projects
        - E-commerce Platform: Built full-stack application serving 10k+ users
        - Data Analytics Tool: Created dashboard for business intelligence
        """
        
        # Extract skills
        skills = nlp.extract_skills(comprehensive_cv)
        
        # Calculate ATS score
        ats_score = nlp.calculate_ats_score(comprehensive_cv, skills)
        
        print(f"✅ ATS Score: {ats_score}")
        print(f"✅ Skills extracted: {len(skills)}")
        print(f"✅ Skills: {skills}")
        
        # Test industry keywords detection
        industry_keywords = nlp._extract_industry_keywords(comprehensive_cv)
        print(f"✅ Industry keywords: {industry_keywords}")
        
        # Test skills categories detection
        skills_categories = nlp._detect_skills_categories(skills)
        print(f"✅ Skills categories: {skills_categories}")
        
        # Verify enhanced scoring
        assert ats_score > 50, "Enhanced ATS score should be reasonable for comprehensive CV"
        assert len(skills) >= 10, "Should extract substantial skills"
        assert len(skills_categories) >= 3, "Should detect multiple skill categories"
        
        print("✅ ENHANCED ATS SCORING: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced ATS Scoring Test Failed: {str(e)}")
        traceback.print_exc()
        return False

def test_industry_detection_and_benchmarks():
    """Test industry detection and benchmark analysis"""
    try:
        from ai_modules.cv_analyzer import CVAnalyzer
        
        cv_analyzer = CVAnalyzer()
        
        # Test different industry CVs
        industry_tests = {
            'technology': """
                Python Developer with 3 years experience
                Skills: Python, Django, React, AWS, Docker
                Experience: Full-stack development, REST APIs, cloud deployment
                """,
            'finance': """
                Financial Analyst with CFA certification
                Skills: Financial modeling, Bloomberg, Excel, Risk management
                Experience: Investment analysis, portfolio management, financial reporting
                """,
            'marketing': """
                Digital Marketing Specialist
                Skills: Google Ads, Facebook Ads, SEO, Analytics, Content marketing
                Experience: Campaign management, lead generation, social media strategy
                """
        }
        
        results = {}
        for industry, cv_text in industry_tests.items():
            # Extract skills using NLP
            skills = cv_analyzer.nlp.extract_skills(cv_text)
            
            # Detect industry
            detected_industry = cv_analyzer.detect_industry(cv_text, skills)
            
            # Analyze benchmarks
            benchmarks = cv_analyzer.analyze_industry_benchmarks(cv_text, skills, detected_industry)
            
            results[industry] = {
                'detected': detected_industry,
                'skills': len(skills),
                'benchmarks': benchmarks.get('benchmark_score', 0) if benchmarks else 0
            }
            
            print(f"✅ {industry.title()}: Detected as {detected_industry}, Skills: {len(skills)}, Benchmark: {benchmarks.get('benchmark_score', 0)}")
        
        # Verify industry detection accuracy
        technology_correct = results['technology']['detected'] == 'technology'
        finance_correct = results['finance']['detected'] == 'finance' 
        marketing_correct = results['marketing']['detected'] == 'marketing'
        
        print(f"✅ Industry Detection Accuracy:")
        print(f"   Technology: {'✅' if technology_correct else '❌'}")
        print(f"   Finance: {'✅' if finance_correct else '❌'}")
        print(f"   Marketing: {'✅' if marketing_correct else '❌'}")
        
        # At least 2 out of 3 should be correct
        accuracy = sum([technology_correct, finance_correct, marketing_correct])
        assert accuracy >= 2, f"Industry detection accuracy should be at least 2/3, got {accuracy}/3"
        
        print("✅ INDUSTRY DETECTION & BENCHMARKS: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Industry Detection Test Failed: {str(e)}")
        traceback.print_exc()
        return False

def test_enhanced_cv_analysis():
    """Test enhanced CV analysis with industry context"""
    try:
        from ai_modules.cv_analyzer import CVAnalyzer
        
        cv_analyzer = CVAnalyzer()
        
        # Create comprehensive test CV
        test_cv_content = """
        Sarah Johnson
        Email: sarah.johnson@email.com
        Phone: +1987654321
        
        Professional Summary
        Senior Data Scientist with 6 years of experience in machine learning and analytics
        
        Experience
        Senior Data Scientist at DataCorp (2021-2023)
        - Developed ML models that increased revenue by 25%
        - Led team of 4 data scientists and mentored junior colleagues
        - Implemented MLOps pipeline using AWS and Docker
        
        Data Scientist at Analytics Inc (2019-2021)
        - Built predictive models using Python, TensorFlow, and scikit-learn
        - Created dashboards using Tableau and Power BI
        - Collaborated with business stakeholders on data-driven decisions
        
        Education
        Master of Science in Data Science, Tech University (2019)
        Bachelor of Statistics, State University (2017)
        
        Skills
        Programming: Python, R, SQL, Scala
        ML/AI: TensorFlow, PyTorch, scikit-learn, XGBoost
        Data Tools: Pandas, NumPy, Apache Spark, Hadoop
        Cloud: AWS, Azure, GCP
        Visualization: Tableau, Power BI, Matplotlib, Seaborn
        """
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_cv_content)
            temp_file_path = f.name
        
        try:
            # Analyze CV
            analysis_result = cv_analyzer.analyze_cv(temp_file_path, len(test_cv_content))
            
            # Verify enhanced analysis
            print(f"✅ Extracted Skills: {len(analysis_result['extracted_skills'])}")
            print(f"✅ ATS Score: {analysis_result['ats_score']}")
            print(f"✅ Experience Level: {analysis_result['experience_level']}")
            print(f"✅ Years Experience: {analysis_result['years_experience']}")
            print(f"✅ Detected Industry: {analysis_result['detected_industry']}")
            print(f"✅ Industry Benchmark Score: {analysis_result['industry_benchmarks'].get('benchmark_score', 'N/A')}")
            
            # Verify enhanced summary
            summary = analysis_result['summary']
            print(f"✅ Enhanced Summary Length: {len(summary)} characters")
            
            # Check for industry-specific content in summary
            industry_specific_terms = ['data science', 'machine learning', 'analytics', 'technology']
            has_industry_context = any(term in summary.lower() for term in industry_specific_terms)
            print(f"✅ Summary has industry context: {'✅' if has_industry_context else '❌'}")
            
            # Verify comprehensive analysis
            assert analysis_result['ats_score'] > 0, "ATS score should be calculated"
            assert analysis_result['detected_industry'] != 'unknown', "Industry should be detected"
            assert len(analysis_result['extracted_skills']) >= 8, "Should extract substantial skills"
            assert len(summary) > 100, "Enhanced summary should be comprehensive"
            
            print("✅ ENHANCED CV ANALYSIS: PASSED")
            return True
            
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)
        
    except Exception as e:
        print(f"❌ Enhanced CV Analysis Test Failed: {str(e)}")
        traceback.print_exc()
        return False

def test_advanced_recommendations():
    """Test advanced insights and recommendations system"""
    try:
        from ai_modules.insights_generator import InsightsGenerator
        
        insights_gen = InsightsGenerator()
        
        # Create comprehensive user data
        user_data = {
            'cv_analysis': {
                'extracted_skills': ['python', 'react', 'aws', 'docker', 'sql'],
                'ats_score': 75,
                'experience_level': 'mid',
                'years_experience': 4,
                'detected_industry': 'technology'
            },
            'job_applications': [
                {'position': 'Senior Python Developer', 'requirements': ['python', 'django', 'aws']},
                {'position': 'Full Stack Engineer', 'requirements': ['react', 'node.js', 'docker']}
            ]
        }
        
        # Generate all insights
        all_insights = insights_gen.generate_all_insights(user_data)
        
        print(f"✅ Total insights generated: {len(all_insights)}")
        
        # Test specific insight types
        career_insights = insights_gen.analyze_career_path(user_data)
        skill_gap_insights = insights_gen.analyze_skill_gaps(user_data)
        market_insights = insights_gen.analyze_market_trends(user_data)
        success_insights = insights_gen.predict_success_probability(user_data)
        
        print(f"✅ Career path insights: {len(career_insights)}")
        print(f"✅ Skill gap insights: {len(skill_gap_insights)}")
        print(f"✅ Market trend insights: {len(market_insights)}")
        print(f"✅ Success prediction insights: {len(success_insights)}")
        
        # Verify insight quality
        high_priority_insights = [i for i in all_insights if i.get('priority', 0) >= 4]
        actionable_insights = [i for i in all_insights if i.get('action_required', False)]
        
        print(f"✅ High priority insights: {len(high_priority_insights)}")
        print(f"✅ Actionable insights: {len(actionable_insights)}")
        
        # Sample insights
        for i, insight in enumerate(all_insights[:3]):
            print(f"   Insight {i+1}: {insight['title']} (Priority: {insight['priority']})")
        
        # Verify comprehensive insights
        assert len(all_insights) >= 8, "Should generate comprehensive insights"
        assert len(high_priority_insights) >= 2, "Should identify high priority areas"
        assert len(actionable_insights) >= 3, "Should provide actionable recommendations"
        
        print("✅ ADVANCED RECOMMENDATIONS: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Advanced Recommendations Test Failed: {str(e)}")
        traceback.print_exc()
        return False

def test_integration_between_components():
    """Test integration between all AI components"""
    try:
        from ai_modules.cv_analyzer import CVAnalyzer
        from ai_modules.nlp_processor import NLPProcessor
        from ai_modules.insights_generator import InsightsGenerator
        
        # Test end-to-end workflow
        test_cv = """
        Michael Chen
        Email: michael.chen@email.com
        Phone: +1122334455
        
        Summary
        Experienced DevOps Engineer with 7 years in cloud infrastructure
        
        Experience
        DevOps Lead at CloudTech (2020-2023)
        - Managed AWS infrastructure for 50+ microservices
        - Implemented Kubernetes orchestration and CI/CD pipelines
        - Reduced deployment time by 60% using automation
        
        Senior DevOps Engineer at ScaleCorp (2018-2020)
        - Built monitoring systems using Prometheus and Grafana
        - Developed infrastructure as code using Terraform
        
        Skills
        Cloud: AWS, Azure, GCP
        Containers: Docker, Kubernetes, Helm
        IaC: Terraform, Ansible, CloudFormation
        Monitoring: Prometheus, Grafana, ELK Stack
        Programming: Python, Bash, Go
        """
        
        # Step 1: NLP Processing
        nlp = NLPProcessor()
        nlp_results = nlp.process_cv_text(test_cv)
        
        # Step 2: CV Analysis with industry detection
        cv_analyzer = CVAnalyzer()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_cv)
            temp_file_path = f.name
        
        try:
            cv_analysis = cv_analyzer.analyze_cv(temp_file_path, len(test_cv))
            
            # Step 3: Insights Generation
            insights_gen = InsightsGenerator()
            user_data = {
                'cv_analysis': cv_analysis,
                'job_applications': []
            }
            insights = insights_gen.generate_all_insights(user_data)
            
            # Verify integration
            print(f"✅ NLP Skills extracted: {len(nlp_results['extracted_skills'])}")
            print(f"✅ CV Industry detected: {cv_analysis['detected_industry']}")
            print(f"✅ Industry benchmark score: {cv_analysis['industry_benchmarks'].get('benchmark_score', 'N/A')}")
            print(f"✅ Total insights generated: {len(insights)}")
            
            # Check data flow consistency
            nlp_skills = set(skill.lower() for skill in nlp_results['extracted_skills'])
            cv_skills = set(skill.lower() for skill in cv_analysis['extracted_skills'])
            
            skills_consistency = len(nlp_skills & cv_skills) / max(len(nlp_skills), len(cv_skills))
            print(f"✅ Skills consistency between NLP and CV analysis: {skills_consistency:.2f}")
            
            # Verify enhanced features are working
            assert cv_analysis['detected_industry'] != 'unknown', "Industry should be detected"
            assert cv_analysis['industry_benchmarks'], "Industry benchmarks should be generated"
            assert len(insights) > 0, "Insights should be generated"
            assert skills_consistency > 0.8, "Skills extraction should be consistent"
            
            print("✅ COMPONENT INTEGRATION: PASSED")
            return True
            
        finally:
            os.unlink(temp_file_path)
        
    except Exception as e:
        print(f"❌ Component Integration Test Failed: {str(e)}")
        traceback.print_exc()
        return False

def main():
    """Main test function for AI optimization"""
    print("🧪 COMPREHENSIVE AI OPTIMIZATION TEST")
    print("=" * 60)
    print(f"📅 Test date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Expanded Skill Database", test_expanded_skill_database),
        ("Enhanced ATS Scoring", test_enhanced_ats_scoring),
        ("Industry Detection & Benchmarks", test_industry_detection_and_benchmarks),
        ("Enhanced CV Analysis", test_enhanced_cv_analysis),
        ("Advanced Recommendations", test_advanced_recommendations),
        ("Component Integration", test_integration_between_components)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 40)
        
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
    print("\n" + "=" * 60)
    print("📊 AI OPTIMIZATION TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print(f"\n📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL AI OPTIMIZATION TESTS PASSED!")
        print("🚀 The AI system has been successfully optimized with:")
        print("   • 15+ industry skill categories")
        print("   • Advanced ATS scoring (9 factors)")
        print("   • Industry-specific analysis and benchmarks")
        print("   • Enhanced CV analysis with industry context")
        print("   • Advanced insights and recommendations")
        print("   • Full component integration")
    else:
        print("⚠️  Some tests failed. Please review the results above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
