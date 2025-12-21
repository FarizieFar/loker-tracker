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

class CVAnalyzer:
    """CV/Resume analyzer with PDF and DOCX support"""
    
    def __init__(self):
        self.nlp = NLPProcessor()
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
    
    def analyze_cv(self, file_path, file_size):
        """Complete CV analysis pipeline"""
        try:
            # Extract text from file
            extracted_text = self.extract_text(file_path)
            
            # Process text with NLP
            nlp_results = self.nlp.process_cv_text(extracted_text)
            
            # Additional analysis
            experience_level = self.analyze_experience_level(extracted_text)
            education_level = self.analyze_education_level(extracted_text)
            years_experience = self.estimate_years_experience(extracted_text)
            
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
                'file_size': file_size,
                'analysis_date': datetime.now().isoformat()
            }
            
            # Generate summary
            analysis_results['summary'] = self.generate_summary(analysis_results)
            
            return analysis_results
            
        except Exception as e:
            raise Exception(f"Error analyzing CV: {str(e)}")
    
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
