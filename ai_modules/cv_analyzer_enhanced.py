"""
Enhanced CV Analyzer Extensions
Additional methods for detailed CV analysis with component scoring and improvement plans
"""

def generate_component_scores(self, extracted_data):
    """Generate detailed scores for each CV component"""
    if not extracted_data:
        return {}
    
    scores = {}
    
    # 1. Content Quality Score
    skills = extracted_data.get('extracted_skills', [])
    content_score = min(100, (len(skills) * 10) + (len(extracted_data.get('extracted_text', '')) / 20))
    scores['content_quality'] = min(content_score, 100)
    
    # 2. ATS Optimization Score
    ats_score = extracted_data.get('ats_score', 0)
    scores['ats_optimization'] = ats_score
    
    # 3. Contact Information Score
    contact_info = extracted_data.get('contact_info', {})
    contact_score = 0
    if contact_info.get('email'):
        contact_score += 40
    if contact_info.get('phone'):
        contact_score += 40
    if contact_info.get('name'):
        contact_score += 20
    scores['contact_information'] = contact_score
    
    # 4. Experience Depth Score
    years_experience = extracted_data.get('years_experience', 0)
    experience_score = min(100, years_experience * 10)
    scores['experience_depth'] = experience_score
    
    # 5. Industry Relevance Score
    industry_benchmarks = extracted_data.get('industry_benchmarks', {})
    industry_score = industry_benchmarks.get('benchmark_score', 0) if industry_benchmarks else 50
    scores['industry_relevance'] = industry_score
    
    # 6. Overall CV Strength Score
    overall_score = (scores['content_quality'] + scores['ats_optimization'] + 
                    scores['contact_information'] + scores['experience_depth'] + 
                    scores['industry_relevance']) / 5
    scores['overall_strength'] = round(overall_score, 1)
    
    return scores

