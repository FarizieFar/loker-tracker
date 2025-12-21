"""
Insights Generator Module
Generates AI-powered insights and recommendations for users
"""

import json
from datetime import datetime, timedelta
from collections import Counter, defaultdict

class InsightsGenerator:
    """AI-powered insights and recommendations generator"""
    
    def __init__(self):
        self.insight_types = [
            'career_path', 'skill_gap', 'market_trend', 'success_prediction',
            'application_strategy', 'skill_development', 'industry_analysis'
        ]
        
        # Common career patterns and insights
        self.career_patterns = {
            'technology': {
                'progression_path': ['Junior Developer', 'Mid Developer', 'Senior Developer', 'Tech Lead', 'Engineering Manager'],
                'key_skills': ['Programming', 'Problem Solving', 'System Design', 'Leadership', 'Communication'],
                'growth_areas': ['Cloud Computing', 'DevOps', 'Machine Learning', 'Cybersecurity']
            },
            'data_science': {
                'progression_path': ['Data Analyst', 'Data Scientist', 'Senior Data Scientist', 'Lead Data Scientist', 'Head of Data'],
                'key_skills': ['Statistics', 'Programming', 'Machine Learning', 'Business Acumen', 'Visualization'],
                'growth_areas': ['AI/ML', 'Big Data', 'Cloud Analytics', 'MLOps']
            },
            'marketing': {
                'progression_path': ['Marketing Coordinator', 'Marketing Specialist', 'Marketing Manager', 'Senior Marketing Manager', 'Marketing Director'],
                'key_skills': ['Digital Marketing', 'Analytics', 'Content Creation', 'Campaign Management', 'Brand Strategy'],
                'growth_areas': ['Performance Marketing', 'Marketing Automation', 'Influencer Marketing', 'Marketing Technology']
            }
        }
        
        # Market trends (can be updated with real data)
        self.market_trends = {
            'high_demand_skills': [
                'Python Programming', 'Cloud Computing', 'Data Science', 'Machine Learning',
                'Cybersecurity', 'DevOps', 'React/Frontend Development', 'SQL/Database Management'
            ],
            'emerging_skills': [
                'AI/ChatGPT Integration', 'Kubernetes', 'Docker', 'Serverless Computing',
                'Edge Computing', 'Quantum Computing', 'Blockchain Development'
            ],
            'salary_growth_skills': [
                'Machine Learning', 'Cloud Architecture', 'Cybersecurity', 'DevOps Engineering',
                'Data Engineering', 'Product Management'
            ]
        }
    
    def analyze_career_path(self, user_data):
        """Generate career path insights"""
        try:
            # Extract user information
            cv_analysis = user_data.get('cv_analysis', {})
            job_history = user_data.get('job_applications', [])
            
            # Determine current career stage
            current_stage = self._determine_career_stage(cv_analysis, job_history)
            
            # Identify industry category
            industry = self._identify_industry(cv_analysis, job_history)
            
            # Get career progression path
            progression_path = self._get_career_progression_path(industry, current_stage)
            
            # Generate insights
            insights = []
            
            # Current stage assessment
            insights.append({
                'type': 'career_stage_assessment',
                'title': 'Current Career Stage Analysis',
                'content': f"You appear to be at the {current_stage.replace('_', ' ')} stage in the {industry.replace('_', ' ')} field. Based on your experience and skills, you're well-positioned for the next level in your career progression.",
                'confidence': 0.8,
                'priority': 3,
                'related_skills': self._get_stage_skills(current_stage)
            })
            
            # Progression timeline
            if progression_path:
                next_level = progression_path[0] if progression_path else 'Senior Role'
                insights.append({
                    'type': 'progression_timeline',
                    'title': 'Career Progression Timeline',
                    'content': f"Based on typical career progression in {industry.replace('_', ' ')}, you could advance to {next_level} within 2-3 years with consistent skill development and strategic career moves.",
                    'confidence': 0.7,
                    'priority': 4,
                    'action_required': True,
                    'action_text': f"Focus on developing skills required for {next_level} role"
                })
            
            # Skills development priority
            skill_priorities = self._get_skill_priorities(industry, current_stage)
            if skill_priorities:
                insights.append({
                    'type': 'skill_development_priority',
                    'title': 'Priority Skills for Career Growth',
                    'content': f"To accelerate your career progression, focus on developing these high-value skills: {', '.join(skill_priorities[:3])}. These skills are currently in high demand in the {industry.replace('_', ' ')} industry.",
                    'confidence': 0.85,
                    'priority': 5,
                    'action_required': True,
                    'action_text': 'Create a learning plan for priority skills',
                    'related_skills': skill_priorities
                })
            
            return insights
            
        except Exception as e:
            return [self._create_error_insight(str(e))]
    
    def analyze_skill_gaps(self, user_data):
        """Identify and analyze skill gaps"""
        try:
            cv_analysis = user_data.get('cv_analysis', {})
            job_applications = user_data.get('job_applications', [])
            
            # Extract current skills
            current_skills = cv_analysis.get('extracted_skills', [])
            
            # Analyze job requirements from applications
            all_required_skills = self._extract_all_job_skills(job_applications)
            
            # Identify gaps
            skill_gaps = list(set(all_required_skills) - set(current_skills))
            
            insights = []
            
            if skill_gaps:
                # High-priority gaps
                high_priority_gaps = self._identify_high_priority_gaps(skill_gaps)
                if high_priority_gaps:
                    insights.append({
                        'type': 'critical_skill_gaps',
                        'title': 'Critical Skill Gaps Identified',
                        'content': f"Your applications reveal gaps in these high-demand skills: {', '.join(high_priority_gaps[:3])}. Addressing these gaps could significantly improve your job match scores.",
                        'confidence': 0.9,
                        'priority': 5,
                        'action_required': True,
                        'action_text': 'Prioritize learning these skills',
                        'related_skills': high_priority_gaps
                    })
                
                # Learning recommendations
                learning_resources = self._get_learning_resources(skill_gaps[:5])
                if learning_resources:
                    insights.append({
                        'type': 'learning_recommendations',
                        'title': 'Structured Learning Path',
                        'content': f"Create a structured learning plan for your skill gaps. Start with fundamentals and progress to advanced concepts. Consider online courses, certifications, and hands-on projects.",
                        'confidence': 0.8,
                        'priority': 4,
                        'action_required': True,
                        'action_text': 'Create a 3-month learning plan'
                    })
            
            # Skills strength analysis
            if current_skills:
                strength_score = self._calculate_skills_strength(current_skills, all_required_skills)
                if strength_score < 50:
                    insights.append({
                        'type': 'skills_strength',
                        'title': 'Skills Portfolio Assessment',
                        'content': f"Your current skills portfolio shows {strength_score}% alignment with market demands. Focus on expanding both technical and soft skills to increase your competitiveness.",
                        'confidence': 0.85,
                        'priority': 4,
                        'action_required': True,
                        'action_text': 'Expand skills portfolio systematically'
                    })
            
            return insights
            
        except Exception as e:
            return [self._create_error_insight(str(e))]
    
    def analyze_market_trends(self, user_data):
        """Analyze current market trends and opportunities"""
        try:
            cv_analysis = user_data.get('cv_analysis', {})
            industry = self._identify_industry(cv_analysis, user_data.get('job_applications', []))
            
            insights = []
            
            # High-demand skills trend
            trending_skills = self.market_trends['high_demand_skills'][:4]
            insights.append({
                'type': 'market_trend',
                'title': 'High-Demand Skills in Current Market',
                'content': f"The current job market shows high demand for skills in: {', '.join(trending_skills)}. Consider incorporating these into your skill set to increase job opportunities.",
                'confidence': 0.8,
                'priority': 3,
                'action_required': True,
                'action_text': 'Research trending skills in your field',
                'related_skills': trending_skills
            })
            
            # Emerging skills opportunity
            emerging_skills = self.market_trends['emerging_skills'][:3]
            insights.append({
                'type': 'emerging_opportunity',
                'title': 'Emerging Technology Opportunities',
                'content': f"Keep an eye on emerging technologies like: {', '.join(emerging_skills)}. Early adoption of these skills could give you a competitive advantage.",
                'confidence': 0.7,
                'priority': 2,
                'action_required': False,
                'action_text': 'Stay informed about emerging technologies'
            })
            
            # Salary growth areas
            high_growth_skills = self.market_trends['salary_growth_skills'][:3]
            insights.append({
                'type': 'salary_growth',
                'title': 'Skills with High Salary Growth Potential',
                'content': f"Skills showing the highest salary growth include: {', '.join(high_growth_skills)}. Developing expertise in these areas could lead to significant salary increases.",
                'confidence': 0.75,
                'priority': 3,
                'action_required': True,
                'action_text': 'Evaluate salary growth potential in career planning',
                'related_skills': high_growth_skills
            })
            
            return insights
            
        except Exception as e:
            return [self._create_error_insight(str(e))]
    
    def predict_success_probability(self, user_data):
        """Predict job search success probability"""
        try:
            cv_analysis = user_data.get('cv_analysis', {})
            job_applications = user_data.get('job_applications', [])
            
            insights = []
            
            # Calculate success factors
            success_factors = self._calculate_success_factors(cv_analysis, job_applications)
            
            # Overall success prediction
            overall_probability = success_factors['overall_score']
            
            if overall_probability >= 80:
                insights.append({
                    'type': 'success_prediction',
                    'title': 'High Success Probability',
                    'content': f"Based on your profile analysis, you have a {overall_probability}% probability of success in your job search. Your strong skill set and experience level align well with market demands.",
                    'confidence': 0.9,
                    'priority': 4,
                    'action_required': False
                })
            elif overall_probability >= 60:
                insights.append({
                    'type': 'success_prediction',
                    'title': 'Good Success Potential',
                    'content': f"Your job search success probability is {overall_probability}%. With some targeted improvements, you could significantly increase your chances of landing your desired role.",
                    'confidence': 0.8,
                    'priority': 4,
                    'action_required': True,
                    'action_text': 'Focus on highlighted improvement areas'
                })
            else:
                insights.append({
                    'type': 'success_prediction',
                    'title': 'Improvement Opportunities',
                    'content': f"Your current success probability is {overall_probability}%. Consider the recommendations below to improve your job search strategy and skill set.",
                    'confidence': 0.7,
                    'priority': 5,
                    'action_required': True,
                    'action_text': 'Implement recommended improvements'
                })
            
            # Specific improvement areas
            improvement_areas = success_factors.get('improvement_areas', [])
            if improvement_areas:
                insights.append({
                    'type': 'improvement_areas',
                    'title': 'Key Areas for Improvement',
                    'content': f"Focus on these areas to boost your success: {', '.join(improvement_areas[:3])}. Each area has specific strategies that could increase your job match scores.",
                    'confidence': 0.8,
                    'priority': 5,
                    'action_required': True,
                    'action_text': 'Create action plan for improvement areas'
                })
            
            return insights
            
        except Exception as e:
            return [self._create_error_insight(str(e))]
    
    def generate_all_insights(self, user_data):
        """Generate all types of insights for a user"""
        all_insights = []
        
        # Career path insights
        career_insights = self.analyze_career_path(user_data)
        all_insights.extend(career_insights)
        
        # Skill gap insights
        skill_insights = self.analyze_skill_gaps(user_data)
        all_insights.extend(skill_insights)
        
        # Market trend insights
        market_insights = self.analyze_market_trends(user_data)
        all_insights.extend(market_insights)
        
        # Success prediction insights
        success_insights = self.predict_success_probability(user_data)
        all_insights.extend(success_insights)
        
        # Sort by priority and confidence
        all_insights.sort(key=lambda x: (x['priority'], -x['confidence']), reverse=True)
        
        return all_insights
    
    # Helper methods
    def _determine_career_stage(self, cv_analysis, job_history):
        """Determine user's current career stage"""
        experience_level = cv_analysis.get('experience_level', 'unknown')
        years_experience = cv_analysis.get('years_experience', 0)
        
        if experience_level == 'junior' or years_experience <= 2:
            return 'entry_level'
        elif experience_level == 'mid' or 2 < years_experience <= 7:
            return 'mid_level'
        elif experience_level == 'senior' or years_experience > 7:
            return 'senior_level'
        else:
            return 'mid_level'  # Default
    
    def _identify_industry(self, cv_analysis, job_history):
        """Identify user's industry based on skills and job applications"""
        skills = cv_analysis.get('extracted_skills', [])
        
        # Simple industry identification based on skills
        if any(skill.lower() in ['python', 'java', 'javascript', 'programming'] for skill in skills):
            return 'technology'
        elif any(skill.lower() in ['data', 'analytics', 'statistics'] for skill in skills):
            return 'data_science'
        elif any(skill.lower() in ['marketing', 'seo', 'social media'] for skill in skills):
            return 'marketing'
        else:
            return 'technology'  # Default to tech
    
    def _get_career_progression_path(self, industry, current_stage):
        """Get career progression path for industry and stage"""
        if industry in self.career_patterns:
            path = self.career_patterns[industry]['progression_path']
            stage_index = {
                'entry_level': 0,
                'mid_level': 2,
                'senior_level': 3
            }.get(current_stage, 0)
            return path[stage_index:]
        return []
    
    def _get_stage_skills(self, stage):
        """Get key skills for career stage"""
        stage_skills = {
            'entry_level': ['Technical Fundamentals', 'Learning Agility', 'Communication', 'Team Collaboration'],
            'mid_level': ['Technical Expertise', 'Project Management', 'Mentoring', 'Problem Solving'],
            'senior_level': ['Leadership', 'Strategic Thinking', 'Technical Architecture', 'Stakeholder Management']
        }
        return stage_skills.get(stage, ['Professional Development'])
    
    def _get_skill_priorities(self, industry, stage):
        """Get priority skills for career stage and industry"""
        if industry in self.career_patterns:
            return self.career_patterns[industry]['key_skills']
        return ['Communication', 'Technical Skills', 'Leadership']
    
    def _extract_all_job_skills(self, job_applications):
        """Extract all skills from job applications"""
        all_skills = []
        for job in job_applications:
            # This would use job matcher's skill extraction in real implementation
            # For now, using placeholder logic
            position = job.get('position', '').lower()
            if 'developer' in position:
                all_skills.extend(['programming', 'problem solving'])
            elif 'analyst' in position:
                all_skills.extend(['data analysis', 'statistics'])
        return list(set(all_skills))
    
    def _identify_high_priority_gaps(self, skill_gaps):
        """Identify high-priority skill gaps"""
        # Prioritize based on market demand
        high_demand = ['programming', 'data analysis', 'cloud computing', 'machine learning']
        return [skill for skill in skill_gaps if skill.lower() in [hd.lower() for hd in high_demand]] or skill_gaps[:3]
    
    def _get_learning_resources(self, skill_gaps):
        """Get learning resources for skill gaps"""
        # Placeholder - would integrate with actual learning platforms
        return {
            'programming': ['Online coding bootcamps', 'GitHub projects', 'Technical documentation'],
            'data analysis': ['Data science courses', 'Kaggle competitions', 'Real-world datasets']
        }
    
    def _calculate_skills_strength(self, current_skills, required_skills):
        """Calculate skills strength score"""
        if not required_skills:
            return 100
        matches = len(set(skill.lower() for skill in current_skills) & set(skill.lower() for skill in required_skills))
        return (matches / len(required_skills)) * 100
    
    def _calculate_success_factors(self, cv_analysis, job_applications):
        """Calculate success prediction factors"""
        factors = {
            'cv_quality': cv_analysis.get('ats_score', 0),
            'skills_relevance': len(cv_analysis.get('extracted_skills', [])),
            'experience_alignment': 75,  # Simplified
            'application_quality': 80    # Simplified
        }
        
        # Calculate overall score
        overall_score = sum(factors.values()) / len(factors)
        
        # Identify improvement areas
        improvement_areas = []
        if factors['cv_quality'] < 70:
            improvement_areas.append('CV optimization')
        if factors['skills_relevance'] < 5:
            improvement_areas.append('skill development')
        if factors['experience_alignment'] < 70:
            improvement_areas.append('experience alignment')
        
        return {
            'overall_score': overall_score,
            'improvement_areas': improvement_areas,
            'factors': factors
        }
    
    def _create_error_insight(self, error_message):
        """Create error insight"""
        return {
            'type': 'error',
            'title': 'Analysis Error',
            'content': f"An error occurred during insight generation: {error_message}",
            'confidence': 0.0,
            'priority': 1,
            'action_required': False
        }
