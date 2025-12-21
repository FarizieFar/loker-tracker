"""
Job Matcher Module
Analyzes job compatibility between CV skills and job requirements
"""

import json
import re
from datetime import datetime
from difflib import SequenceMatcher

class JobMatcher:
    """AI-powered job matching and compatibility analysis"""
    
    def __init__(self):
        # Common job requirement patterns
        self.requirement_patterns = {
            'programming': [
                r'python\s+developer', r'java\s+developer', r'javascript\s+developer',
                r'c\+\+\s+developer', r'software\s+engineer', r'web\s+developer',
                r'full\s+stack', r'frontend\s+developer', r'backend\s+developer',
                r'programming', r'coding', r'development'
            ],
            'data_science': [
                r'data\s+scientist', r'data\s+analyst', r'machine\s+learning',
                r'artificial\s+intelligence', r'big\s+data', r'business\s+intelligence',
                r'statistics', r'data\s+analysis', r'predictive\s+modeling'
            ],
            'design': [
                r'graphic\s+designer', r'ui\s+designer', r'ux\s+designer',
                r'web\s+designer', r'creative\s+director', r'visual\s+designer',
                r'brand\s+designer', r'digital\s+designer'
            ],
            'marketing': [
                r'digital\s+marketing', r'content\s+marketing', r'social\s+media',
                r'seo\s+specialist', r'growth\s+hacker', r'brand\s+manager',
                r'marketing\s+manager', r'performance\s+marketing'
            ],
            'management': [
                r'project\s+manager', r'product\s+manager', r'team\s+lead',
                r'scrum\s+master', r'operations\s+manager', r'general\s+manager',
                r'branch\s+manager', r'regional\s+manager'
            ]
        }
        
        # Skill importance weights
        self.skill_weights = {
            'programming': 1.0,
            'data_science': 1.2,  # Higher weight for specialized skills
            'tools': 0.8,
            'soft_skills': 0.6
        }
        
        # Experience level scoring
        self.experience_scoring = {
            'junior': {'junior': 90, 'mid': 70, 'senior': 40},
            'mid': {'junior': 95, 'mid': 85, 'senior': 70},
            'senior': {'junior': 100, 'mid': 95, 'senior': 85},
            'expert': {'junior': 100, 'mid': 100, 'senior': 95}
        }
    
    def extract_job_requirements(self, job_data):
        """Extract job requirements from job application data"""
        if not job_data:
            return {}
        
        requirements = {
            'position': job_data.get('position', ''),
            'company': job_data.get('company_name', ''),
            'location': job_data.get('location', ''),
            'source_info': job_data.get('source_info', ''),
            'notes': job_data.get('notes', ''),
            'status': job_data.get('status', {})
        }
        
        # Combine all text for analysis
        text_to_analyze = ' '.join([
            requirements['position'],
            requirements['company'],
            requirements['location'],
            requirements['source_info'],
            requirements['notes']
        ])
        
        # Extract skills from job description
        requirements['extracted_skills'] = self._extract_skills_from_text(text_to_analyze)
        
        # Determine experience level required
        requirements['experience_required'] = self._determine_experience_required(text_to_analyze)
        
        # Determine job category
        requirements['job_category'] = self._categorize_job(text_to_analyze)
        
        return requirements
    
    def _extract_skills_from_text(self, text):
        """Extract skills and keywords from job description"""
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = []
        
        # Common technical skills
        technical_skills = [
            'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
            'machine learning', 'deep learning', 'data science', 'ai',
            'tableau', 'power bi', 'excel', 'statistics',
            'project management', 'agile', 'scrum', 'kanban'
        ]
        
        # Find matching skills
        for skill in technical_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    def _determine_experience_required(self, text):
        """Determine required experience level from job description"""
        if not text:
            return 'unknown'
        
        text_lower = text.lower()
        
        # Experience patterns
        senior_patterns = [
            'senior', 'lead', 'principal', 'architect', '5+ years', '7+ years',
            '10+ years', 'experienced', 'team lead', 'technical lead'
        ]
        
        junior_patterns = [
            'junior', 'entry level', 'fresh graduate', 'new grad', '0-2 years',
            '1-2 years', 'trainee', 'intern', 'beginner'
        ]
        
        # Check for senior requirements
        for pattern in senior_patterns:
            if pattern in text_lower:
                return 'senior'
        
        # Check for junior requirements
        for pattern in junior_patterns:
            if pattern in text_lower:
                return 'junior'
        
        # Default to mid-level if no specific level mentioned
        return 'mid'
    
    def _categorize_job(self, text):
        """Categorize job based on description"""
        if not text:
            return 'other'
        
        text_lower = text.lower()
        
        for category, patterns in self.requirement_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return category
        
        return 'other'
    
    def calculate_skill_match_score(self, cv_skills, job_skills):
        """Calculate skill compatibility score"""
        if not cv_skills and not job_skills:
            return 50  # Neutral score
        
        if not cv_skills:
            return 20  # No CV skills
        
        if not job_skills:
            return 80  # Job has no specific requirements
        
        # Convert to lowercase for comparison
        cv_skills_lower = [skill.lower() for skill in cv_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        # Find exact matches
        exact_matches = set(cv_skills_lower) & set(job_skills_lower)
        
        # Find partial matches using similarity
        partial_matches = []
        for cv_skill in cv_skills_lower:
            for job_skill in job_skills_lower:
                if cv_skill != job_skill:
                    similarity = SequenceMatcher(None, cv_skill, job_skill).ratio()
                    if similarity > 0.7:  # 70% similarity threshold
                        partial_matches.append((cv_skill, job_skill, similarity))
        
        # Calculate scores
        exact_score = len(exact_matches) / len(job_skills_lower) * 100 if job_skills_lower else 0
        partial_score = len(partial_matches) / len(job_skills_lower) * 100 if job_skills_lower else 0
        
        # Weight exact matches higher than partial
        total_score = (exact_score * 0.8) + (partial_score * 0.2)
        
        return min(100, total_score)
    
    def calculate_experience_match_score(self, cv_experience_level, job_experience_required):
        """Calculate experience level compatibility"""
        if not cv_experience_level or not job_experience_required:
            return 70  # Default score if levels unknown
        
        cv_level = cv_experience_level.lower()
        job_level = job_experience_required.lower()
        
        # Use scoring matrix
        if cv_level in self.experience_scoring and job_level in self.experience_scoring[cv_level]:
            return self.experience_scoring[cv_level][job_level]
        
        # Fallback scoring
        if cv_level == job_level:
            return 90
        elif cv_level == 'senior' and job_level == 'mid':
            return 85
        elif cv_level == 'mid' and job_level == 'junior':
            return 85
        elif cv_level == 'junior' and job_level == 'mid':
            return 70
        else:
            return 60
    
    def calculate_location_match_score(self, cv_location, job_location):
        """Calculate location compatibility score"""
        if not cv_location and not job_location:
            return 100  # No location constraints
        
        if not job_location:
            return 100  # Job has no location preference
        
        if not cv_location:
            return 50  # CV has no location specified
        
        # Simple location matching (can be enhanced with geocoding)
        cv_location_lower = cv_location.lower()
        job_location_lower = job_location.lower()
        
        # Exact match
        if cv_location_lower == job_location_lower:
            return 100
        
        # Partial match (same city/province)
        cv_parts = cv_location_lower.split()
        job_parts = job_location_lower.split()
        
        for cv_part in cv_parts:
            for job_part in job_parts:
                if len(cv_part) > 3 and len(job_part) > 3:
                    similarity = SequenceMatcher(None, cv_part, job_part).ratio()
                    if similarity > 0.8:
                        return 80
        
        # Different locations but both in same country/region
        return 60
    
    def analyze_job_compatibility(self, cv_analysis, job_data):
        """Complete job compatibility analysis"""
        try:
            # Extract job requirements
            job_requirements = self.extract_job_requirements(job_data)
            
            # Calculate individual scores
            skill_score = self.calculate_skill_match_score(
                cv_analysis.get('extracted_skills', []),
                job_requirements.get('extracted_skills', [])
            )
            
            experience_score = self.calculate_experience_match_score(
                cv_analysis.get('experience_level', ''),
                job_requirements.get('experience_required', '')
            )
            
            location_score = self.calculate_location_match_score(
                cv_analysis.get('contact_info', {}).get('location', ''),
                job_requirements.get('location', '')
            )
            
            # Calculate overall match score (weighted average)
            weights = {
                'skills': 0.6,      # Skills are most important
                'experience': 0.3,   # Experience level is important
                'location': 0.1      # Location has lower weight
            }
            
            overall_score = (
                skill_score * weights['skills'] +
                experience_score * weights['experience'] +
                location_score * weights['location']
            )
            
            # Identify matching and missing skills
            cv_skills = [skill.lower() for skill in cv_analysis.get('extracted_skills', [])]
            job_skills = [skill.lower() for skill in job_requirements.get('extracted_skills', [])]
            
            matching_skills = list(set(cv_skills) & set(job_skills))
            missing_skills = list(set(job_skills) - set(cv_skills))
            additional_skills = list(set(cv_skills) - set(job_skills))
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                overall_score, matching_skills, missing_skills, job_requirements
            )
            
            # Compile results
            match_results = {
                'overall_match_score': round(overall_score, 1),
                'skill_match_score': round(skill_score, 1),
                'experience_match_score': round(experience_score, 1),
                'location_match_score': round(location_score, 1),
                'matching_skills': matching_skills,
                'missing_skills': missing_skills,
                'additional_skills': additional_skills,
                'job_requirements': job_requirements,
                'recommendations': recommendations,
                'analysis_date': datetime.now().isoformat(),
                'match_level': self._get_match_level(overall_score)
            }
            
            return match_results
            
        except Exception as e:
            raise Exception(f"Error analyzing job compatibility: {str(e)}")
    
    def _generate_recommendations(self, overall_score, matching_skills, missing_skills, job_requirements):
        """Generate personalized recommendations for job application"""
        recommendations = []
        
        # Overall match level recommendations
        if overall_score >= 80:
            recommendations.append({
                'type': 'encouragement',
                'priority': 'high',
                'title': 'Strong Match!',
                'description': 'You have excellent qualifications for this position. Consider highlighting your matching skills in your application.'
            })
        elif overall_score >= 60:
            recommendations.append({
                'type': 'improvement',
                'priority': 'medium',
                'title': 'Good Match with Room for Improvement',
                'description': 'You meet many of the requirements. Focus on your strong points and address any skill gaps in your application.'
            })
        else:
            recommendations.append({
                'type': 'development',
                'priority': 'medium',
                'title': 'Consider Skill Development',
                'description': 'This role may require additional skills. Consider what you can learn quickly or how to emphasize transferable skills.'
            })
        
        # Skill-specific recommendations
        if missing_skills:
            high_priority_skills = missing_skills[:3]  # Top 3 missing skills
            recommendations.append({
                'type': 'skill_gap',
                'priority': 'high',
                'title': 'Address Skill Gaps',
                'description': f'Consider highlighting these relevant skills you might have: {", ".join(high_priority_skills[:2])}. If you lack them, consider quick learning or emphasizing related experience.',
                'skills_to_highlight': high_priority_skills
            })
        
        # Experience recommendations
        job_experience = job_requirements.get('experience_required', 'unknown')
        if job_experience == 'senior':
            recommendations.append({
                'type': 'experience',
                'priority': 'medium',
                'title': 'Emphasize Leadership Experience',
                'description': 'This role requires senior-level experience. Highlight any leadership roles, mentoring, or project management experience.'
            })
        elif job_experience == 'junior':
            recommendations.append({
                'type': 'experience',
                'priority': 'medium',
                'title': 'Highlight Growth Potential',
                'description': 'This entry-level role values learning ability. Emphasize your enthusiasm, quick learning, and any relevant projects or coursework.'
            })
        
        # Application strategy recommendations
        if overall_score >= 70:
            recommendations.append({
                'type': 'application_strategy',
                'priority': 'high',
                'title': 'Strong Application Strategy',
                'description': 'Tailor your cover letter to emphasize your strongest matching qualifications. Prepare specific examples of how you\'ve used these skills.'
            })
        
        # Location considerations
        job_location = job_requirements.get('location', '')
        if job_location:
            recommendations.append({
                'type': 'logistics',
                'priority': 'low',
                'title': 'Location Considerations',
                'description': f'Consider the location requirement ({job_location}) and be prepared to discuss relocation or remote work preferences.'
            })
        
        return recommendations
    
    def _get_match_level(self, score):
        """Convert numerical score to match level"""
        if score >= 80:
            return 'excellent'
        elif score >= 65:
            return 'good'
        elif score >= 50:
            return 'fair'
        else:
            return 'poor'
    
    def batch_analyze_jobs(self, cv_analysis, job_applications):
        """Analyze multiple jobs for compatibility"""
        results = []
        
        for job in job_applications:
            try:
                match_result = self.analyze_job_compatibility(cv_analysis, job)
                match_result['job_id'] = job.get('id')
                results.append(match_result)
            except Exception as e:
                # Log error but continue with other jobs
                print(f"Error analyzing job {job.get('id', 'unknown')}: {str(e)}")
                continue
        
        # Sort by overall match score (highest first)
        results.sort(key=lambda x: x['overall_match_score'], reverse=True)
        
        return results
    
    def get_top_matches(self, cv_analysis, job_applications, limit=5):
        """Get top N job matches"""
        batch_results = self.batch_analyze_jobs(cv_analysis, job_applications)
        return batch_results[:limit]