def generate_detailed_component_analysis(self, extracted_data):
    """Generate detailed analysis for each CV component with specific feedback"""
    if not extracted_data:
        return {}
    
    analysis = {}
    
    scores = self.generate_component_scores(extracted_data)
    
    # Content Quality Analysis
    content_score = scores.get('content_quality', 0)
    skills = extracted_data.get('extracted_skills', [])
    text_length = len(extracted_data.get('extracted_text', ''))
    
    analysis['content_quality'] = {
        'score': content_score,
        'status': 'Excellent' if content_score >= 80 else 'Good' if content_score >= 60 else 'Needs Improvement',
        'strengths': [],
        'weaknesses': [],
        'recommendations': []
    }
    
    if len(skills) >= 10:
        analysis['content_quality']['strengths'].append(f"Comprehensive skills portfolio with {len(skills)} competencies")
    elif len(skills) >= 5:
        analysis['content_quality']['strengths'].append(f"Decent skills portfolio with {len(skills)} competencies")
    else:
        analysis['content_quality']['weaknesses'].append(f"Limited skills portfolio with only {len(skills)} competencies")
        analysis['content_quality']['recommendations'].append("Add more technical skills and competencies to strengthen your profile")
    
    if text_length > 500:
        analysis['content_quality']['strengths'].append("Sufficient content length for comprehensive analysis")
    else:
        analysis['content_quality']['weaknesses'].append("Content appears too brief")
        analysis['content_quality']['recommendations'].append("Expand your CV content with more detailed descriptions")
    
    # ATS Optimization Analysis
    ats_score = scores.get('ats_optimization', 0)
    analysis['ats_optimization'] = {
        'score': ats_score,
        'status': 'Excellent' if ats_score >= 80 else 'Good' if ats_score >= 60 else 'Needs Improvement',
        'strengths': [],
        'weaknesses': [],
        'recommendations': []
    }
    
    if ats_score >= 80:
        analysis['ats_optimization']['strengths'].append("Excellent ATS compatibility and keyword optimization")
    elif ats_score >= 60:
        analysis['ats_optimization']['strengths'].append("Good ATS compatibility with room for improvement")
    else:
        analysis['ats_optimization']['weaknesses'].append("Poor ATS compatibility - needs immediate optimization")
        analysis['ats_optimization']['recommendations'].extend([
            "Include more industry-relevant keywords",
            "Use standard section headers",
            "Improve formatting consistency",
            "Test with ATS scanning tools"
        ])
    
    # Contact Information Analysis
    contact_score = scores.get('contact_information', 0)
    contact_info = extracted_data.get('contact_info', {})
    
    analysis['contact_information'] = {
        'score': contact_score,
        'status': 'Complete' if contact_score >= 80 else 'Partial' if contact_score >= 40 else 'Missing',
        'strengths': [],
        'weaknesses': [],
        'recommendations': []
    }
    
    if contact_info.get('email'):
        analysis['contact_information']['strengths'].append("Email address provided")
    else:
        analysis['contact_information']['weaknesses'].append("Missing email address")
        analysis['contact_information']['recommendations'].append("Add professional email address")
    
    if contact_info.get('phone'):
        analysis['contact_information']['strengths'].append("Phone number provided")
    else:
        analysis['contact_information']['weaknesses'].append("Missing phone number")
        analysis['contact_information']['recommendations'].append("Add phone number for easy contact")
    
    if contact_info.get('name'):
        analysis['contact_information']['strengths'].append("Name clearly identified")
    else:
        analysis['contact_information']['weaknesses'].append("Name not clearly identified")
        analysis['contact_information']['recommendations'].append("Ensure name is prominently displayed")
    
    # Experience Depth Analysis
    experience_score = scores.get('experience_depth', 0)
    years_experience = extracted_data.get('years_experience', 0)
    experience_level = extracted_data.get('experience_level', 'unknown')
    
    analysis['experience_depth'] = {
        'score': experience_score,
        'status': 'Senior' if experience_score >= 70 else 'Mid' if experience_score >= 30 else 'Junior',
        'strengths': [],
        'weaknesses': [],
        'recommendations': []
    }
    
    if years_experience >= 5:
        analysis['experience_depth']['strengths'].append(f"Strong experience foundation with {years_experience} years")
    elif years_experience >= 2:
        analysis['experience_depth']['strengths'].append(f"Moderate experience with {years_experience} years")
    else:
        analysis['experience_depth']['weaknesses'].append(f"Limited experience with {years_experience} years")
        analysis['experience_depth']['recommendations'].extend([
            "Highlight relevant projects and internships",
            "Emphasize learning and growth potential",
            "Include freelance or volunteer experience"
        ])
    
    if experience_level == 'senior':
        analysis['experience_depth']['strengths'].append("Senior-level experience demonstrates leadership capability")
    elif experience_level == 'mid':
        analysis['experience_depth']['strengths'].append("Mid-level experience with solid foundation")
    
    # Industry Relevance Analysis
    industry_score = scores.get('industry_relevance', 0)
    detected_industry = extracted_data.get('detected_industry', 'general')
    industry_benchmarks = extracted_data.get('industry_benchmarks', {})
    
    analysis['industry_relevance'] = {
        'score': industry_score,
        'status': 'Excellent' if industry_score >= 80 else 'Good' if industry_score >= 60 else 'Needs Development',
        'strengths': [],
        'weaknesses': [],
        'recommendations': []
    }
    
    if detected_industry != 'general':
        analysis['industry_relevance']['strengths'].append(f"Clear industry focus in {detected_industry}")
        
        if industry_benchmarks:
            essential_skills = industry_benchmarks.get('essential_skills_match', [])
            if essential_skills:
                analysis['industry_relevance']['strengths'].append(f"Has {len(essential_skills)} essential {detected_industry} skills")
            
            essential_missing = industry_benchmarks.get('essential_skills_missing', [])
            if essential_missing:
                analysis['industry_relevance']['weaknesses'].append(f"Missing {len(essential_missing)} essential {detected_industry} skills")
                analysis['industry_relevance']['recommendations'].append(f"Develop {', '.join(essential_missing[:3])} skills")
    else:
        analysis['industry_relevance']['weaknesses'].append("Industry not clearly identified")
        analysis['industry_relevance']['recommendations'].append("Clearly identify your target industry and relevant skills")
    
    return analysis

