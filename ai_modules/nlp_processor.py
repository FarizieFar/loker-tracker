"""
NLP Processor Module
Handles text processing, skill extraction, and language analysis
"""

import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
import yake
import string

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class NLPProcessor:
    """Natural Language Processing utilities for CV and job analysis"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.max_keywords = 20
        
        # Common skill keywords for extraction
        self.skill_keywords = {
            'programming': [
                'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
                'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css',
                'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'data analysis', 'statistics',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
                'tableau', 'power bi', 'excel', 'sql', 'data visualization'
            ],
            'tools': [
                'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins',
                'github', 'gitlab', 'jira', 'confluence', 'slack', 'trello'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving',
                'analytical thinking', 'creativity', 'adaptability', 'time management',
                'project management', 'customer service'
            ]
        }
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep spaces and basic punctuation
        text = re.sub(r'[^\w\s\-\.]', ' ', text)
        
        return text.strip()
    
    def extract_skills(self, text):
        """Extract skills from text using keyword matching"""
        if not text:
            return []
        
        text = self.clean_text(text)
        skills_found = []
        
        for category, keywords in self.skill_keywords.items():
            category_skills = []
            for keyword in keywords:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                if re.search(pattern, text):
                    category_skills.append(keyword)
            
            if category_skills:
                skills_found.extend(category_skills)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in skills_found:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                unique_skills.append(skill)
        
        return unique_skills
    
    def extract_keywords(self, text, max_keywords=20):
        """Extract important keywords using YAKE algorithm"""
        if not text:
            return []
        
        text = self.clean_text(text)
        
        try:
            # Initialize YAKE extractor
            kw_extractor = yake.KeywordExtractor(
                lan="en",
                n=2,  # Extract 1-2 word phrases
                dedupLim=0.7,  # Remove 70% similar keywords
                top=max_keywords
            )
            
            keywords = kw_extractor.extract_keywords(text)
            return [kw[0] for kw in keywords]
        except:
            # Fallback: simple word frequency
            words = word_tokenize(text)
            words = [word for word in words if word.isalpha() and word not in self.stop_words]
            word_freq = Counter(words)
            return [word for word, freq in word_freq.most_common(max_keywords)]
    
    def calculate_readability_score(self, text):
        """Calculate text readability (simplified Flesch Reading Ease)"""
        if not text:
            return 0
        
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        
        if len(sentences) == 0 or len(words) == 0:
            return 0
        
        # Simple syllables estimation
        syllables = sum(self._count_syllables(word) for word in words)
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)
        
        # Flesch Reading Ease score
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        return max(0, min(100, score))  # Clamp between 0-100
    
    def _count_syllables(self, word):
        """Simple syllable counter for English words"""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def analyze_text_structure(self, text):
        """Analyze text structure for CV completeness"""
        if not text:
            return {}
        
        text = self.clean_text(text)
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        
        analysis = {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_words_per_sentence': len(words) / len(sentences) if sentences else 0,
            'readability_score': self.calculate_readability_score(text),
            'has_sections': self._detect_sections(text)
        }
        
        return analysis
    
    def _detect_sections(self, text):
        """Detect common CV sections"""
        sections = {
            'experience': ['experience', 'work history', 'employment', 'career'],
            'education': ['education', 'academic', 'university', 'degree', 'bachelor', 'master'],
            'skills': ['skills', 'technical skills', 'programming', 'software'],
            'summary': ['summary', 'objective', 'profile', 'about'],
            'contact': ['contact', 'email', 'phone', 'address']
        }
        
        found_sections = []
        for section, keywords in sections.items():
            for keyword in keywords:
                if keyword in text.lower():
                    found_sections.append(section)
                    break
        
        return found_sections
    
    def calculate_ats_score(self, text, extracted_skills):
        """Calculate ATS (Applicant Tracking System) compatibility score"""
        if not text:
            return 0
        
        score = 0
        max_score = 100
        
        # Word count score (20 points)
        word_count = len(word_tokenize(text))
        if 200 <= word_count <= 800:
            score += 20
        elif word_count >= 100:
            score += 10
        
        # Section detection score (30 points)
        sections = self._detect_sections(text)
        section_score = len(sections) * 6  # 6 points per section
        score += min(section_score, 30)
        
        # Skills score (25 points)
        if len(extracted_skills) >= 5:
            score += 25
        elif len(extracted_skills) >= 3:
            score += 15
        elif len(extracted_skills) > 0:
            score += 10
        
        # Readability score (15 points)
        readability = self.calculate_readability_score(text)
        readability_score = min(readability / 6, 15)  # 15 points for 90+ readability
        score += readability_score
        
        # Contact info score (10 points)
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        has_phone = bool(re.search(r'\b\d{3}-\d{3}-\d{4}\b', text))
        if has_email and has_phone:
            score += 10
        elif has_email or has_phone:
            score += 5
        
        return min(score, max_score)
    
    def extract_contact_info(self, text):
        """Extract contact information from text"""
        if not text:
            return {}
        
        contact_info = {}
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Extract phone (various formats)
        phone_patterns = [
            r'\b\d{3}-\d{3}-\d{4}\b',
            r'\(\d{3}\)\s*\d{3}-\d{4}',
            r'\b\d{10,11}\b',
            r'\+\d{1,3}[-\s]?\d{8,10}'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact_info['phone'] = phone_match.group()
                break
        
        # Extract name (first line or before contact info)
        lines = text.split('\n')[:3]  # Check first 3 lines
        for line in lines:
            line = line.strip()
            if len(line) > 2 and len(line) < 50 and not re.search(r'@|tel|phone|email', line.lower()):
                # Check if it looks like a name (2-3 words, no numbers)
                words = line.split()
                if 2 <= len(words) <= 3 and not any(char.isdigit() for char in line):
                    contact_info['name'] = line.title()
                    break
        
        return contact_info
    
    def process_cv_text(self, text):
        """Complete CV text processing pipeline"""
        if not text:
            return {
                'extracted_skills': [],
                'keywords': [],
                'contact_info': {},
                'text_analysis': {},
                'ats_score': 0,
                'completeness_score': 0
            }
        
        # Extract skills
        extracted_skills = self.extract_skills(text)
        
        # Extract keywords
        keywords = self.extract_keywords(text, max_keywords=15)
        
        # Extract contact info
        contact_info = self.extract_contact_info(text)
        
        # Analyze text structure
        text_analysis = self.analyze_text_structure(text)
        
        # Calculate ATS score
        ats_score = self.calculate_ats_score(text, extracted_skills)
        
        # Calculate completeness score
        completeness_score = self._calculate_completeness_score(
            extracted_skills, contact_info, text_analysis
        )
        
        return {
            'extracted_skills': extracted_skills,
            'keywords': keywords,
            'contact_info': contact_info,
            'text_analysis': text_analysis,
            'ats_score': round(ats_score, 1),
            'completeness_score': round(completeness_score, 1)
        }
    
    def _calculate_completeness_score(self, extracted_skills, contact_info, text_analysis):
        """Calculate overall CV completeness score"""
        score = 0
        
        # Skills completeness (30 points)
        if len(extracted_skills) >= 10:
            score += 30
        elif len(extracted_skills) >= 5:
            score += 20
        elif len(extracted_skills) >= 3:
            score += 15
        elif len(extracted_skills) > 0:
            score += 10
        
        # Contact information completeness (25 points)
        if 'email' in contact_info and 'phone' in contact_info:
            score += 25
        elif 'email' in contact_info or 'phone' in contact_info:
            score += 15
        elif 'name' in contact_info:
            score += 10
        
        # Section completeness (25 points)
        section_count = len(text_analysis.get('has_sections', []))
        score += min(section_count * 5, 25)  # 5 points per section, max 25
        
        # Word count completeness (20 points)
        word_count = text_analysis.get('word_count', 0)
        if 200 <= word_count <= 800:
            score += 20
        elif word_count >= 100:
            score += 10
        
        return min(score, 100)
