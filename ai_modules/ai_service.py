"""
AI Service Module
Main AI service that integrates all AI modules and provides unified interface
"""

import json
import os
from datetime import datetime
from .nlp_processor import NLPProcessor
from .cv_analyzer import CVAnalyzer
from .job_matcher import JobMatcher
from .insights_generator import InsightsGenerator

class AIService:
    """Main AI service for job tracker application"""
    
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.cv_analyzer = CVAnalyzer()
        self.job_matcher = JobMatcher()
        self.insights_generator = InsightsGenerator()
    
    def analyze_cv(self, cv_file_path, file_size):
        """Complete CV analysis"""
        try:
            return self.cv_analyzer.analyze_cv(cv_file_path, file_size)
        except Exception as e:
            return {'error': str(e), 'analysis_date': datetime.now().isoformat()}
    
    def get_cv_recommendations(self, analysis_results):
        """Get recommendations based on CV analysis"""
        try:
            return self.cv_analyzer.get_recommendations(analysis_results)
        except Exception as e:
            return [{'type': 'error', 'title': 'Analysis Error', 'description': str(e)}]
    
    def match_job(self, cv_analysis, job_data):
        """Analyze job compatibility"""
        try:
            return self.job_matcher.analyze_job_compatibility(cv_analysis, job_data)
        except Exception as e:
            return {'error': str(e), 'analysis_date': datetime.now().isoformat()}
    
    def batch_match_jobs(self, cv_analysis, job_applications):
        """Analyze multiple jobs for compatibility"""
        try:
            return self.job_matcher.batch_analyze_jobs(cv_analysis, job_applications)
        except Exception as e:
            return [{'error': str(e), 'job_id': 'unknown'}]
    
    def get_top_job_matches(self, cv_analysis, job_applications, limit=5):
        """Get top N job matches"""
        try:
            return self.job_matcher.get_top_matches(cv_analysis, job_applications, limit)
        except Exception as e:
            return [{'error': str(e)}]
    
    def generate_insights(self, user_data):
        """Generate AI-powered insights"""
        try:
            return self.insights_generator.generate_all_insights(user_data)
        except Exception as e:
            return [{
                'type': 'error',
                'title': 'Insights Generation Error',
                'content': f"Error generating insights: {str(e)}",
                'confidence': 0.0,
                'priority': 1,
                'action_required': False
            }]
    
    def analyze_career_path(self, user_data):
        """Generate career path insights"""
        try:
            return self.insights_generator.analyze_career_path(user_data)
        except Exception as e:
            return [{
                'type': 'error',
                'title': 'Career Path Analysis Error',
                'content': f"Error analyzing career path: {str(e)}",
                'confidence': 0.0,
                'priority': 1,
                'action_required': False
            }]
    
    def analyze_skill_gaps(self, user_data):
        """Analyze skill gaps"""
        try:
            return self.insights_generator.analyze_skill_gaps(user_data)
        except Exception as e:
            return [{
                'type': 'error',
                'title': 'Skill Gap Analysis Error',
                'content': f"Error analyzing skill gaps: {str(e)}",
                'confidence': 0.0,
                'priority': 1,
                'action_required': False
            }]
    
    def analyze_market_trends(self, user_data):
        """Analyze market trends"""
        try:
            return self.insights_generator.analyze_market_trends(user_data)
        except Exception as e:
            return [{
                'type': 'error',
                'title': 'Market Trends Analysis Error',
                'content': f"Error analyzing market trends: {str(e)}",
                'confidence': 0.0,
                'priority': 1,
                'action_required': False
            }]
    
    def predict_success(self, user_data):
        """Predict job search success"""
        try:
            return self.insights_generator.predict_success_probability(user_data)
        except Exception as e:
            return [{
                'type': 'error',
                'title': 'Success Prediction Error',
                'content': f"Error predicting success: {str(e)}",
                'confidence': 0.0,
                'priority': 1,
                'action_required': False
            }]
    
    def process_cv_text(self, text):
        """Process CV text using NLP"""
        try:
            return self.nlp_processor.process_cv_text(text)
        except Exception as e:
            return {
                'error': str(e),
                'extracted_skills': [],
                'keywords': [],
                'contact_info': {},
                'text_analysis': {},
                'ats_score': 0,
                'completeness_score': 0
            }
    
    def extract_skills_from_text(self, text):
        """Extract skills from text"""
        try:
            return self.nlp_processor.extract_skills(text)
        except Exception as e:
            return []
    
    def calculate_ats_score(self, text, extracted_skills):
        """Calculate ATS compatibility score"""
        try:
            return self.nlp_processor.calculate_ats_score(text, extracted_skills)
        except Exception as e:
            return 0
    
    def get_comprehensive_analysis(self, cv_file_path, file_size, job_applications=None):
        """Get comprehensive AI analysis including CV, job matching, and insights"""
        try:
            # Analyze CV
            cv_analysis = self.analyze_cv(cv_file_path, file_size)
            
            if 'error' in cv_analysis:
                return cv_analysis
            
            # Initialize comprehensive data
            user_data = {
                'cv_analysis': cv_analysis,
                'job_applications': job_applications or []
            }
            
            # Generate insights
            insights = self.generate_insights(user_data)
            
            # Job matching if job applications provided
            job_matches = []
            if job_applications:
                job_matches = self.batch_match_jobs(cv_analysis, job_applications)
            
            # Compile comprehensive results
            comprehensive_analysis = {
                'cv_analysis': cv_analysis,
                'insights': insights,
                'job_matches': job_matches,
                'analysis_summary': {
                    'total_insights': len(insights),
                    'job_matches_found': len(job_matches),
                    'top_match_score': max([match.get('overall_match_score', 0) for match in job_matches]) if job_matches else 0,
                    'cv_ats_score': cv_analysis.get('ats_score', 0),
                    'cv_completeness_score': cv_analysis.get('completeness_score', 0),
                    'skills_count': len(cv_analysis.get('extracted_skills', [])),
                    'analysis_date': datetime.now().isoformat()
                }
            }
            
            return comprehensive_analysis
            
        except Exception as e:
            return {
                'error': f"Comprehensive analysis failed: {str(e)}",
                'analysis_date': datetime.now().isoformat()
            }
    
    def get_quick_insights(self, user_data):
        """Get quick insights for dashboard"""
        try:
            insights = self.generate_insights(user_data)
            
            # Filter high-priority insights
            high_priority_insights = [
                insight for insight in insights 
                if insight.get('priority', 1) >= 4
            ][:5]  # Top 5 high-priority insights
            
            return {
                'high_priority_insights': high_priority_insights,
                'total_insights': len(insights),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'high_priority_insights': [],
                'total_insights': 0,
                'error': str(e),
                'generated_at': datetime.now().isoformat()
            }
    
    def get_skill_recommendations(self, cv_analysis, job_applications):
        """Get skill development recommendations"""
        try:
            # Extract current skills
            current_skills = cv_analysis.get('extracted_skills', [])
            
            # Get skill gaps from job applications
            user_data = {
                'cv_analysis': cv_analysis,
                'job_applications': job_applications
            }
            
            skill_gaps = self.analyze_skill_gaps(user_data)
            
            # Extract recommended skills from insights
            recommended_skills = []
            for insight in skill_gaps:
                if insight.get('type') == 'critical_skill_gaps':
                    recommended_skills.extend(insight.get('related_skills', []))
            
            # Remove skills user already has
            current_skills_lower = [skill.lower() for skill in current_skills]
            unique_recommendations = [
                skill for skill in recommended_skills 
                if skill.lower() not in current_skills_lower
            ]
            
            return {
                'current_skills': current_skills,
                'recommended_skills': unique_recommendations[:10],  # Top 10
                'skill_gaps_count': len(unique_recommendations),
                'priority_skills': unique_recommendations[:5]  # Top 5 priority
            }
            
        except Exception as e:
            return {
                'current_skills': [],
                'recommended_skills': [],
                'skill_gaps_count': 0,
                'priority_skills': [],
                'error': str(e)
            }
    
    def validate_ai_dependencies(self):
        """Validate that all AI dependencies are available"""
        try:
            # Test NLP processor
            test_text = "Python programming and machine learning experience"
            nlp_result = self.nlp_processor.extract_skills(test_text)
            
            # Test CV analyzer (basic initialization)
            cv_analyzer_ok = True
            
            # Test job matcher
            test_job = {'position': 'Software Developer', 'company_name': 'Tech Corp'}
            job_matcher_ok = True
            
            # Test insights generator
            test_user_data = {'cv_analysis': {'extracted_skills': ['python']}, 'job_applications': []}
            insights_ok = True
            
            return {
                'status': 'success',
                'nlp_processor': 'working' if nlp_result else 'error',
                'cv_analyzer': 'working' if cv_analyzer_ok else 'error',
                'job_matcher': 'working' if job_matcher_ok else 'error',
                'insights_generator': 'working' if insights_ok else 'error',
                'validation_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'validation_date': datetime.now().isoformat()
            }

# Global AI service instance
ai_service = AIService()