def generate_specific_improvement_plan(self, extracted_data):
    """Generate specific improvement plan with timelines and resources"""
    if not extracted_data:
        return ""
    
    improvement_plan = []
    
    scores = self.generate_component_scores(extracted_data)
    component_analysis = self.generate_detailed_component_analysis(extracted_data)
    ats_score = extracted_data.get('ats_score', 0)
    skills = extracted_data.get('extracted_skills', [])
    detected_industry = extracted_data.get('detected_industry', 'general')
    
    improvement_plan.append("📅 IMPROVEMENT TIMELINE & RESOURCES:\n")
    
    # Week 1-2: Immediate improvements
    improvement_plan.append("🗓️ WEEK 1-2 (IMMEDIATE IMPROVEMENTS):")
    
    if ats_score < 70:
        improvement_plan.append("  • ATS Optimization (2-3 days):")
        improvement_plan.append("    - Research 10-15 job descriptions in your field")
        improvement_plan.append("    - Extract and incorporate relevant keywords naturally")
        improvement_plan.append("    - Ensure standard section headers (Experience, Education, Skills)")
        improvement_plan.append("    - Use tools: JobScan.co, Resume Worded for ATS testing")
    
    contact_info = extracted_data.get('contact_info', {})
    if not contact_info.get('email') or not contact_info.get('phone'):
        improvement_plan.append("  • Complete Contact Info (1 day):")
        improvement_plan.append("    - Add professional email address")
        improvement_plan.append("    - Include phone number with proper formatting")
        improvement_plan.append("    - Consider adding LinkedIn profile link")
    
    improvement_plan.append("")
    
    # Week 3-4: Skills enhancement
    improvement_plan.append("🗓️ WEEK 3-4 (SKILLS ENHANCEMENT):")
    
    if len(skills) < 10:
        improvement_plan.append("  • Skills Portfolio Expansion (1 week):")
        improvement_plan.append(f"    - Add {10 - len(skills)} more relevant skills")
        improvement_plan.append("    - Focus on industry-standard technologies/tools")
        improvement_plan.append("    - Include both technical and soft skills")
        
        if detected_industry == 'technology':
            improvement_plan.append("    - Recommended additions: Cloud platforms (AWS/Azure), CI/CD tools, Version control")
        elif detected_industry == 'finance':
            improvement_plan.append("    - Recommended additions: Financial modeling tools, Bloomberg terminal, Risk management")
        elif detected_industry == 'marketing':
            improvement_plan.append("    - Recommended additions: Marketing automation, Analytics tools, SEO platforms")
    
    improvement_plan.append("")
    
    # Month 2: Industry-specific development
    if detected_industry != 'general':
        improvement_plan.append("🗓️ MONTH 2 (INDUSTRY-SPECIFIC DEVELOPMENT):")
        
        industry_benchmarks = extracted_data.get('industry_benchmarks', {})
        essential_missing = industry_benchmarks.get('essential_skills_missing', [])
        
        if essential_missing:
            improvement_plan.append(f"  • {detected_industry.title()} Essential Skills:")
            improvement_plan.append("    - Online courses:")
            
            if detected_industry == 'technology':
                improvement_plan.append("      * Coursera: Software Development courses")
                improvement_plan.append("      * Udemy: Programming and framework specific courses")
                improvement_plan.append("      * Pluralsight: Technical skill paths")
            elif detected_industry == 'finance':
                improvement_plan.append("      * CFA Institute: Investment analysis courses")
                improvement_plan.append("      * Coursera: Financial modeling specialization")
                improvement_plan.append("      * Bloomberg Market Concepts: Financial markets")
            elif detected_industry == 'marketing':
                improvement_plan.append("      * Google Digital Garage: Digital marketing courses")
                improvement_plan.append("      * HubSpot Academy: Inbound marketing certification")
                improvement_plan.append("      * Facebook Blueprint: Social media marketing")
            
            improvement_plan.append("    - Practical experience:")
            improvement_plan.append("      * Personal projects or freelance work")
            improvement_plan.append("      * Open source contributions")
            improvement_plan.append("      * Industry certifications")
    
    improvement_plan.append("")
    
    # Long-term: Strategic improvements
    improvement_plan.append("🗓️ ONGOING (STRATEGIC IMPROVEMENTS):")
    
    years_experience = extracted_data.get('years_experience', 0)
    if years_experience < 5:
        improvement_plan.append("  • Career Development:")
        improvement_plan.append("    - Seek mentorship opportunities")
        improvement_plan.append("    - Take on challenging projects")
        improvement_plan.append("    - Build a portfolio of work samples")
        improvement_plan.append("    - Network within your industry")
    
    education_level = extracted_data.get('education_level', 'unknown')
    if education_level in ['high_school', 'unknown']:
        improvement_plan.append("  • Education Enhancement:")
        improvement_plan.append("    - Consider professional certifications")
        improvement_plan.append("    - Take relevant online courses")
        improvement_plan.append("    - Attend industry conferences and workshops")
    
    improvement_plan.append("")
    
    # Resources and tools
    improvement_plan.append("🛠️ RECOMMENDED TOOLS & RESOURCES:")
    improvement_plan.append("  • ATS Optimization:")
    improvement_plan.append("    - JobScan.co (ATS compatibility checker)")
    improvement_plan.append("    - Resume Worded (resume optimization)")
    improvement_plan.append("    - LinkedIn Resume Assistant")
    improvement_plan.append("")
    improvement_plan.append("  • Skill Development:")
    improvement_plan.append("    - Coursera (university-level courses)")
    improvement_plan.append("    - Udemy (practical skill courses)")
    improvement_plan.append("    - LinkedIn Learning (professional skills)")
    improvement_plan.append("    - Khan Academy (foundational knowledge)")
    improvement_plan.append("")
    improvement_plan.append("  • Industry-Specific:")
    improvement_plan.append("    - GitHub (for showcasing coding projects)")
    improvement_plan.append("    - Behance/Dribbble (for design portfolios)")
    improvement_plan.append("    - Tableau Public (for data visualization)")
    improvement_plan.append("    - Google Analytics Academy (for marketing)")
    
    return "\n".join(improvement_plan)
