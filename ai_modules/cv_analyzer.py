"""
CV Analyzer Module
Handles CV/Resume upload, parsing, and analysis
"""

import os
import io
import json
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

# PDF processing
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# DOCX processing
try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

from .nlp_processor import NLPProcessor
from .critical_analyzer import CriticalAnalyzer
from .feedback_generator import FeedbackGenerator

class CVAnalyzer:
    """CV/Resume analyzer with PDF and DOCX support"""
    
    def __init__(self):
        self.nlp = NLPProcessor()
        self.critical_analyzer = CriticalAnalyzer()
        self.feedback_generator = FeedbackGenerator()
        self.allowed_extensions = {'pdf', 'docx', 'txt'}
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        
        # File upload directory
        self.upload_dir = 'static/uploads/cv'
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def save_cv_file(self, file):
        """Save uploaded CV file and return file path"""
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add unique identifier
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(self.upload_dir, unique_filename)
            file.save(file_path)
            return unique_filename
        return None
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        if not PDF_AVAILABLE:
            raise ImportError("PyPDF2 not available for PDF processing")
        
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx not available for DOCX processing")
        
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
    
    def extract_text_from_txt(self, file_path):
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")
    
    def extract_text(self, file_path):
        """Extract text from CV file based on extension"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = file_path.split('.')[-1].lower()
        
        if file_ext == 'pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_ext == 'docx':
            return self.extract_text_from_docx(file_path)
        elif file_ext == 'txt':
            return self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def analyze_experience_level(self, text):
        """Determine experience level from CV text"""
        if not text:
            return "unknown"
        
        text_lower = text.lower()
        
        # Look for experience indicators
        experience_patterns = {
            'senior': [
                'senior', 'lead', 'principal', 'architect', 'manager', 'director',
                '10+ years', '10+ tahun', 'senior engineer', 'team lead',
                'project manager', 'technical lead'
            ],
            'mid': [
                'mid-level', 'intermediate', '3-5 years', '4-6 years', '5+ years',
                'software engineer', 'developer', 'programmer', 'analyst',
                'specialist', 'consultant'
            ],
            'junior': [
                'junior', 'entry-level', 'fresh graduate', 'new grad',
                '0-2 years', '1-2 years', 'internship', 'trainee',
                'associate', 'beginner'
            ]
        }
        
        # Count pattern matches
        level_scores = {}
        for level, patterns in experience_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            level_scores[level] = score
        
        # Determine highest scoring level
        if max(level_scores.values()) == 0:
            return "unknown"
        
        return max(level_scores, key=level_scores.get)
    
    def analyze_education_level(self, text):
        """Extract education level from CV text"""
        if not text:
            return "unknown"
        
        text_lower = text.lower()
        
        education_patterns = {
            'phd': ['phd', 'doctorate', 'doctoral', 'ph.d'],
            'masters': ['master', 'mba', 'm.sc', 'm.s', 'msc', 'ms'],
            'bachelors': ['bachelor', 'b.sc', 'b.s', 'bsc', 'bs', 'diploma', 'sarjana'],
            'associate': ['associate', 'diploma', 'certificate'],
            'high_school': ['high school', 'secondary', 'sma', 'smk']
        }
        
        for level, patterns in education_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return level
        
        return "unknown"
    
    def estimate_years_experience(self, text):
        """Estimate years of experience from CV text"""
        if not text:
            return 0
        
        # Look for years patterns
        import re
        
        # Pattern untuk mencari pengalaman dalam tahun
        year_patterns = [
            r'(\d+)\+?\s*years?\s*(of\s*)?experience',
            r'experience\s*(of\s*)?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in\s*(the\s*)?(field|industry)',
            r'(\d+)\+?\s*years?\s*as\s*(a\s*)?(developer|engineer|analyst)',
        ]
        
        max_years = 0
        
        for pattern in year_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                # Handle both direct years and years from groups
                years = int(match[0] if match[0] else match[1])
                max_years = max(max_years, years)
        
        # If no explicit years found, estimate from text length and content
        if max_years == 0:
            word_count = len(text.split())
            if word_count > 1000:  # Long CV might indicate experience
                max_years = 3  # Conservative estimate
        
        return max_years
    
    def detect_industry(self, text, extracted_skills):
        """Detect likely industry based on text content and skills"""
        if not text:
            return "unknown"
        
        text_lower = text.lower()
        skills_lower = [skill.lower() for skill in extracted_skills]
        
        # Industry detection patterns
        industry_indicators = {
            'technology': {
                'text_keywords': ['software', 'development', 'programming', 'tech', 'digital', 'ai', 'data science', 'cloud'],
                'skills': ['python', 'java', 'javascript', 'react', 'node.js', 'aws', 'docker', 'kubernetes']
            },
            'finance': {
                'text_keywords': ['financial', 'banking', 'investment', 'trading', 'accounting', 'audit', 'compliance', 'risk'],
                'skills': ['bloomberg', 'excel', 'financial modeling', 'cfa', 'cpa', 'risk management']
            },
            'healthcare': {
                'text_keywords': ['medical', 'health', 'clinical', 'patient', 'hospital', 'pharmaceutical', 'nursing'],
                'skills': ['medical coding', 'hipaa', 'patient care', 'clinical', 'nursing', 'healthcare']
            },
            'marketing': {
                'text_keywords': ['marketing', 'advertising', 'brand', 'campaign', 'digital marketing', 'social media'],
                'skills': ['seo', 'google ads', 'facebook ads', 'content marketing', 'analytics', 'crm']
            },
            'sales': {
                'text_keywords': ['sales', 'revenue', 'client', 'customer', 'account', 'territory', 'quota'],
                'skills': ['crm', 'salesforce', 'lead generation', 'negotiation', 'pipeline management']
            },
            'education': {
                'text_keywords': ['teaching', 'education', 'academic', 'curriculum', 'student', 'learning'],
                'skills': ['curriculum development', 'instructional design', 'assessment', 'lms']
            },
            'legal': {
                'text_keywords': ['legal', 'law', 'compliance', 'regulatory', 'contract', 'litigation'],
                'skills': ['contract law', 'compliance', 'legal research', 'regulatory affairs']
            },
            'operations': {
                'text_keywords': ['operations', 'supply chain', 'logistics', 'manufacturing', 'quality'],
                'skills': ['supply chain', 'logistics', 'lean', 'six sigma', 'process improvement']
            },
            'hr': {
                'text_keywords': ['human resources', 'recruitment', 'talent', 'employee', 'benefits'],
                'skills': ['recruitment', 'talent acquisition', 'performance management', 'hris']
            },
            'design': {
                'text_keywords': ['design', 'creative', 'visual', 'brand', 'user experience'],
                'skills': ['photoshop', 'illustrator', 'figma', 'ui design', 'ux design', 'branding']
            }
        }
        
        industry_scores = {}
        
        for industry, indicators in industry_indicators.items():
            score = 0
            
            # Score based on text keywords
            for keyword in indicators['text_keywords']:
                if keyword in text_lower:
                    score += 2
            
            # Score based on skills
            for skill in indicators['skills']:
                if any(skill.lower() in extracted_skill for extracted_skill in skills_lower):
                    score += 3
            
            industry_scores[industry] = score
        
        # Return industry with highest score
        if industry_scores:
            best_industry = max(industry_scores, key=industry_scores.get)
            if industry_scores[best_industry] > 0:
                return best_industry
        
        return "general"
    
    def analyze_industry_benchmarks(self, text, extracted_skills, industry):
        """Analyze CV against industry-specific benchmarks"""
        if industry == "unknown" or industry == "general":
            return {}
        
        benchmarks = {
            'technology': {
                'essential_skills': ['programming', 'problem solving', 'debugging', 'version control'],
                'preferred_skills': ['cloud computing', 'agile', 'ci/cd', 'testing'],
                'experience_indicators': ['project management', 'team collaboration', 'technical leadership'],
                'education_preferences': ['computer science', 'software engineering', 'information technology']
            },
            'finance': {
                'essential_skills': ['financial analysis', 'excel', 'financial modeling', 'attention to detail'],
                'preferred_skills': ['bloomberg', 'cfa', 'risk management', 'compliance'],
                'experience_indicators': ['financial reporting', 'audit', 'regulatory knowledge'],
                'education_preferences': ['finance', 'economics', 'accounting', 'business administration']
            },
            'healthcare': {
                'essential_skills': ['patient care', 'medical knowledge', 'communication', 'empathy'],
                'preferred_skills': ['electronic health records', 'medical coding', 'clinical research'],
                'experience_indicators': ['patient outcomes', 'quality improvement', 'regulatory compliance'],
                'education_preferences': ['medicine', 'nursing', 'healthcare administration', 'public health']
            },
            'marketing': {
                'essential_skills': ['communication', 'creativity', 'analytics', 'digital literacy'],
                'preferred_skills': ['seo', 'content marketing', 'social media', 'marketing automation'],
                'experience_indicators': ['campaign management', 'brand development', 'customer acquisition'],
                'education_preferences': ['marketing', 'communications', 'business', 'journalism']
            },
            'sales': {
                'essential_skills': ['communication', 'negotiation', 'relationship building', 'persistence'],
                'preferred_skills': ['crm', 'salesforce', 'lead generation', 'pipeline management'],
                'experience_indicators': ['quota achievement', 'customer retention', 'territory management'],
                'education_preferences': ['sales', 'business', 'communications', 'marketing']
            }
        }
        
        if industry not in benchmarks:
            return {}
        
        benchmark = benchmarks[industry]
        analysis = {
            'industry': industry,
            'essential_skills_match': [],
            'essential_skills_missing': [],
            'preferred_skills_match': [],
            'preferred_skills_missing': [],
            'experience_alignment': 0,
            'education_relevance': 0,
            'benchmark_score': 0
        }
        
        skills_lower = [skill.lower() for skill in extracted_skills]
        
        # Analyze essential skills
        for skill in benchmark['essential_skills']:
            if any(skill.lower() in extracted_skill for extracted_skill in skills_lower):
                analysis['essential_skills_match'].append(skill)
            else:
                analysis['essential_skills_missing'].append(skill)
        
        # Analyze preferred skills
        for skill in benchmark['preferred_skills']:
            if any(skill.lower() in extracted_skill for extracted_skill in skills_lower):
                analysis['preferred_skills_match'].append(skill)
            else:
                analysis['preferred_skills_missing'].append(skill)
        
        # Calculate scores
        essential_match_rate = len(analysis['essential_skills_match']) / len(benchmark['essential_skills'])
        preferred_match_rate = len(analysis['preferred_skills_match']) / len(benchmark['preferred_skills'])
        
        analysis['experience_alignment'] = round(essential_match_rate * 100, 1)
        analysis['education_relevance'] = round(preferred_match_rate * 100, 1)
        analysis['benchmark_score'] = round((essential_match_rate * 0.7 + preferred_match_rate * 0.3) * 100, 1)
        
        return analysis
    
    def generate_summary(self, extracted_data):
        """Generate CV summary based on extracted data"""
        if not extracted_data:
            return "Unable to generate summary."
        
        summary_parts = []
        
        # Skills summary
        skills = extracted_data.get('extracted_skills', [])
        if skills:
            top_skills = skills[:5]  # Top 5 skills
            summary_parts.append(f"Your CV shows expertise in {', '.join(top_skills[:3])}")
            if len(top_skills) > 3:
                summary_parts.append(f"and {len(top_skills) - 3} other technical skills")
        
        # Experience level
        experience_level = extracted_data.get('experience_level', 'unknown')
        if experience_level != 'unknown':
            level_descriptions = {
                'junior': 'entry-level professional with foundational skills',
                'mid': 'experienced professional with solid technical foundation',
                'senior': 'experienced professional with advanced skills and leadership potential'
            }
            summary_parts.append(level_descriptions.get(experience_level, 'professional with experience'))
        
        # Education
        education_level = extracted_data.get('education_level', 'unknown')
        if education_level != 'unknown':
            education_descriptions = {
                'phd': 'holding a doctoral degree',
                'masters': 'with advanced education',
                'bachelors': 'with undergraduate education',
                'associate': 'with specialized education',
                'high_school': 'with secondary education'
            }
            summary_parts.append(education_descriptions.get(education_level, 'with education'))
        
        # ATS score insight
        ats_score = extracted_data.get('ats_score', 0)
        if ats_score >= 80:
            summary_parts.append("Your CV is highly optimized for ATS systems")
        elif ats_score >= 60:
            summary_parts.append("Your CV has good ATS compatibility with room for improvement")
        else:
            summary_parts.append("Consider optimizing your CV for better ATS compatibility")
        
        if not summary_parts:
            return "CV analysis completed. Please review the detailed sections below."
        
        return ". ".join(summary_parts) + "."
    
    def generate_enhanced_summary(self, extracted_data):
        """Generate industry-enhanced CV summary with detailed analysis"""
        if not extracted_data:
            return "Unable to generate summary."
        
        # Generate detailed analysis
        detailed_analysis = self.generate_detailed_cv_analysis(extracted_data)
        
        # Combine summary and detailed analysis
        summary_parts = []
        
        # Basic skills and experience summary
        skills = extracted_data.get('extracted_skills', [])
        if skills:
            top_skills = skills[:5]  # Top 5 skills
            summary_parts.append(f"Your CV demonstrates strong expertise in {', '.join(top_skills[:3])}")
            if len(top_skills) > 3:
                summary_parts.append(f"and {len(top_skills) - 3} other technical competencies")
        
        # industry context
        experience_level = extracted_data.get('experience_level', 'unknown')
        if experience_level != 'unknown':
            level_descriptions = {
                'junior': 'entry-level professional with foundational skills',
                'mid': 'experienced professional with solid technical foundation',
                'senior': 'experienced professional with advanced skills and leadership potential'
            }
            summary_parts.append(level_descriptions.get(experience_level, 'professional with experience'))
        
        # Industry-specific insights
        detected_industry = extracted_data.get('detected_industry', 'general')
        industry_benchmarks = extracted_data.get('industry_benchmarks', {})
        
        if detected_industry != 'general' and industry_benchmarks:
            industry_score = industry_benchmarks.get('benchmark_score', 0)
            if industry_score >= 80:
                summary_parts.append(f"Your profile shows excellent alignment with {detected_industry} industry standards")
            elif industry_score >= 60:
                summary_parts.append(f"You have good potential in the {detected_industry} sector with room for growth")
            else:
                summary_parts.append(f"Consider developing more {detected_industry}-specific skills to strengthen your market position")
        
        # ATS score insight
        ats_score = extracted_data.get('ats_score', 0)
        if ats_score >= 85:
            summary_parts.append("Your CV is highly optimized for ATS systems with excellent formatting and keyword density")
        elif ats_score >= 70:
            summary_parts.append("Your CV shows good ATS compatibility with some opportunities for optimization")
        elif ats_score >= 50:
            summary_parts.append("Your CV could benefit from ATS optimization to improve keyword matching and formatting")
        else:
            summary_parts.append("Significant ATS improvements needed - focus on standard sections and relevant keywords")
        
        # Education level with industry relevance
        education_level = extracted_data.get('education_level', 'unknown')
        if education_level != 'unknown':
            education_descriptions = {
                'phd': 'with doctoral-level expertise',
                'masters': 'with advanced academic qualifications',
                'bachelors': 'with strong undergraduate foundation',
                'associate': 'with specialized technical training',
                'high_school': 'with secondary education background'
            }
            summary_parts.append(education_descriptions.get(education_level, 'with education background'))
        
        # Years of experience context
        years_experience = extracted_data.get('years_experience', 0)
        if years_experience > 0:
            if years_experience >= 10:
                summary_parts.append(f"With {years_experience} years of experience, you bring substantial expertise to potential roles")
            elif years_experience >= 5:
                summary_parts.append(f"Your {years_experience} years of experience demonstrate solid professional growth")
            else:
                summary_parts.append(f"Early career professional with {years_experience} years of practical experience")
        
        if not summary_parts:
            summary_parts = ["CV analysis completed. Please review the detailed sections below for specific insights and recommendations."]
        
        # Combine summary with detailed analysis
        base_summary = ". ".join(summary_parts) + "."
        
        # Add detailed analysis
        if detailed_analysis:
            analysis_text = "\n\n" + "="*60 + "\n"
            analysis_text += "📊 DETAILED CV ANALYSIS & RECOMMENDATIONS\n"
            analysis_text += "="*60 + "\n\n"
            analysis_text += detailed_analysis
            return base_summary + analysis_text
        
        return base_summary
    
    def generate_detailed_cv_analysis(self, extracted_data):
        """Generate detailed CV analysis with strengths, weaknesses, and recommendations"""
        if not extracted_data:
            return ""
        
        analysis_parts = []
        
        # 1. STRENGTHS ANALYSIS
        analysis_parts.append("🎯 CV STRENGTHS:\n")
        strengths = []
        
        skills = extracted_data.get('extracted_skills', [])
        if len(skills) >= 8:
            strengths.append(f"✅ Rich skill portfolio with {len(skills)} identified competencies")
        
        if len(skills) >= 5:
            top_skills = skills[:3]
            strengths.append(f"✅ Strong technical foundation in {', '.join(top_skills)}")
        
        ats_score = extracted_data.get('ats_score', 0)
        if ats_score >= 80:
            strengths.append("✅ Excellent ATS optimization and formatting")
        elif ats_score >= 60:
            strengths.append("✅ Good ATS compatibility with room for improvement")
        
        contact_info = extracted_data.get('contact_info', {})
        if contact_info:
            contact_count = len(contact_info)
            if contact_count >= 2:
                strengths.append("✅ Complete contact information provided")
        
        experience_level = extracted_data.get('experience_level', 'unknown')
        if experience_level == 'senior':
            strengths.append("✅ Senior-level experience demonstrates leadership capability")
        elif experience_level == 'mid':
            strengths.append("✅ Solid mid-level experience with growth potential")
        
        if not strengths:
            strengths.append("✅ Basic CV structure is present")
        
        for strength in strengths:
            analysis_parts.append(f"  {strength}")
        
        # 2. AREAS FOR IMPROVEMENT
        analysis_parts.append("\n⚠️ AREAS FOR IMPROVEMENT:\n")
        improvements = []
        
        if ats_score < 70:
            improvements.append("🔧 ATS Optimization: Improve keyword density and section formatting")
        
        if len(skills) < 5:
            improvements.append("🔧 Skill Documentation: Add more technical skills and competencies")
        
        if len(skills) < 8:
            improvements.append("🔧 Skill Portfolio: Expand skills to include modern technologies and tools")
        
        # Industry-specific improvements
        detected_industry = extracted_data.get('detected_industry', 'general')
        industry_benchmarks = extracted_data.get('industry_benchmarks', {})
        
        if industry_benchmarks and detected_industry != 'general':
            essential_missing = industry_benchmarks.get('essential_skills_missing', [])
            if essential_missing:
                improvements.append(f"🔧 {detected_industry.title()} Industry Skills: Missing essential skills like {', '.join(essential_missing[:2])}")
            
            preferred_missing = industry_benchmarks.get('preferred_skills_missing', [])
            if preferred_missing and len(preferred_missing) <= 3:
                improvements.append(f"🔧 {detected_industry.title()} Preferred Skills: Consider adding {', '.join(preferred_missing[:2])}")
        
        # Contact info improvements
        if not contact_info.get('email'):
            improvements.append("🔧 Contact Information: Add professional email address")
        if not contact_info.get('phone'):
            improvements.append("🔧 Contact Information: Include phone number for easy reach")
        
        # Education improvements
        education_level = extracted_data.get('education_level', 'unknown')
        if education_level == 'unknown':
            improvements.append("🔧 Education Section: Add educational background and qualifications")
        
        if not improvements:
            improvements.append("✅ No major improvement areas identified - CV is well-structured")
        
        for improvement in improvements:
            analysis_parts.append(f"  {improvement}")
        
        # 3. SPECIFIC RECOMMENDATIONS
        analysis_parts.append("\n💡 SPECIFIC RECOMMENDATIONS:\n")
        recommendations = []
        
        # ATS recommendations
        if ats_score < 80:
            recommendations.append("📝 ATS Optimization:")
            recommendations.append("  • Include relevant keywords from job descriptions")
            recommendations.append("  • Use standard section headers (Experience, Education, Skills)")
            recommendations.append("  • Maintain consistent formatting throughout")
            recommendations.append("  • Add action verbs in experience descriptions")
        
        # Skills recommendations
        if len(skills) < 10:
            recommendations.append(f"\n📝 Skills Enhancement:")
            recommendations.append("  • Add 3-5 more relevant technical skills")
            recommendations.append("  • Include both technical and soft skills")
            recommendations.append("  • Group skills by category (Programming, Tools, etc.)")
        
        # Industry-specific recommendations
        if detected_industry != 'general':
            recommendations.append(f"\n📝 {detected_industry.title()} Industry Focus:")
            if detected_industry == 'technology':
                recommendations.append("  • Highlight programming languages and frameworks")
                recommendations.append("  • Mention cloud platforms and DevOps tools")
                recommendations.append("  • Include software development methodologies")
            elif detected_industry == 'finance':
                recommendations.append("  • Emphasize financial modeling and analysis skills")
                recommendations.append("  • Mention relevant certifications (CFA, CPA)")
                recommendations.append("  • Highlight regulatory knowledge and compliance")
            elif detected_industry == 'marketing':
                recommendations.append("  • Showcase digital marketing expertise")
                recommendations.append("  • Include analytics and measurement skills")
                recommendations.append("  • Highlight campaign management experience")
        
        # Experience recommendations
        years_experience = extracted_data.get('years_experience', 0)
        if years_experience < 3:
            recommendations.append(f"\n📝 Experience Enhancement:")
            recommendations.append("  • Add more detailed job descriptions")
            recommendations.append("  • Include quantifiable achievements")
            recommendations.append("  • Highlight relevant projects and accomplishments")
        
        # Education recommendations
        if education_level == 'unknown':
            recommendations.append(f"\n📝 Education Section:")
            recommendations.append("  • Add educational background")
            recommendations.append("  • Include relevant coursework or projects")
            recommendations.append("  • Mention certifications and training")
        
        if not recommendations:
            recommendations.append("✅ CV is well-optimized - maintain current structure")
        
        for recommendation in recommendations:
            analysis_parts.append(f"  {recommendation}")
        
        # 4. ACTION PLAN
        analysis_parts.append("\n🚀 ACTION PLAN (Priority Order):\n")
        
        action_plan = []
        
        if ats_score < 70:
            action_plan.append("1. IMMEDIATE: Optimize ATS compatibility (Keywords & Formatting)")
        
        if len(skills) < 8:
            action_plan.append("2. HIGH PRIORITY: Expand skills section with relevant competencies")
        
        if detected_industry != 'general':
            missing_essential = industry_benchmarks.get('essential_skills_missing', [])
            if missing_essential:
                action_plan.append(f"3. MEDIUM PRIORITY: Develop {detected_industry} industry-specific skills")
        
        if not contact_info.get('email') or not contact_info.get('phone'):
            action_plan.append("4. MEDIUM PRIORITY: Complete contact information")
        
        if education_level == 'unknown':
            action_plan.append("5. LOW PRIORITY: Add education section")
        
        if not action_plan:
            action_plan.append("✅ Maintain current CV quality and focus on job applications")
        
        for action in action_plan:
            analysis_parts.append(f"  {action}")
        
        return "\n".join(analysis_parts)
    
    def analyze_cv(self, file_path, file_size):
        """Complete CV analysis pipeline with industry-specific insights"""
        try:
            # Extract text from file
            extracted_text = self.extract_text(file_path)
            
            # Process text with NLP
            nlp_results = self.nlp.process_cv_text(extracted_text)
            
            # Additional analysis
            experience_level = self.analyze_experience_level(extracted_text)
            education_level = self.analyze_education_level(extracted_text)
            years_experience = self.estimate_years_experience(extracted_text)
            
            # Industry detection and benchmarks
            detected_industry = self.detect_industry(extracted_text, nlp_results['extracted_skills'])
            industry_benchmarks = self.analyze_industry_benchmarks(
                extracted_text, nlp_results['extracted_skills'], detected_industry
            )
            
            # Compile results
            analysis_results = {
                'extracted_text': extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text,  # First 1000 chars
                'extracted_skills': nlp_results['extracted_skills'],
                'keywords': nlp_results['keywords'],
                'contact_info': nlp_results['contact_info'],
                'experience_level': experience_level,
                'years_experience': years_experience,
                'education_level': education_level,
                'ats_score': nlp_results['ats_score'],
                'completeness_score': nlp_results['completeness_score'],
                'text_analysis': nlp_results['text_analysis'],
                
                # New industry-specific features
                'detected_industry': detected_industry,
                'industry_benchmarks': industry_benchmarks,
                
                # File metadata
                'file_size': file_size,
                'analysis_date': datetime.now().isoformat()
            }
            
            # Generate summary with industry context
            analysis_results['summary'] = self.generate_enhanced_summary(analysis_results)
            
            return analysis_results
            
        except Exception as e:
            raise Exception(f"Error analyzing CV: {str(e)}")
    
    def analyze_cv_critical(self, file_path, file_size):
        """Enhanced CV analysis with critical analysis and intelligent feedback"""
        try:
            # Perform standard analysis first
            standard_results = self.analyze_cv(file_path, file_size)
            
            # Perform critical analysis
            critical_analysis = self.critical_analyzer.generate_comprehensive_critical_analysis(standard_results)
            
            # Generate intelligent feedback
            intelligent_feedback = self.feedback_generator.generate_comprehensive_feedback(
                standard_results, critical_analysis
            )
            
            # Add critical analysis results to standard results
            enhanced_results = standard_results.copy()
            enhanced_results.update({
                'critical_analysis': critical_analysis,
                'intelligent_feedback': intelligent_feedback,
                'enhanced_summary': self._generate_enhanced_summary_with_critical_insights(
                    standard_results, critical_analysis, intelligent_feedback
                ),
                'analysis_version': '2.0-enhanced',
                'critical_analysis_included': True
            })
            
            return enhanced_results
            
        except Exception as e:
            raise Exception(f"Error in critical CV analysis: {str(e)}")
    
    def _generate_enhanced_summary_with_critical_insights(self, standard_results, critical_analysis, feedback):
        """Generate enhanced summary incorporating critical insights"""
        summary_parts = []
        
        # Basic profile summary
        skills = standard_results.get('extracted_skills', [])
        if skills:
            top_skills = skills[:3]
            summary_parts.append(f"Profil profesional dengan keahlian kuat di {', '.join(top_skills)}")
        
        # Experience and industry context
        experience_level = standard_results.get('experience_level', 'unknown')
        detected_industry = standard_results.get('detected_industry', 'general')
        
        if experience_level != 'unknown':
            level_descriptions = {
                'junior': 'profesional junior dengan fondasi技能 yang solid',
                'mid': 'profesional berpengalaman dengan expertise yang teruji',
                'senior': 'profesional senior dengan leadership dan strategic capability'
            }
            summary_parts.append(level_descriptions.get(experience_level, 'profesional berpengalaman'))
        
        # Critical insights integration
        content_score = critical_analysis.get('overall_score', 0)
        if content_score >= 80:
            summary_parts.append("CV menunjukkan kualitas konten yang sangat baik dengan detail yang komprehensif")
        elif content_score >= 60:
            summary_parts.append("CV memiliki kualitas yang baik dengan beberapa area untuk perbaikan")
        else:
            summary_parts.append("CV memerlukan perbaikan fundamental untuk meningkatkan daya tarik")
        
        # Industry positioning
        if detected_industry != 'general':
            summary_parts.append(f"Memiliki positioning yang baik di industri {detected_industry}")
        
        # ATS and market readiness
        ats_score = standard_results.get('ats_score', 0)
        if ats_score >= 80:
            summary_parts.append("CV dioptimalkan dengan baik untuk sistem ATS dan memiliki daya saing tinggi")
        elif ats_score >= 60:
            summary_parts.append("CV memiliki compatibility yang baik dengan ATS namun masih bisa ditingkatkan")
        else:
            summary_parts.append("CV perlu optimasi ATS untuk meningkatkan visibility di pasar kerja")
        
        # Add strategic insights
        priority_feedback = feedback.get('priority_based_feedback', {})
        if priority_feedback.get('critical'):
            summary_parts.append("Memerlukan perbaikan segera pada beberapa aspek kritis")
        
        return ". ".join(summary_parts) + "."
    
    def get_detailed_critical_feedback(self, file_path, file_size):
        """Get detailed critical feedback and improvement recommendations"""
        try:
            # Perform critical analysis
            critical_results = self.analyze_cv_critical(file_path, file_size)
            
            # Extract specific feedback components
            critical_analysis = critical_results.get('critical_analysis', {})
            intelligent_feedback = critical_results.get('intelligent_feedback', {})
            
            feedback_report = {
                'overall_assessment': self._generate_overall_assessment(critical_analysis),
                'critical_gaps': critical_analysis.get('critical_gaps', {}),
                'priority_improvements': intelligent_feedback.get('priority_based_feedback', {}),
                'improvement_timeline': intelligent_feedback.get('improvement_timeline', {}),
                'competitive_position': intelligent_feedback.get('competitive_analysis', {}),
                'actionable_recommendations': self._extract_actionable_recommendations(intelligent_feedback),
                'indonesian_context': intelligent_feedback.get('indonesian_specific_advice', {}),
                'confidence_level': self._calculate_overall_confidence(critical_analysis),
                'next_steps': self._generate_next_steps(critical_analysis, intelligent_feedback)
            }
            
            return feedback_report
            
        except Exception as e:
            raise Exception(f"Error generating detailed critical feedback: {str(e)}")
    
    def _generate_overall_assessment(self, critical_analysis):
        """Generate overall assessment summary"""
        content_score = critical_analysis.get('overall_score', 0)
        credibility_score = critical_analysis.get('credibility_analysis', {}).get('score', 0)
        
        if content_score >= 80 and credibility_score >= 80:
            return {
                'rating': 'Excellent',
                'summary': 'CV berkualitas tinggi dengan konten yang kuat dan kredibilitas yang baik',
                'market_readiness': 'Siap untuk posisi strategis dan competitive job market',
                'improvement_potential': 'Minor optimizations untuk maximum impact'
            }
        elif content_score >= 60 and credibility_score >= 60:
            return {
                'rating': 'Good',
                'summary': 'CV solid dengan beberapa area yang perlu diperbaiki',
                'market_readiness': 'Cocok untuk mid-level positions dengan targeted improvements',
                'improvement_potential': 'Moderate improvements akan significantly boost competitiveness'
            }
        elif content_score >= 40:
            return {
                'rating': 'Needs Improvement',
                'summary': 'CV memerlukan perbaikan fundamental',
                'market_readiness': 'Focus pada basic improvements sebelum competitive applications',
                'improvement_potential': 'Significant improvements needed untuk market viability'
            }
        else:
            return {
                'rating': 'Critical',
                'summary': 'CV memerlukan overhaul total',
                'market_readiness': 'Tidak competitive dalam job market saat ini',
                'improvement_potential': 'Comprehensive rebuild diperlukan untuk basic functionality'
            }
    
    def _extract_actionable_recommendations(self, intelligent_feedback):
        """Extract specific actionable recommendations"""
        recommendations = []
        
        priority_feedback = intelligent_feedback.get('priority_based_feedback', {})
        
        # Extract critical recommendations
        for critical_item in priority_feedback.get('critical', []):
            recommendations.append({
                'priority': 'Critical',
                'recommendation': critical_item,
                'timeline': 'Immediate (1-3 days)',
                'impact': 'High'
            })
        
        # Extract high priority recommendations
        for high_item in priority_feedback.get('high', []):
            recommendations.append({
                'priority': 'High',
                'recommendation': high_item,
                'timeline': '1-2 weeks',
                'impact': 'High'
            })
        
        # Extract medium priority recommendations
        for medium_item in priority_feedback.get('medium', []):
            recommendations.append({
                'priority': 'Medium',
                'recommendation': medium_item,
                'timeline': '2-4 weeks',
                'impact': 'Medium'
            })
        
        return recommendations
    
    def _calculate_overall_confidence(self, critical_analysis):
        """Calculate overall confidence level in the analysis"""
        confidence_factors = []
        
        # Content quality confidence
        content_score = critical_analysis.get('overall_score', 0)
        confidence_factors.append(content_score / 100)
        
        # Credibility confidence
        credibility = critical_analysis.get('credibility_analysis', {})
        credibility_score = credibility.get('score', 0)
        confidence_factors.append(credibility_score / 100)
        
        # Gap analysis completeness
        gaps = critical_analysis.get('critical_gaps', {})
        gap_completeness = 1.0 if gaps else 0.5
        confidence_factors.append(gap_completeness)
        
        overall_confidence = sum(confidence_factors) / len(confidence_factors)
        
        if overall_confidence >= 0.8:
            return 'High'
        elif overall_confidence >= 0.6:
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_next_steps(self, critical_analysis, intelligent_feedback):
        """Generate specific next steps for CV improvement"""
        next_steps = []
        
        gaps = critical_analysis.get('critical_gaps', {})
        
        # Critical gaps -> Immediate actions
        if gaps.get('critical'):
            next_steps.append({
                'phase': 'Immediate (Week 1)',
                'actions': [
                    'Fix critical ATS compatibility issues',
                    'Complete missing contact information',
                    'Expand skills section to minimum viable level'
                ]
            })
        
        # Important gaps -> Short term improvements
        if gaps.get('important'):
            next_steps.append({
                'phase': 'Short Term (Week 2-4)',
                'actions': [
                    'Enhance achievement descriptions with quantified results',
                    'Optimize for target industry requirements',
                    'Improve content quality and professionalism'
                ]
            })
        
        # Strategic improvements
        next_steps.append({
            'phase': 'Medium Term (Month 2-3)',
            'actions': [
                'Develop professional industry-specific competencies',
                'Build portfolio and online presence',
                'Network and seek mentorship opportunities'
            ]
        })
        
        # Long term development
        next_steps.append({
            'phase': 'Long Term (Ongoing)',
            'actions': [
                'Continuous learning and skill development',
                'Regular CV updates and market positioning',
                'Strategic career planning and goal setting'
            ]
        })
        
        return next_steps
    
    def get_recommendations(self, analysis_results):
        """Generate recommendations based on CV analysis"""
        recommendations = []
        
        ats_score = analysis_results.get('ats_score', 0)
        completeness_score = analysis_results.get('completeness_score', 0)
        extracted_skills = analysis_results.get('extracted_skills', [])
        
        # ATS score recommendations
        if ats_score < 50:
            recommendations.append({
                'type': 'ats_improvement',
                'priority': 'high',
                'title': 'Improve ATS Compatibility',
                'description': 'Your CV needs optimization for better ATS parsing. Consider adding more standard sections, improving formatting, and including relevant keywords.'
            })
        elif ats_score < 70:
            recommendations.append({
                'type': 'ats_improvement',
                'priority': 'medium',
                'title': 'Enhance ATS Optimization',
                'description': 'Your CV has decent ATS compatibility. Consider adding more specific technical keywords and ensuring consistent formatting.'
            })
        
        # Skills recommendations
        if len(extracted_skills) < 3:
            recommendations.append({
                'type': 'skills_enhancement',
                'priority': 'high',
                'title': 'Add More Technical Skills',
                'description': 'Consider adding more technical skills to your CV. Include programming languages, tools, and frameworks relevant to your field.'
            })
        elif len(extracted_skills) < 8:
            recommendations.append({
                'type': 'skills_enhancement',
                'priority': 'medium',
                'title': 'Expand Skill Section',
                'description': 'Your skills section could be more comprehensive. Consider adding industry-specific tools and emerging technologies.'
            })
        
        # Completeness recommendations
        if completeness_score < 60:
            recommendations.append({
                'type': 'completeness',
                'priority': 'high',
                'title': 'Improve CV Completeness',
                'description': 'Your CV could be more comprehensive. Consider adding work experience details, education background, and a professional summary.'
            })
        
        # Experience level specific recommendations
        experience_level = analysis_results.get('experience_level', 'unknown')
        if experience_level == 'junior':
            recommendations.append({
                'type': 'career_development',
                'priority': 'medium',
                'title': 'Highlight Learning and Growth',
                'description': 'As a junior professional, emphasize your learning curve, relevant projects, and willingness to grow. Consider adding internships or academic projects.'
            })
        elif experience_level == 'senior':
            recommendations.append({
                'type': 'leadership',
                'priority': 'medium',
                'title': 'Emphasize Leadership Experience',
                'description': 'Highlight your leadership experience, mentoring roles, and impact on team/projects. Consider adding quantifiable achievements.'
            })
        
        return recommendations
    
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
