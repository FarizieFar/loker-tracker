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
        # Support for multiple languages
        try:
            self.stop_words_en = set(stopwords.words('english'))
        except:
            self.stop_words_en = set()
        
        try:
            # Download Indonesian stopwords if available
            nltk.download('stopwords')
            self.stop_words_id = set(stopwords.words('indonesian'))
        except:
            # Indonesian stopwords as fallback
            self.stop_words_id = {
                'yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'dengan', 'adalah', 'akan', 'pada',
                'oleh', 'atau', 'dalam', 'oleh', 'kami', 'kita', 'mereka', 'dia', 'ia', 'nya',
                'ini', 'itu', 'dapat', 'bisa', 'harus', 'sebagai', 'juga', 'sudah', 'telah',
                'dapat', 'bisa', 'harus', 'tidak', 'ya', 'atau', 'dengan', 'untuk'
            }
        
        self.stemmer = PorterStemmer()
        self.max_keywords = 20
        
        # Comprehensive skill keywords database for extraction (English & Indonesian)
        self.skill_keywords = {
            # Programming & Development
            'programming': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
                'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'xml', 'json',
                'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel',
                'react native', 'flutter', 'xamarin', 'ionic', 'electron', 'next.js', 'nuxt.js', 'svelte',
                'graphql', 'rest api', 'microservices', 'devops', 'ci/cd', 'test-driven development', 'tdd',
                'agile', 'scrum', 'kanban', 'clean code', 'refactoring', 'design patterns', 'solid principles'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'neural networks', 'artificial intelligence', 'ai',
                'data analysis', 'statistics', 'statistical analysis', 'predictive modeling', 'data mining',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'xgboost', 'lightgbm',
                'tableau', 'power bi', 'excel', 'sql', 'data visualization', 'matplotlib', 'seaborn', 'plotly',
                'jupyter', 'spyder', 'r studio', 'spss', 'sas', 'stata', 'hadoop', 'spark', 'hive',
                'big data', 'data warehouse', 'etl', 'data pipeline', 'real-time analytics', 'business intelligence'
            ],
            'cybersecurity': [
                'cybersecurity', 'information security', 'network security', 'penetration testing', 'ethical hacking',
                'vulnerability assessment', 'security auditing', 'incident response', 'risk assessment',
                'compliance', 'gdpr', 'iso 27001', 'nist', 'firewall', 'vpn', 'encryption', 'cryptography',
                'siem', 'ids', 'ips', 'malware analysis', 'forensics', 'security architecture', 'zero trust',
                'soc', 'threat intelligence', 'vulnerability management', 'security awareness', 'data protection'
            ],
            'cloud_computing': [
                'aws', 'amazon web services', 'azure', 'microsoft azure', 'google cloud', 'gcp', 'oracle cloud',
                'docker', 'kubernetes', 'openshift', 'helm', 'terraform', 'ansible', 'cloudformation',
                'serverless', 'lambda', 'functions as a service', 'faas', 'microservices', 'api gateway',
                'load balancer', 'auto scaling', 'cloud storage', 'cdn', 'content delivery network',
                'cloud security', 'identity management', 'multi-cloud', 'hybrid cloud', 'cloud migration'
            ],
            
            # Business & Management
            'project_management': [
                'project management', 'agile', 'scrum', 'kanban', 'prince2', 'pmp', 'capm', 'lean',
                'six sigma', 'waterfall', 'critical path', 'gantt chart', 'risk management', 'stakeholder management',
                'resource planning', 'budget management', 'timeline management', 'quality assurance',
                'vendor management', 'team leadership', 'change management', 'communication management'
            ],
            'business_analysis': [
                'business analysis', 'requirements gathering', 'process improvement', 'bpmn', 'uml',
                'data modeling', 'system analysis', 'functional specifications', 'user stories', 'use cases',
                'stakeholder analysis', 'gap analysis', 'root cause analysis', 'fishbone diagram',
                'pareto analysis', 'swot analysis', 'cost-benefit analysis', 'roi analysis', 'feasibility study'
            ],
            'marketing': [
                'digital marketing', 'content marketing', 'social media marketing', 'email marketing',
                'seo', 'search engine optimization', 'sem', 'google ads', 'facebook ads', 'instagram marketing',
                'linkedin marketing', 'youtube marketing', 'influencer marketing', 'affiliate marketing',
                'marketing automation', 'lead generation', 'conversion optimization', 'ab testing',
                'brand management', 'market research', 'competitive analysis', 'customer acquisition',
                'customer retention', 'marketing analytics', 'google analytics', 'facebook pixel', 'crm'
            ],
            'sales': [
                'sales', 'inside sales', 'outside sales', 'enterprise sales', 'b2b sales', 'b2c sales',
                'cold calling', 'lead qualification', 'sales funnel', 'crm', 'salesforce', 'hubspot',
                'negotiation', 'closing techniques', 'account management', 'relationship building',
                'prospecting', 'sales process', 'quota achievement', 'pipeline management', 'territory management',
                'key account management', 'channel sales', 'partner management', 'sales training', 'sales coaching'
            ],
            
            # Finance & Accounting
            'finance': [
                'financial analysis', 'financial modeling', 'financial planning', 'investment analysis',
                'risk management', 'portfolio management', 'corporate finance', 'financial reporting',
                'budgeting', 'forecasting', 'variance analysis', 'cost accounting', 'management accounting',
                'financial statement analysis', 'excel advanced', 'bloomberg', 'reuters', 'factset',
                'derivatives', 'equity research', 'credit analysis', 'treasury management', 'cash flow',
                'dcf', 'wacc', 'npv', 'irr', 'monte carlo', 'scenario analysis', 'stress testing'
            ],
            'accounting': [
                'accounting', 'bookkeeping', 'financial accounting', 'management accounting', 'cost accounting',
                'tax accounting', 'audit', 'internal audit', 'external audit', 'forensic accounting',
                'quickbooks', 'xero', 'sage', 'peachtree', 'gaap', 'ifrs', 'financial statements',
                'accounts payable', 'accounts receivable', 'general ledger', 'journal entries', 'reconciliations',
                'monthly close', 'financial reporting', 'tax preparation', 'tax planning', 'compliance'
            ],
            
            # Healthcare & Medical
            'healthcare': [
                'clinical research', 'medical research', 'pharmaceutical', 'biotech', 'medical devices',
                'healthcare administration', 'hospital management', 'patient care', 'medical coding',
                'icd-10', 'cpt coding', 'hipaa compliance', 'electronic health records', 'ehr', 'emr',
                'medical billing', 'insurance', 'claims processing', 'quality improvement', 'patient safety',
                'clinical trials', 'regulatory affairs', 'fda', 'gmp', 'gcp', 'clinical data management'
            ],
            'nursing': [
                'nursing', 'registered nurse', 'licensed practical nurse', 'nurse practitioner', 'clinical nurse',
                'critical care', 'emergency nursing', 'pediatric nursing', 'maternal nursing', 'oncology nursing',
                'psychiatric nursing', 'community health', 'home health', 'nursing informatics', 'case management',
                'patient education', 'health assessment', 'medication administration', 'wound care', 'infection control'
            ],
            
            # Education & Training
            'education': [
                'teaching', 'instructional design', 'curriculum development', 'lesson planning', 'assessment',
                'student assessment', 'educational technology', 'e-learning', 'online learning', 'blended learning',
                'learning management system', 'lms', 'moodle', 'blackboard', 'canvas', 'educational research',
                'pedagogy', 'andragogy', 'special education', 'inclusive education', 'differentiated instruction',
                'classroom management', 'student engagement', 'educational leadership', 'academic advising'
            ],
            
            # Legal & Compliance
            'legal': [
                'legal research', 'contract law', 'corporate law', 'litigation', 'employment law', 'intellectual property',
                'patent law', 'trademark law', 'copyright law', 'compliance', 'regulatory compliance', 'due diligence',
                'legal writing', 'brief writing', 'legal analysis', 'case management', 'document review',
                'legal technology', 'contract management', 'negotiation', 'mediation', 'arbitration'
            ],
            'compliance': [
                'compliance', 'regulatory compliance', 'policy development', 'risk assessment', 'audit',
                'internal controls', 'sox compliance', 'gdpr', 'ccpa', 'hipaa', 'pci dss', 'iso standards',
                'training programs', 'monitoring', 'reporting', 'investigations', 'remediation', 'governance'
            ],
            
            # Creative & Design
            'design': [
                'graphic design', 'ui design', 'ux design', 'product design', 'visual design', 'web design',
                'mobile design', 'interaction design', 'user research', 'wireframing', 'prototyping', 'figma',
                'adobe photoshop', 'adobe illustrator', 'adobe indesign', 'sketch', 'invision', 'principle',
                'design thinking', 'design systems', 'branding', 'typography', 'color theory', 'layout design'
            ],
            'content_creation': [
                'content creation', 'copywriting', 'technical writing', 'content strategy', 'blog writing',
                'social media content', 'video production', 'photography', 'videography', 'editing',
                'premiere pro', 'final cut pro', 'after effects', 'lightroom', 'canon', 'sony',
                'content management', 'wordpress', 'cms', 'storytelling', 'brand voice', 'seo writing'
            ],
            
            # Human Resources
            'hr': [
                'human resources', 'recruitment', 'talent acquisition', 'hiring', 'onboarding', 'offboarding',
                'performance management', 'employee relations', 'compensation', 'benefits administration',
                'payroll', 'hris', 'successfactors', 'workday', 'bamboo hr', 'workforce planning',
                'employee engagement', 'organizational development', 'change management', 'training',
                'learning and development', 'succession planning', 'diversity and inclusion', 'employee retention'
            ],
            'talent_management': [
                'talent management', 'talent acquisition', 'talent development', 'succession planning',
                'leadership development', 'mentoring', 'coaching', 'performance coaching', 'career planning',
                'talent analytics', 'workforce analytics', 'employee engagement', 'retention strategies'
            ],
            
            # Operations & Logistics
            'operations': [
                'operations management', 'supply chain management', 'logistics', 'inventory management',
                'procurement', 'vendor management', 'lean manufacturing', 'six sigma', 'process improvement',
                'quality management', 'iso 9001', 'erp', 'sap', 'oracle', 'microsoft dynamics',
                'warehouse management', 'distribution', 'transportation', 'demand planning', 'supply planning'
            ],
            'supply_chain': [
                'supply chain', 'supply chain management', 'procurement', 'purchasing', 'vendor management',
                'supplier relations', 'contract negotiation', 'cost reduction', 'supply chain analytics',
                'demand forecasting', 'inventory optimization', 'logistics', 'freight management', 'customs'
            ],
            
            # Product Management
            'product_management': [
                'product management', 'product development', 'product strategy', 'roadmap planning',
                'user stories', 'backlog management', 'agile product development', 'market research',
                'competitive analysis', 'feature prioritization', 'product lifecycle', 'launch management',
                'product analytics', 'a/b testing', 'user research', 'customer feedback', 'product-market fit'
            ],
            
            # General Soft Skills
            'leadership': [
                'leadership', 'team leadership', 'strategic thinking', 'vision', 'decision making',
                'influence', 'mentoring', 'coaching', 'delegation', 'conflict resolution', 'change leadership'
            ],
            'communication': [
                'communication', 'presentation', 'public speaking', 'written communication', 'verbal communication',
                'interpersonal skills', 'cross-cultural communication', 'negotiation', 'active listening',
                'empathy', 'relationship building', 'client relations', 'customer service'
            ],
            'problem_solving': [
                'problem solving', 'critical thinking', 'analytical thinking', 'root cause analysis',
                'creative thinking', 'innovation', 'design thinking', 'data-driven decision making',
                'troubleshooting', 'debugging', 'continuous improvement', 'lean thinking'
            ],
            
            # Indonesian Programming & Development
            'programming_id': [
                'pemrograman', 'pengembangan aplikasi', 'web development', 'mobile development',
                'frontend', 'backend', 'fullstack', 'database', 'mysql', 'postgresql', 'mongodb',
                'codeigniter', 'laravel', 'spring boot', 'react native', 'flutter', 'android', 'ios',
                'vue.js', 'angular', 'node.js', 'express', 'django', 'golang', 'kotlin', 'swift',
                'bootstrap', 'tailwind', 'css', 'html', 'javascript', 'typescript', 'jquery',
                'api', 'rest api', 'graphql', 'microservices', 'docker', 'kubernetes', 'git',
                'github', 'gitlab', 'ci/cd', 'jenkins', 'aws', 'azure', 'gcp', 'cloud computing'
            ],
            
            # Indonesian Business & Management
            'business_id': [
                'manajemen bisnis', 'bisnis plan', 'strategi bisnis', 'marketing', 'digital marketing',
                'seo', 'sem', 'google ads', 'facebook ads', 'instagram marketing', 'tiktok marketing',
                'content marketing', 'social media', 'brand awareness', 'customer acquisition',
                'sales', 'penjualan', 'customer service', 'relationship management', 'networking',
                'lead generation', 'conversion rate', 'analytics', 'google analytics', 'facebook pixel',
                'project management', 'manajemen proyek', 'agile', 'scrum', 'kanban', 'timeline',
                'budget planning', 'perencanaan anggaran', 'cost reduction', 'pengurangan biaya',
                'process improvement', 'pelayanan pelanggan', 'operational efficiency'
            ],
            
            # Indonesian Finance & Accounting
            'finance_id': [
                'keuangan', 'akuntansi', 'manajemen keuangan', 'analisis keuangan', 'laporan keuangan',
                'budgeting', 'anggaran', 'forecasting', 'proyeksi', 'investment', 'investasi',
                'risk management', 'manajemen risiko', 'audit', 'perpajakan', 'tax planning',
                'cash flow', 'arus kas', 'financial planning', 'perencanaan keuangan', 'npv', 'irr',
                'roi analysis', 'cost benefit analysis', 'quickbooks', 'xero', 'sage', 'sap',
                'excel', 'spreadsheet', 'pivot table', 'vlookup', 'hlookup', 'financial modeling'
            ],
            
            # Indonesian Healthcare & Medical
            'healthcare_id': [
                'kesehatan', 'medis', 'klinik', 'rumah sakit', 'pasien', 'perawatan', 'terapi',
                'diagnosis', 'rekam medis', 'ehr', 'emr', 'hipaa', 'kode icd-10', 'cpt coding',
                'medical billing', 'billing medis', 'asuransi kesehatan', 'quality improvement',
                'patient safety', 'keamanan pasien', 'clinical research', 'riset klinis',
                'farmasi', 'farmakologi', 'bioteknologi', 'medical device', 'alat kesehatan',
                'nursing', 'keperawatan', 'bidan', 'dokter', 'spesialis', 'konsultan'
            ],
            
            # Indonesian Education & Training
            'education_id': [
                'pendidikan', 'mengajar', 'pelatihan', 'kursus', 'workshop', 'seminar', 'kurikulum',
                'lesson plan', 'rencana pembelajaran', 'assesment', 'evaluasi', 'student evaluation',
                'educational technology', 'teknologi pendidikan', 'e-learning', 'online learning',
                'lms', 'moodle', 'canvas', 'blackboard', 'video pembelajaran', 'multimedia',
                'research', 'riset', 'publikasi', 'jurnal', 'academic writing', 'penulisan akademik',
                'supervisi', 'mentoring', 'coaching', 'student counseling', 'konseling siswa'
            ],
            
            # Indonesian Legal & Compliance
            'legal_id': [
                'hukum', 'legal', 'perundang-undangan', 'regulasi', 'compliance', 'kepatuhan',
                'kontrak', 'perjanjian', 'litigasi', 'mediasi', 'arbitrase', 'due diligence',
                'legal research', 'riset hukum', 'intellectual property', 'hak kekayaan intelektual',
                'hak paten', 'hak cipta', 'merek dagang', 'contract law', 'hukum kontrak',
                'employment law', 'hukum ketenagakerjaan', 'corporate law', 'hukum perusahaan',
                'legal writing', 'penulisan hukum', 'legal analysis', 'analisis hukum'
            ],
            
            # Indonesian HR & Management
            'hr_id': [
                'sumber daya manusia', 'sdm', 'recruitment', 'rekrutmen', 'hiring', 'perekrutan',
                'onboarding', 'employee onboarding', 'performance management', 'manajemen kinerja',
                'employee relations', 'hubungan karyawan', 'compensation', 'kompensasi', 'gaji',
                'benefits', 'manfaat', 'payroll', 'gaji dan.upah', 'hris', 'employee engagement',
                'employee retention', 'retensi karyawan', 'organizational development',
                'perubahan organisasi', 'training', 'pelatihan', 'learning development',
                'talent management', 'manajemen talenta', 'succession planning', 'suksesi'
            ],
            
            # Indonesian Creative & Design
            'design_id': [
                'desain', 'graphic design', 'desain grafis', 'ui design', 'ux design', 'web design',
                'mobile design', 'desain aplikasi', 'visual design', 'desain visual', 'branding',
                'merek dagang', 'typography', 'tipografi', 'color theory', 'teori warna',
                'layout design', 'desain tata letak', 'photoshop', 'illustrator', 'figma',
                'sketch', 'invision', 'canva', 'adobe creative', 'premiere pro', 'after effects',
                'photography', 'fotografi', 'videography', 'videografi', 'editing', 'penyuntingan'
            ],
            
            # General Soft Skills (continued)
            'collaboration': [
                'teamwork', 'collaboration', 'cross-functional teamwork', 'agile collaboration',
                'virtual teamwork', 'remote work', 'distributed teams', 'stakeholder management',
                'partnership building', 'vendor relationships', 'client collaboration'
            ],
            'time_management': [
                'time management', 'prioritization', 'task management', 'deadline management', 'productivity',
                'organization', 'planning', 'scheduling', 'multitasking', 'work efficiency', 'goal setting'
            ]
        }
    
    def detect_language(self, text):
        """Detect if text is primarily Indonesian or English"""
        if not text:
            return 'unknown'
        
        text_lower = text.lower()
        
        # Indonesian common words and patterns
        indonesian_indicators = [
            'yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'dengan', 'adalah', 'akan', 'pada',
            'oleh', 'atau', 'dalam', 'kami', 'kita', 'mereka', 'dia', 'ia', 'nya', 'ini', 'itu',
            'dapat', 'bisa', 'harus', 'sebagai', 'juga', 'sudah', 'telah', 'tidak', 'ya',
            'pendidikan', 'pengalaman', 'keahlian', 'kemampuan', 'manajemen', 'proyek',
            'pengembangan', 'pelayanan', 'pelanggan', 'perusahaan', 'organisasi'
        ]
        
        # Count Indonesian indicators
        indonesian_count = sum(1 for word in indonesian_indicators if word in text_lower)
        
        # Calculate percentage
        words = text_lower.split()
        if len(words) > 0:
            indonesian_percentage = (indonesian_count / len(words)) * 100
            
            if indonesian_percentage > 5:  # More than 5% Indonesian indicators
                return 'indonesian'
            elif indonesian_percentage > 1:  # Mixed language
                return 'mixed'
            else:
                return 'english'
        
        return 'unknown'
    
    def clean_text(self, text):
        """Enhanced text cleaning with language awareness"""
        if not text:
            return ""
        
        # Detect language first
        language = self.detect_language(text)
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep some important ones
        text = re.sub(r'[^\w\s\-\.\,\;\:\!\?\(\)\[\]\/\&\%\#\@\+]', ' ', text)
        
        # Handle common OCR errors and formatting issues
        text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with space
        text = re.sub(r'\r+', ' ', text)  # Replace carriage returns
        
        # Fix common spacing issues
        text = re.sub(r'\s*\.\s*', '. ', text)  # Fix spacing around periods
        text = re.sub(r'\s*,\s*', ', ', text)  # Fix spacing around commas
        text = re.sub(r'\s*\(\s*', '(', text)  # Fix spacing around parentheses
        text = re.sub(r'\s*\)\s*', ') ', text)  # Fix spacing around parentheses
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def fuzzy_skill_match(self, text, skill_list, threshold=0.8):
        """Fuzzy matching for skills with multiple languages support"""
        if not text or not skill_list:
            return []
        
        text_clean = self.clean_text(text)
        text_lower = text_clean.lower()
        
        found_skills = []
        
        for skill in skill_list:
            skill_lower = skill.lower()
            
            # Direct match
            if skill_lower in text_lower:
                found_skills.append(skill)
                continue
            
            # Handle compound skills (e.g., "machine learning" vs "ml")
            skill_words = skill_lower.split()
            if len(skill_words) > 1:
                # Check if all words are present in text
                if all(word in text_lower for word in skill_words):
                    found_skills.append(skill)
                    continue
            
            # Handle abbreviations
            if len(skill_lower) <= 4 and skill_lower in text_lower.replace(' ', ''):
                found_skills.append(skill)
                continue
        
        return found_skills
    
    def extract_skills(self, text):
        """Enhanced skill extraction with language awareness and fuzzy matching"""
        if not text:
            return []
        
        # Detect language
        language = self.detect_language(text)
        text_clean = self.clean_text(text)
        
        skills_found = []
        
        # Define skill priority based on language
        if language == 'indonesian':
            priority_categories = [
                'programming_id', 'business_id', 'finance_id', 'healthcare_id', 
                'education_id', 'legal_id', 'hr_id', 'design_id'
            ] + [cat for cat in self.skill_keywords.keys() if not cat.endswith('_id')]
        elif language == 'mixed':
            # Include both English and Indonesian
            priority_categories = list(self.skill_keywords.keys())
        else:
            # English only
            priority_categories = [cat for cat in self.skill_keywords.keys() if not cat.endswith('_id')]
        
        # Extract skills by priority
        for category in priority_categories:
            if category in self.skill_keywords:
                category_skills = self.fuzzy_skill_match(text_clean, self.skill_keywords[category])
                if category_skills:
                    skills_found.extend(category_skills)
        
        # Advanced pattern matching for specific CV elements
        skills_found.extend(self._extract_education_skills(text_clean))
        skills_found.extend(self._extract_experience_indicators(text_clean))
        skills_found.extend(self._extract_soft_skills(text_clean))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in skills_found:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                unique_skills.append(skill)
        
        return unique_skills
    
    def _extract_education_skills(self, text):
        """Extract education-related skills and certifications"""
        education_patterns = [
            r'\b(google\s+analytics|facebook\s+ads|aws\s+certification|pmp|cfa|cpa|scrum\s+master)\b',
            r'\b(microsoft\s+office|excel\s+advanced|power\s+bi|tableau)\b',
            r'\b(iso\s+\d+|six\s+sigma|lean|agile|scrum)\b',
            r'\b(cloud\s+computing|devops|css\s+frameworks|responsive\s+design)\b'
        ]
        
        found_skills = []
        for pattern in education_patterns:
            matches = re.findall(pattern, text.lower())
            found_skills.extend(matches)
        
        return found_skills
    
    def _extract_experience_indicators(self, text):
        """Extract experience level indicators"""
        experience_skills = []
        
        # Senior level indicators
        if re.search(r'\b(senior|lead|principal|director|manager|head)\b', text.lower()):
            experience_skills.extend(['leadership', 'team management', 'strategic planning'])
        
        # Mid level indicators
        if re.search(r'\b(mid-level|intermediate|3\s*-\s*5\s*years)\b', text.lower()):
            experience_skills.extend(['project coordination', 'problem solving'])
        
        # Technical expertise indicators
        if re.search(r'\b(expert|advanced|proficient)\b', text.lower()):
            experience_skills.extend(['technical expertise', 'domain knowledge'])
        
        return experience_skills
    
    def _extract_soft_skills(self, text):
        """Extract soft skills with enhanced detection"""
        soft_skills_found = []
        
        # Leadership indicators
        if re.search(r'\b(lead|team|manage|mentor|coach|supervise)\b', text.lower()):
            soft_skills_found.extend(['leadership', 'teamwork', 'communication'])
        
        # Problem-solving indicators
        if re.search(r'\b(solve|analyze|improve|optimize|troubleshoot)\b', text.lower()):
            soft_skills_found.extend(['problem solving', 'analytical thinking', 'continuous improvement'])
        
        # Collaboration indicators
        if re.search(r'\b(collaborate|coordinate|partner|network)\b', text.lower()):
            soft_skills_found.extend(['collaboration', 'stakeholder management', 'networking'])
        
        return list(set(soft_skills_found))  # Remove duplicates
    
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
    
    def detect_experience_level(self, text):
        """Enhanced experience level detection with multiple indicators"""
        if not text:
            return 'unknown', 0
        
        text_lower = text.lower()
        
        # Experience patterns with weights
        experience_patterns = {
            'junior': {
                'keywords': ['junior', 'entry', 'fresh', 'graduate', 'intern', 'trainee', '0-2 years', '1-2 years'],
                'weight': 1.0
            },
            'mid': {
                'keywords': ['mid-level', 'intermediate', '3-5 years', '4-6 years', 'specialist', 'analyst'],
                'weight': 1.0
            },
            'senior': {
                'keywords': ['senior', 'lead', 'principal', '5+ years', '6+ years', '7+ years', '8+ years'],
                'weight': 1.0
            },
            'executive': {
                'keywords': ['director', 'head', 'manager', 'chief', 'vp', 'executive', '10+ years'],
                'weight': 1.0
            }
        }
        
        scores = {}
        for level, config in experience_patterns.items():
            score = 0
            for keyword in config['keywords']:
                if keyword in text_lower:
                    score += config['weight']
            scores[level] = score
        
        # Calculate total experience years
        year_patterns = [
            r'(\d+)\+?\s*(years?|tahun)\s*(of\s*)?(experience|exp)',
            r'(\d+)\+?\s*years?\s*(in|of)',
            r'(\d+)\+?\s*tahun\s*(pengalaman|kerja)',
        ]
        
        total_years = 0
        for pattern in year_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                try:
                    years = int(match[0])
                    if years > total_years:
                        total_years = years
                except:
                    pass
        
        # Determine experience level based on scores and years
        max_score_level = max(scores, key=scores.get) if max(scores.values()) > 0 else 'unknown'
        
        if total_years >= 10 or max_score_level == 'executive':
            return 'executive', min(total_years, 15)
        elif total_years >= 5 or max_score_level == 'senior':
            return 'senior', total_years
        elif total_years >= 3 or max_score_level == 'mid':
            return 'mid', total_years
        elif total_years >= 1 or max_score_level == 'junior':
            return 'junior', total_years
        else:
            return 'unknown', total_years
    
    def detect_education_level(self, text):
        """Enhanced education level detection"""
        if not text:
            return 'unknown', 'unknown', 0
        
        text_lower = text.lower()
        
        # Education patterns
        education_patterns = {
            'phd': {
                'keywords': ['phd', 'doctorate', 'doctoral', 'ph.d'],
                'level': 'phd'
            },
            'master': {
                'keywords': ['master', 'mba', 'msc', 'ma', 'magister', 's2'],
                'level': 'master'
            },
            'bachelor': {
                'keywords': ['bachelor', 'bsc', 'ba', 's1', 'sarjana', 'undergraduate'],
                'level': 'bachelor'
            },
            'diploma': {
                'keywords': ['diploma', 'associate', 'certificate', 'sertifikat', 'd3', 'd4'],
                'level': 'diploma'
            },
            'high_school': {
                'keywords': ['high school', 'secondary', 'sma', 'smk', 'ged'],
                'level': 'high_school'
            }
        }
        
        detected_level = 'unknown'
        institution_score = 0
        
        # Check for education keywords
        for config in education_patterns.values():
            for keyword in config['keywords']:
                if keyword in text_lower:
                    detected_level = config['level']
                    break
            if detected_level != 'unknown':
                break
        
        # Check for prestigious institutions
        prestigious_institutions = [
            'harvard', 'mit', 'stanford', 'oxford', 'cambridge', 'ui', 'itb', 'ugm', 'ui',
            'nus', 'ntu', 'melbourne', 'sydney', 'toronto', 'waterloo', 'cmu', 'berkeley'
        ]
        
        for institution in prestigious_institutions:
            if institution in text_lower:
                institution_score += 10
        
        return detected_level, detected_level, institution_score
    
    def enhanced_industry_classification(self, text, extracted_skills):
        """Enhanced industry classification with confidence scoring"""
        if not text:
            return 'general', 0
        
        text_lower = text.lower()
        
        # Enhanced industry patterns with weights
        industry_patterns = {
            'technology': {
                'keywords': [
                    'software', 'programming', 'development', 'tech', 'digital', 'ai', 'ml', 'data science',
                    'cloud', 'cybersecurity', 'blockchain', 'mobile app', 'web development', 'devops',
                    'python', 'java', 'javascript', 'react', 'angular', 'node.js', 'aws', 'azure',
                    'machine learning', 'artificial intelligence', 'data analysis', 'big data',
                    'pemrograman', 'pengembangan aplikasi', 'teknologi', 'digital', 'cloud computing'
                ],
                'weight': 1.0
            },
            'finance': {
                'keywords': [
                    'finance', 'banking', 'investment', 'trading', 'accounting', 'audit', 'compliance',
                    'financial', 'portfolio', 'risk', 'derivatives', 'equity', 'credit', 'treasury',
                    'bloomberg', 'reuters', 'factset', 'financial modeling', 'excel advanced',
                    'keuangan', 'perbankan', 'akuntansi', 'manajemen keuangan', 'investasi'
                ],
                'weight': 1.0
            },
            'healthcare': {
                'keywords': [
                    'medical', 'health', 'clinical', 'patient', 'hospital', 'pharmaceutical', 'nursing',
                    'healthcare', 'biotech', 'clinical research', 'medical device', 'ehr', 'emr',
                    'nursing', 'doctor', 'specialist', 'healthcare administration',
                    'kesehatan', 'medis', 'klinik', 'rumah sakit', 'keperawatan', 'farmasi'
                ],
                'weight': 1.0
            },
            'education': {
                'keywords': [
                    'education', 'teaching', 'academic', 'curriculum', 'student', 'learning', 'training',
                    'educational', 'research', 'university', 'college', 'school', 'lms',
                    'pendidikan', 'mengajar', 'pelatihan', 'kurikulum', 'universitas', 'riset'
                ],
                'weight': 1.0
            },
            'marketing': {
                'keywords': [
                    'marketing', 'advertising', 'branding', 'campaign', 'digital marketing', 'seo', 'sem',
                    'social media', 'content marketing', 'lead generation', 'customer acquisition',
                    'google ads', 'facebook ads', 'marketing automation', 'brand management',
                    'marketing', 'digital marketing', 'branding', 'kampanye', 'media sosial'
                ],
                'weight': 1.0
            },
            'sales': {
                'keywords': [
                    'sales', 'revenue', 'client', 'customer', 'account', 'territory', 'quota', 'pipeline',
                    'b2b', 'b2c', 'inside sales', 'outside sales', 'enterprise sales',
                    'sales', 'penjualan', 'klien', 'pelanggan', 'target', 'pipeline penjualan'
                ],
                'weight': 1.0
            },
            'operations': {
                'keywords': [
                    'operations', 'supply chain', 'logistics', 'manufacturing', 'quality', 'process',
                    'lean', 'six sigma', 'erp', 'inventory', 'procurement', 'vendor management',
                    'operasional', 'rantai pasok', 'manufaktur', 'proses', 'kualitas'
                ],
                'weight': 1.0
            },
            'hr': {
                'keywords': [
                    'human resources', 'recruitment', 'talent', 'employee', 'benefits', 'performance',
                    'hris', 'workforce', 'organizational', 'culture', 'engagement',
                    'sumber daya manusia', 'sdm', 'rekrutmen', 'karyawan', 'kinerja'
                ],
                'weight': 1.0
            },
            'legal': {
                'keywords': [
                    'legal', 'law', 'compliance', 'regulatory', 'contract', 'litigation', 'intellectual property',
                    'hukum', 'legal', 'kepatuhan', 'regulasi', 'kontrak', 'hukum perusahaan'
                ],
                'weight': 1.0
            },
            'consulting': {
                'keywords': [
                    'consulting', 'advisory', 'strategy', 'transformation', 'optimization', 'implementation',
                    'konsultasi', 'konsultan', 'strategi', 'transformasi', 'optimasi'
                ],
                'weight': 1.0
            }
        }
        
        industry_scores = {}
        for industry, config in industry_patterns.items():
            score = 0
            for keyword in config['keywords']:
                if keyword in text_lower:
                    score += config['weight']
            
            # Boost score if industry keywords appear in skills
            skills_text = ' '.join(extracted_skills).lower()
            for keyword in config['keywords']:
                if keyword in skills_text:
                    score += 0.5  # Bonus for skills match
            
            industry_scores[industry] = score
        
        # Find best match
        if industry_scores:
            best_industry = max(industry_scores, key=industry_scores.get)
            confidence = min(industry_scores[best_industry] / 10, 1.0)  # Normalize to 0-1
            
            if industry_scores[best_industry] > 0:
                return best_industry, confidence
        
        return 'general', 0
    
    def calculate_detection_confidence(self, extracted_data):
        """Calculate overall confidence score for CV detection"""
        if not extracted_data:
            return 0
        
        confidence_factors = []
        
        # Skills detection confidence
        skills_count = len(extracted_data.get('extracted_skills', []))
        if skills_count >= 10:
            confidence_factors.append(0.9)
        elif skills_count >= 5:
            confidence_factors.append(0.7)
        elif skills_count >= 3:
            confidence_factors.append(0.5)
        else:
            confidence_factors.append(0.2)
        
        # Contact info confidence
        contact_info = extracted_data.get('contact_info', {})
        contact_score = 0
        if contact_info.get('email'):
            contact_score += 0.4
        if contact_info.get('phone'):
            contact_score += 0.4
        if contact_info.get('name'):
            contact_score += 0.2
        confidence_factors.append(contact_score)
        
        # Text analysis confidence
        text_analysis = extracted_data.get('text_analysis', {})
        sections = text_analysis.get('has_sections', [])
        if len(sections) >= 3:
            confidence_factors.append(0.9)
        elif len(sections) >= 2:
            confidence_factors.append(0.7)
        elif len(sections) >= 1:
            confidence_factors.append(0.5)
        else:
            confidence_factors.append(0.2)
        
        # ATS score confidence
        ats_score = extracted_data.get('ats_score', 0)
        ats_confidence = ats_score / 100
        confidence_factors.append(ats_confidence)
        
        # Calculate overall confidence
        overall_confidence = sum(confidence_factors) / len(confidence_factors)
        return round(overall_confidence, 2)
    
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
    
    def _detect_skills_categories(self, skills):
        """Detect which skill categories are represented in the extracted skills"""
        if not skills:
            return []
        
        detected_categories = []
        skills_lower = [skill.lower() for skill in skills]
        
        for category, keywords in self.skill_keywords.items():
            # Check if any skill matches this category
            category_matches = sum(1 for skill in skills_lower 
                                 for keyword in keywords 
                                 if keyword.lower() in skill or skill in keyword.lower())
            
            if category_matches > 0:
                detected_categories.append(category)
        
        return detected_categories
    
    def _extract_industry_keywords(self, text):
        """Extract industry-specific keywords from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        industry_keywords = []
        
        # Industry-specific keyword patterns
        industry_patterns = {
            'technology': ['software', 'development', 'programming', 'tech', 'digital', 'innovation', 'cloud', 'ai', 'data'],
            'finance': ['financial', 'banking', 'investment', 'trading', 'accounting', 'audit', 'compliance', 'risk'],
            'healthcare': ['medical', 'health', 'clinical', 'patient', 'hospital', 'pharmaceutical', 'biotech', 'nursing'],
            'education': ['teaching', 'education', 'academic', 'curriculum', 'student', 'learning', 'training'],
            'marketing': ['marketing', 'advertising', 'branding', 'campaign', 'digital marketing', 'social media', 'seo'],
            'sales': ['sales', 'revenue', 'client', 'customer', 'account', 'territory', 'quota', 'pipeline'],
            'operations': ['operations', 'supply chain', 'logistics', 'manufacturing', 'quality', 'process', 'efficiency'],
            'hr': ['human resources', 'recruitment', 'talent', 'employee', 'benefits', 'performance', 'culture'],
            'legal': ['legal', 'law', 'compliance', 'regulatory', 'contract', 'litigation', 'intellectual property'],
            'consulting': ['consulting', 'advisory', 'strategy', 'transformation', 'optimization', 'implementation']
        }
        
        for industry, keywords in industry_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    industry_keywords.append(keyword)
        
        return list(set(industry_keywords))  # Remove duplicates
    
    def calculate_ats_score(self, text, extracted_skills):
        """Calculate advanced ATS (Applicant Tracking System) compatibility score"""
        if not text:
            return 0
        
        score = 0
        max_score = 100
        
        # 1. Word Count Score (15 points)
        word_count = len(word_tokenize(text))
        if 300 <= word_count <= 600:
            score += 15
        elif 200 <= word_count <= 800:
            score += 12
        elif 150 <= word_count <= 1000:
            score += 8
        elif word_count >= 100:
            score += 5
        
        # 2. Section Detection & Structure Score (20 points)
        sections = self._detect_sections(text)
        section_score = len(sections) * 4  # 4 points per section
        score += min(section_score, 20)
        
        # Bonus for standard sections
        standard_sections = ['experience', 'education', 'skills', 'summary', 'contact']
        bonus_sections = sum(1 for section in standard_sections if section in sections)
        score += min(bonus_sections, 5)
        
        # 3. Skills Density & Relevance Score (20 points)
        skills_count = len(extracted_skills)
        if skills_count >= 15:
            score += 20
        elif skills_count >= 10:
            score += 16
        elif skills_count >= 5:
            score += 12
        elif skills_count >= 3:
            score += 8
        elif skills_count > 0:
            score += 4
        
        # Skills diversity bonus (different categories)
        skills_categories = self._detect_skills_categories(extracted_skills)
        if len(skills_categories) >= 5:
            score += 5
        elif len(skills_categories) >= 3:
            score += 3
        elif len(skills_categories) >= 2:
            score += 1
        
        # 4. Contact Information Score (10 points)
        contact_info = self.extract_contact_info(text)
        contact_score = 0
        if 'email' in contact_info:
            contact_score += 4
        if 'phone' in contact_info:
            contact_score += 4
        if 'name' in contact_info:
            contact_score += 2
        score += min(contact_score, 10)
        
        # 5. Readability & Formatting Score (10 points)
        readability = self.calculate_readability_score(text)
        if readability >= 80:
            score += 10
        elif readability >= 60:
            score += 8
        elif readability >= 40:
            score += 5
        elif readability >= 20:
            score += 2
        
        # 6. Industry Keywords Density Score (10 points)
        industry_keywords = self._extract_industry_keywords(text)
        if industry_keywords:
            keyword_density = len(industry_keywords) / word_count * 1000  # per 1000 words
            if keyword_density >= 5:
                score += 10
            elif keyword_density >= 3:
                score += 8
            elif keyword_density >= 1:
                score += 5
            elif keyword_keywords := industry_keywords:
                score += 2
        
        # 7. Experience Indicators Score (5 points)
        experience_patterns = [
            r'\d+\+?\s*(years?|tahun)\s*(of\s*)?(experience|exp)',
            r'senior|lead|principal|manager|director',
            r'project\s+(lead|manager|coordinator)',
            r'team\s+(lead|head|supervisor)'
        ]
        
        exp_matches = sum(1 for pattern in experience_patterns if re.search(pattern, text.lower()))
        if exp_matches >= 3:
            score += 5
        elif exp_matches >= 2:
            score += 3
        elif exp_matches >= 1:
            score += 1
        
        # 8. Education Indicators Score (5 points)
        education_patterns = [
            r'bachelor|master|phd|doctorate',
            r'universit(y|as)|college|institute',
            r'degree|diploma|certificate',
            r'gpa|grade|academic'
        ]
        
        edu_matches = sum(1 for pattern in education_patterns if re.search(pattern, text.lower()))
        if edu_matches >= 3:
            score += 5
        elif edu_matches >= 2:
            score += 3
        elif edu_matches >= 1:
            score += 1
        
        # 9. Action Words & Achievements Score (5 points)
        action_words = [
            'managed', 'developed', 'implemented', 'led', 'created', 'designed', 'analyzed',
            'improved', 'increased', 'reduced', 'optimized', 'coordinated', 'delivered'
        ]
        
        action_count = sum(1 for word in action_words if word in text.lower())
        if action_count >= 8:
            score += 5
        elif action_count >= 5:
            score += 3
        elif action_count >= 2:
            score += 1
        
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
        """Enhanced CV text processing pipeline with optimization"""
        if not text:
            return {
                'extracted_skills': [],
                'keywords': [],
                'contact_info': {},
                'text_analysis': {},
                'ats_score': 0,
                'completeness_score': 0,
                'language_detected': 'unknown',
                'experience_level': 'unknown',
                'education_level': 'unknown',
                'industry_classification': 'general',
                'confidence_score': 0,
                'total_years': 0
            }
        
        # Enhanced processing pipeline
        # 1. Language detection
        language_detected = self.detect_language(text)
        
        # 2. Extract skills (with language awareness)
        extracted_skills = self.extract_skills(text)
        
        # 3. Extract keywords
        keywords = self.extract_keywords(text, max_keywords=15)
        
        # 4. Extract contact info
        contact_info = self.extract_contact_info(text)
        
        # 5. Analyze text structure
        text_analysis = self.analyze_text_structure(text)
        
        # 6. Enhanced analysis
        experience_level, total_years = self.detect_experience_level(text)
        education_level, _, institution_score = self.detect_education_level(text)
        industry_classification, industry_confidence = self.enhanced_industry_classification(text, extracted_skills)
        
        # 7. Calculate scores
        ats_score = self.calculate_ats_score(text, extracted_skills)
        completeness_score = self._calculate_completeness_score(
            extracted_skills, contact_info, text_analysis
        )
        
        # Compile data for confidence calculation
        extracted_data = {
            'extracted_skills': extracted_skills,
            'keywords': keywords,
            'contact_info': contact_info,
            'text_analysis': text_analysis,
            'ats_score': ats_score,
            'completeness_score': completeness_score,
            'language_detected': language_detected,
            'experience_level': experience_level,
            'education_level': education_level,
            'industry_classification': industry_classification,
            'total_years': total_years,
            'institution_score': institution_score,
            'industry_confidence': industry_confidence
        }
        
        # 8. Calculate detection confidence
        confidence_score = self.calculate_detection_confidence(extracted_data)
        
        return {
            'extracted_skills': extracted_skills,
            'keywords': keywords,
            'contact_info': contact_info,
            'text_analysis': text_analysis,
            'ats_score': round(ats_score, 1),
            'completeness_score': round(completeness_score, 1),
            'language_detected': language_detected,
            'experience_level': experience_level,
            'education_level': education_level,
            'industry_classification': industry_classification,
            'confidence_score': confidence_score,
            'total_years': total_years,
            'institution_score': institution_score,
            'industry_confidence': round(industry_confidence, 2),
            'metadata': {
                'skills_count': len(extracted_skills),
                'keywords_count': len(keywords),
                'sections_found': len(text_analysis.get('has_sections', [])),
                'readability_score': text_analysis.get('readability_score', 0),
                'word_count': text_analysis.get('word_count', 0)
            }
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
