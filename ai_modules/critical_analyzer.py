"""
Critical Analyzer Module
Provides deep, critical analysis of CV content with Indonesian business context
"""

import re
import json
from collections import Counter, defaultdict
from datetime import datetime
import statistics

class CriticalAnalyzer:
    """Advanced critical analysis engine for CV content evaluation"""
    
    def __init__(self):
        # Indonesian business culture context
        self.indonesian_business_context = {
            'education_hierarchy': {
                'top_tier': ['ui', 'itb', 'ugm', 'telkom university', 'binus', '见见', '见见', '见见'],
                'international': ['overseas', 'luar negeri', 'singapore', 'australia', 'netherlands', 'usa', 'uk'],
                'accredited': ['terakreditasi', 'ban-pt', 'a', 'b', 'c'],
                'technical': ['politeknik', 'stm', 'smk', 'd1', 'd2', 'd3', 'd4']
            },
            'industry_maturity': {
                'traditional': ['banking', 'manufacturing', 'oil & gas', 'palm oil', 'mining'],
                'emerging': ['fintech', 'edtech', 'healthtech', 'e-commerce', 'startup'],
                'digital': ['technology', 'software', 'digital marketing', 'data science']
            },
            'career_progression_indicators': {
                'accelerated': ['fast-track', 'promoted', 'early promotion', 'rapid growth'],
                'standard': ['progressive', 'steady', 'consistent'],
                'stagnant': ['static', 'no growth', 'plateau']
            }
        }
        
        # Quality indicators and red flags
        self.quality_indicators = {
            'high_quality': [
                'quantified achievements', 'metrics', 'percentages', 'numbers',
                'leadership', 'mentored', 'improved', 'increased', 'reduced',
                'managed', 'delivered', 'achieved', 'recognized', 'awarded'
            ],
            'medium_quality': [
                'responsible for', 'involved in', 'participated', 'assisted',
                'supported', 'helped', 'contributed to', 'worked on'
            ],
            'low_quality': [
                'duties include', 'tasks include', 'worked as', 'assigned to',
                'basic', 'simple', 'routine', 'standard'
            ],
            'red_flags': [
                'fired', 'terminated', 'left due to', 'resigned suddenly',
                'gap', 'unexplained', 'vague', 'minimal', 'limited experience'
            ]
        }
        
        # Achievement validation patterns
        self.achievement_patterns = {
            'quantifiable': [
                r'\d+%', r'\d+x', r'\d+ million', r'\d+ billion', r'\$\d+',
                r'\d+ tahun', r'\d+ bulan', r'\d+ orang', r'\d+ proyek'
            ],
            'impact': [
                'improved', 'increased', 'reduced', 'saved', 'optimized',
                'enhanced', 'streamlined', 'accelerated', 'innovated'
            ],
            'responsibility': [
                'managed', 'led', 'directed', 'oversaw', 'coordinated',
                'supervised', 'headed', 'spearheaded', 'championed'
            ]
        }
        
        # Indonesian CV writing patterns
        self.indonesian_cv_patterns = {
            'formal_opening': [
                'dengan hormat', 'sehubungan dengan', 'berdasarkan',
                'dalam rangka', 'sesuai dengan', 'merujuk pada'
            ],
            'achievement_style': [
                'berhasil', 'sukses', 'mencapai', 'meraih', 'memperoleh',
                'mendapatkan', 'menang', 'juara', 'terpilih', 'ditunjuk'
            ],
            'responsibility_style': [
                'bertanggung jawab', 'dipercaya', 'ditunjuk', 'diberikan tugas',
                'menangani', 'mengelola', 'memimpin', 'mengawasi'
            ]
        }
    
    def analyze_content_quality(self, text, extracted_skills):
        """Comprehensive content quality analysis"""
        if not text:
            return {'score': 0, 'issues': [], 'strengths': []}
        
        analysis = {
            'score': 0,
            'issues': [],
            'strengths': [],
            'details': {}
        }
        
        # 1. Content Depth Analysis
        depth_score = self._analyze_content_depth(text)
        analysis['details']['content_depth'] = depth_score
        
        # 2. Achievement Quality Analysis
        achievement_score = self._analyze_achievement_quality(text)
        analysis['details']['achievement_quality'] = achievement_score
        
        # 3. Language Professionalism
        language_score = self._analyze_language_professionalism(text)
        analysis['details']['language_professionalism'] = language_score
        
        # 4. Structure and Organization
        structure_score = self._analyze_structure_organization(text)
        analysis['details']['structure_organization'] = structure_score
        
        # 5. Consistency Analysis
        consistency_score = self._analyze_consistency(text, extracted_skills)
        analysis['details']['consistency'] = consistency_score
        
        # Calculate overall score
        weights = {
            'content_depth': 0.25,
            'achievement_quality': 0.30,
            'language_professionalism': 0.20,
            'structure_organization': 0.15,
            'consistency': 0.10
        }
        
        overall_score = sum(
            analysis['details'][key]['score'] * weight 
            for key, weight in weights.items()
        )
        
        analysis['score'] = round(overall_score, 1)
        
        # Aggregate issues and strengths
        for detail in analysis['details'].values():
            analysis['issues'].extend(detail.get('issues', []))
            analysis['strengths'].extend(detail.get('strengths', []))
        
        return analysis
    
    def _analyze_content_depth(self, text):
        """Analyze depth and richness of content"""
        result = {'score': 0, 'issues': [], 'strengths': []}
        
        word_count = len(text.split())
        sentence_count = len(re.split(r'[.!?]+', text))
        
        # Content length analysis
        if 300 <= word_count <= 800:
            result['strengths'].append("panjang konten optimal untuk CV")
            result['score'] += 20
        elif 200 <= word_count <= 1000:
            result['score'] += 15
        elif word_count < 200:
            result['issues'].append("konten terlalu singkat - kurang detail")
            result['score'] += 5
        else:
            result['issues'].append("konten terlalu panjang - perlu diringkas")
            result['score'] += 10
        
        # Sentence complexity analysis
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        if 12 <= avg_words_per_sentence <= 20:
            result['strengths'].append("kalimat memiliki panjang yang baik")
            result['score'] += 15
        elif avg_words_per_sentence > 25:
            result['issues'].append("kalimat terlalu panjang - sulit dipahami")
            result['score'] += 5
        else:
            result['score'] += 10
        
        # Content analysis
        unique_words = len(set(text.lower().split()))
        word_diversity = unique_words / word_count if word_count > 0 else 0
        
        if word_diversity > 0.7:
            result['strengths'].append("kosakata beragam dan kaya")
            result['score'] += 15
        elif word_diversity > 0.5:
            result['score'] += 10
        else:
            result['issues'].append("kosakata kurang beragam - repetitif")
            result['score'] += 5
        
        result['score'] = min(result['score'], 100)
        return result
    
    def _analyze_achievement_quality(self, text):
        """Analyze quality of achievements and accomplishments"""
        result = {'score': 0, 'issues': [], 'strengths': []}
        
        text_lower = text.lower()
        
        # Quantifiable achievements
        quantifiable_matches = []
        for pattern in self.achievement_patterns['quantifiable']:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            quantifiable_matches.extend(matches)
        
        if len(quantifiable_matches) >= 5:
            result['strengths'].append(f"banyak pencapaian terukur ({len(quantifiable_matches)} data numerik)")
            result['score'] += 25
        elif len(quantifiable_matches) >= 2:
            result['score'] += 15
        elif len(quantifiable_matches) == 1:
            result['score'] += 8
        else:
            result['issues'].append("kurang pencapaian terukur dengan angka konkret")
        
        # Impact indicators
        impact_score = 0
        for impact_word in self.achievement_patterns['impact']:
            if impact_word in text_lower:
                impact_score += 2
        
        if impact_score >= 8:
            result['strengths'].append("banyak menunjukkan dampak positif")
            result['score'] += 20
        elif impact_score >= 4:
            result['score'] += 12
        elif impact_score >= 2:
            result['score'] += 6
        else:
            result['issues'].append("kurang menunjukkan dampak konkret dari pekerjaan")
        
        # Responsibility indicators
        responsibility_score = 0
        for resp_word in self.achievement_patterns['responsibility']:
            if resp_word in text_lower:
                responsibility_score += 2
        
        if responsibility_score >= 6:
            result['strengths'].append("menunjukkan tanggung jawab yang kuat")
            result['score'] += 15
        elif responsibility_score >= 3:
            result['score'] += 10
        else:
            result['issues'].append("tanggung jawab kurang jelas")
        
        # Red flags detection
        red_flag_count = 0
        for red_flag in self.quality_indicators['red_flags']:
            if red_flag in text_lower:
                red_flag_count += 1
        
        if red_flag_count > 0:
            result['issues'].append(f"terdeteksi {red_flag_count} indikasi masalah")
            result['score'] -= red_flag_count * 5
        
        result['score'] = max(0, min(result['score'], 100))
        return result
    
    def _analyze_language_professionalism(self, text):
        """Analyze professionalism of language used"""
        result = {'score': 0, 'issues': [], 'strengths': []}
        
        text_lower = text.lower()
        
        # Indonesian business language detection
        formal_indicators = 0
        for pattern in self.indonesian_cv_patterns['formal_opening']:
            if pattern in text_lower:
                formal_indicators += 1
        
        for pattern in self.indonesian_cv_patterns['achievement_style']:
            if pattern in text_lower:
                formal_indicators += 1
        
        for pattern in self.indonesian_cv_patterns['responsibility_style']:
            if pattern in text_lower:
                formal_indicators += 1
        
        if formal_indicators >= 5:
            result['strengths'].append("bahasa formal dan profesional Indonesia")
            result['score'] += 25
        elif formal_indicators >= 3:
            result['score'] += 15
        elif formal_indicators >= 1:
            result['score'] += 8
        else:
            result['issues'].append("bahasa kurang formal untuk konteks bisnis Indonesia")
        
        # English proficiency indicators
        english_indicators = [
            'english', 'fluent', 'proficient', 'native speaker',
            'bilingual', 'international', 'global', 'multicultural'
        ]
        
        english_score = sum(1 for indicator in english_indicators if indicator in text_lower)
        if english_score >= 2:
            result['strengths'].append("menunjukkan kemampuan bahasa Inggris")
            result['score'] += 15
        elif english_score >= 1:
            result['score'] += 8
        
        # Grammar and spelling quality (basic check)
        common_errors = [
            'tdk', 'tdak', 'gk', 'gak', 'bgt', 'banget', 'sgt', 'sekali'
        ]
        
        informal_count = sum(1 for error in common_errors if error in text_lower)
        if informal_count == 0:
            result['strengths'].append("tidak ada singkatan informal")
            result['score'] += 10
        else:
            result['issues'].append(f"terdeteksi {informal_count} singkatan informal")
        
        result['score'] = min(result['score'], 100)
        return result
    
    def _analyze_structure_organization(self, text):
        """Analyze structure and organization of CV"""
        result = {'score': 0, 'issues': [], 'strengths': []}
        
        lines = text.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        # Section headers detection
        common_headers = [
            'pengalaman kerja', 'work experience', 'pendidikan', 'education',
            'keahlian', 'skills', 'ringkasan', 'summary', 'tentang', 'about',
            'penghargaan', 'awards', 'sertifikasi', 'certifications'
        ]
        
        header_count = 0
        for line in non_empty_lines:
            if any(header.lower() in line.lower() for header in common_headers):
                header_count += 1
        
        if header_count >= 4:
            result['strengths'].append("struktur CV lengkap dengan section yang jelas")
            result['score'] += 30
        elif header_count >= 2:
            result['score'] += 20
        elif header_count >= 1:
            result['score'] += 10
        else:
            result['issues'].append("struktur section kurang jelas")
        
        # Chronological order check
        years = re.findall(r'\b(19|20)\d{2}\b', text)
        if len(years) >= 2:
            try:
                year_list = [int(year) for year in years]
                if year_list == sorted(year_list, reverse=True):
                    result['strengths'].append("pengalaman tersusun kronologis (terbaru ke terlama)")
                    result['score'] += 20
                else:
                    result['issues'].append("urutan kronologis tidak konsisten")
            except:
                result['score'] += 10
        else:
            result['score'] += 5
        
        # Bullet points and formatting
        bullet_patterns = ['•', '-', '*', '→', '▪', '▫']
        bullet_count = sum(text.count(pattern) for pattern in bullet_patterns)
        
        if bullet_count >= 5:
            result['strengths'].append("menggunakan bullet points untuk kemudahan baca")
            result['score'] += 15
        elif bullet_count >= 2:
            result['score'] += 10
        else:
            result['issues'].append("kurang penggunaan bullet points untuk pencapaian")
        
        # Contact information placement
        contact_patterns = [r'@[\w.-]+', r'\+62\d{10,13}', r'\(\d{3}\)\s*\d{3}-\d{4}']
        contact_found = any(re.search(pattern, text) for pattern in contact_patterns)
        
        if contact_found:
            result['strengths'].append("informasi kontak tersedia")
            result['score'] += 10
        else:
            result['issues'].append("informasi kontak tidak jelas atau tidak ada")
        
        result['score'] = min(result['score'], 100)
        return result
    
    def _analyze_consistency(self, text, extracted_skills):
        """Analyze consistency across different sections"""
        result = {'score': 0, 'issues': [], 'strengths': []}
        
        text_lower = text.lower()
        
        # Skills consistency check
        if extracted_skills:
            skills_mentioned_in_text = 0
            for skill in extracted_skills[:10]:  # Check top 10 skills
                if skill.lower() in text_lower:
                    skills_mentioned_in_text += 1
            
            skills_mention_rate = skills_mentioned_in_text / min(len(extracted_skills), 10)
            
            if skills_mention_rate >= 0.7:
                result['strengths'].append("keahlian konsisten disebutkan dalam pengalaman")
                result['score'] += 25
            elif skills_mention_rate >= 0.4:
                result['score'] += 15
            else:
                result['issues'].append("beberapa keahlian tidak dijelaskan dalam pengalaman")
        
        # Experience level consistency
        experience_indicators = {
            'junior': ['junior', 'entry', 'fresh', 'graduate'],
            'senior': ['senior', 'lead', 'principal', 'manager', 'director'],
            'expert': ['expert', 'specialist', 'consultant', 'architect']
        }
        
        level_scores = {}
        for level, indicators in experience_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text_lower)
            level_scores[level] = score
        
        if level_scores:
            dominant_level = max(level_scores, key=level_scores.get)
            max_score = level_scores[dominant_level]
            
            if max_score >= 3:
                result['strengths'].append(f"tingkat pengalaman {dominant_level} konsisten")
                result['score'] += 20
            elif max_score >= 1:
                result['score'] += 10
            else:
                result['issues'].append("tingkat pengalaman tidak konsisten")
        
        # Education-experience alignment
        education_level = self._detect_education_level(text)
        experience_years = self._extract_experience_years(text)
        
        if education_level and experience_years:
            alignment_score = self._check_education_experience_alignment(
                education_level, experience_years
            )
            if alignment_score >= 0.8:
                result['strengths'].append("pendidikan dan pengalaman selaras")
                result['score'] += 15
            elif alignment_score >= 0.6:
                result['score'] += 10
            else:
                result['issues'].append("kesenjangan antara pendidikan dan pengalaman")
        
        result['score'] = min(result['score'], 100)
        return result
    
    def _detect_education_level(self, text):
        """Detect education level from text"""
        text_lower = text.lower()
        
        education_patterns = {
            'phd': ['phd', 'doctorate', 'doctoral'],
            'master': ['master', 'magister', 's2', 'mba', 'msc'],
            'bachelor': ['bachelor', 'sarjana', 's1', 'undergraduate'],
            'diploma': ['diploma', 'd3', 'd4', 'associate'],
            'high_school': ['sma', 'smk', 'high school']
        }
        
        for level, patterns in education_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                return level
        
        return None
    
    def _extract_experience_years(self, text):
        """Extract total years of experience"""
        year_patterns = [
            r'(\d+)\+?\s*(years?|tahun)\s*(of\s*)?(experience|exp)',
            r'(\d+)\+?\s*years?\s*(in|of)',
            r'(\d+)\+?\s*tahun\s*(pengalaman|kerja)',
        ]
        
        max_years = 0
        for pattern in year_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                try:
                    years = int(match[0])
                    max_years = max(max_years, years)
                except:
                    pass
        
        return max_years
    
    def _check_education_experience_alignment(self, education_level, experience_years):
        """Check alignment between education level and experience"""
        alignment_matrix = {
            ('phd', 0): 0.9, ('phd', 5): 1.0, ('phd', 10): 1.0,
            ('master', 0): 0.8, ('master', 3): 0.9, ('master', 7): 1.0,
            ('bachelor', 0): 0.7, ('bachelor', 2): 0.8, ('bachelor', 5): 0.9,
            ('diploma', 0): 0.6, ('diploma', 1): 0.8, ('diploma', 3): 0.9,
            ('high_school', 0): 0.5, ('high_school', 2): 0.7, ('high_school', 5): 0.8
        }
        
        # Find closest match
        for (edu, exp), score in alignment_matrix.items():
            if edu == education_level and exp <= experience_years:
                return score
        
        return 0.6  # Default score
    
    def identify_critical_gaps(self, extracted_data):
        """Identify critical gaps in CV that need immediate attention"""
        gaps = {
            'critical': [],
            'important': [],
            'minor': []
        }
        
        ats_score = extracted_data.get('ats_score', 0)
        skills_count = len(extracted_data.get('extracted_skills', []))
        contact_info = extracted_data.get('contact_info', {})
        industry_benchmarks = extracted_data.get('industry_benchmarks', {})
        
        # Critical gaps
        if ats_score < 50:
            gaps['critical'].append("ATS Score sangat rendah - CV tidak akan terdeteksi sistem rekrutmen")
        
        if not contact_info.get('email'):
            gaps['critical'].append("Email tidak ditemukan - Informasi kontak wajib tidak lengkap")
        
        if skills_count < 3:
            gaps['critical'].append("Keahlian terlalu sedikit - kurang dari 3 skills teridentifikasi")
        
        if industry_benchmarks and industry_benchmarks.get('essential_skills_missing', []):
            missing_essential = industry_benchmarks['essential_skills_missing']
            if len(missing_essential) > 3:
                gaps['critical'].append(f"Terlalu banyak keahlian inti industri yang missing ({len(missing_essential)} skills)")
        
        # Important gaps
        if not contact_info.get('phone'):
            gaps['important'].append("Nomor telepon tidak ditemukan")
        
        if not contact_info.get('name'):
            gaps['important'].append("Nama tidak jelas teridentifikasi")
        
        if ats_score < 70:
            gaps['important'].append("ATS Score perlu perbaikan untuk optimasi aplikasi kerja")
        
        if skills_count < 8:
            gaps['important'].append("Keahlian perlu diperkaya (minimal 8-10 skills)")
        
        if industry_benchmarks and industry_benchmarks.get('preferred_skills_missing', []):
            missing_preferred = industry_benchmarks['preferred_skills_missing']
            if len(missing_preferred) > 2:
                gaps['important'].append(f"Keahlian preferensi industri perlu ditambahkan ({len(missing_preferred)} skills)")
        
        # Minor gaps
        if extracted_data.get('experience_level') == 'unknown':
            gaps['minor'].append("Tingkat pengalaman tidak terdeteksi dengan jelas")
        
        if extracted_data.get('education_level') == 'unknown':
            gaps['minor'].append("Pendidikan tidak terdeteksi dengan jelas")
        
        if extracted_data.get('years_experience', 0) == 0:
            gaps['minor'].append("Tahun pengalaman tidak terdeteksi")
        
        return gaps
    
    def generate_critical_feedback(self, content_analysis, gap_analysis, extracted_data=None):
        """Generate specific, actionable critical feedback"""
        feedback = {
            'immediate_actions': [],
            'priority_improvements': [],
            'strengths_to_leverage': [],
            'strategic_recommendations': []
        }
        
        # Use extracted_data if provided, otherwise use empty dict
        if extracted_data is None:
            extracted_data = {}
        
        # Critical gaps -> Immediate actions
        for gap in gap_analysis['critical']:
            if 'ATS Score' in gap:
                feedback['immediate_actions'].append(
                    "🔴 PRIORITAS TINGGI: Segera optimasi ATS dengan menambah keywords industri, "
                    "memperbaiki formatting, dan memastikan struktur standar (Experience, Education, Skills)"
                )
            elif 'Email' in gap:
                feedback['immediate_actions'].append(
                    "🔴 PRIORITAS TINGGI: Tambahkan email profesional yang jelas di bagian atas CV"
                )
            elif 'Keahlian terlalu sedikit' in gap:
                feedback['immediate_actions'].append(
                    "🔴 PRIORITAS TINGGI: Perluas section skills dengan minimal 8-10 keahlian relevan"
                )
            elif 'missing' in gap:
                feedback['immediate_actions'].append(
                    "🔴 PRIORITAS TINGGI: Tambahkan keahlian inti industri yang hilang dari CV"
                )
        
        # Important gaps -> Priority improvements
        for gap in gap_analysis['important']:
            if 'Nomor telepon' in gap:
                feedback['priority_improvements'].append(
                    "🟡 PENTING: Tambahkan nomor telepon dengan format (+62 xxx xxxx xxxx)"
                )
            elif 'ATS Score' in gap:
                feedback['priority_improvements'].append(
                    "🟡 PENTING: Tingkatkan ATS score dengan optimasi keywords dan formatting"
                )
            elif 'Keahlian perlu diperkaya' in gap:
                feedback['priority_improvements'].append(
                    "🟡 PENTING: Kembangkan portfolio skills yang lebih komprehensif"
                )
        
        # Content analysis strengths
        for strength in content_analysis.get('strengths', []):
            if 'optimal' in strength or 'lengkap' in strength:
                feedback['strengths_to_leverage'].append(
                    f"✅ KEKUATAN: {strength} - Manfaatkan sebagai卖点 utama"
                )
            elif 'terukur' in strength or 'numerik' in strength:
                feedback['strengths_to_leverage'].append(
                    f"✅ KEKUATAN: {strength} - Tingkatkan dengan lebih banyak data konkret"
                )
        
        # Strategic recommendations
        if content_analysis.get('score', 0) >= 70:
            feedback['strategic_recommendations'].append(
                "📈 STRATEGIS: CV memiliki kualitas baik - fokus pada personal branding dan networking"
            )
        else:
            feedback['strategic_recommendations'].append(
                "📈 STRATEGIS: Lakukan perbaikan fundamental sebelum aplica ke posisi strategis"
            )
        
        # Industry-specific recommendations
        detected_industry = extracted_data.get('detected_industry', 'general')
        if detected_industry != 'general':
            industry_rec = self._get_industry_specific_advice(detected_industry)
            feedback['strategic_recommendations'].extend(industry_rec)
        
        return feedback
    
    def _get_industry_specific_advice(self, industry):
        """Get industry-specific strategic advice"""
        advice_map = {
            'technology': [
                "💻 TEKNOLOGI: Highlight technical skills dan programming languages",
                "💻 TEKNOLOGI: Tambahkan portfolio GitHub atau project samples",
                "💻 TEKNOLOGI: Mention experience dengan cloud platforms dan tools modern"
            ],
            'finance': [
                "💰 KEUANGAN: Emphasize analytical skills dan financial tools expertise",
                "💰 KEUANGAN: Highlight certifications seperti CFA, CPA, atau FRM",
                "💰 KEUANGAN: Tunjukkan experience dengan regulatory compliance"
            ],
            'marketing': [
                "📱 MARKETING: Showcase digital marketing tools dan analytics skills",
                "📱 MARKETING: Highlight campaign results dan ROI achievements",
                "📱 MARKETING: Mention experience dengan social media dan content creation"
            ],
            'healthcare': [
                "🏥 KESEHATAN: Emphasize patient care experience dan medical knowledge",
                "🏥 KESEHATAN: Highlight certifications dan continuing education",
                "🏥 KESEHATAN: Tunjukkan experience dengan healthcare technology"
            ]
        }
        
        return advice_map.get(industry, [
            f"🏢 {industry.upper()}: Research industry-specific keywords untuk optimasi"
        ])
    
    def analyze_cv_credibility(self, text, extracted_data):
        """Analyze CV credibility and authenticity indicators"""
        credibility = {
            'score': 0,
            'red_flags': [],
            'trust_indicators': [],
            'verification_suggestions': []
        }
        
        text_lower = text.lower()
        
        # Positive credibility indicators
        positive_indicators = [
            'certified', 'certification', 'degree', 'university', 'gpa',
            'award', 'recognition', 'achievement', 'graduated', 'honor'
        ]
        
        trust_score = sum(1 for indicator in positive_indicators if indicator in text_lower)
        
        # Educational institution verification
        universities = re.findall(r'\b(UI|ITB|UGM|Binus|Telkom|ITS|UNPAD|UNAIR)\b', text, re.IGNORECASE)
        if universities:
            credibility['trust_indicators'].append(f"Institusi pendidikan ternama: {', '.join(universities)}")
            trust_score += len(universities)
        
        # Achievement specificity check
        specific_achievements = len(re.findall(r'\d+%|\$\d+|\d+ (million|billion)', text_lower))
        if specific_achievements >= 3:
            credibility['trust_indicators'].append("Pencapaian dengan detail numerik spesifik")
            trust_score += 2
        elif specific_achievements == 0:
            credibility['red_flags'].append("Kurang pencapaian terukur yang spesifik")
        
        # Time consistency check
        years = re.findall(r'\b(19|20)\d{2}\b', text)
        if len(years) >= 2:
            try:
                year_list = sorted([int(year) for year in years])
                gaps = []
                for i in range(1, len(year_list)):
                    gap = year_list[i] - year_list[i-1]
                    gaps.append(gap)
                
                if max(gaps) > 5:
                    credibility['red_flags'].append("Terdeteksi gap waktu yang mencurigakan dalam karir")
                else:
                    credibility['trust_indicators'].append("Timeline karir konsisten tanpa gap mencurigakan")
            except:
                pass
        
        # Language consistency
        mixed_language_score = 0
        indonesian_words = ['yang', 'dan', 'di', 'dari', 'untuk', 'dengan']
        english_words = ['the', 'and', 'of', 'in', 'for', 'with']
        
        indonesian_count = sum(1 for word in indonesian_words if f' {word} ' in f' {text_lower} ')
        english_count = sum(1 for word in english_words if f' {word} ' in f' {text_lower} ')
        
        if indonesian_count > 0 and english_count > 0:
            mixed_language_score = min(indonesian_count, english_count)
            if mixed_language_score > 5:
                credibility['red_flags'].append("Campuran bahasa Indonesia-English yang tidak konsisten")
        
        # Calculate final credibility score
        credibility['score'] = min(100, trust_score * 10 + 50)  # Base score 50, +10 per trust indicator
        
        # Verification suggestions
        if credibility['score'] < 70:
            credibility['verification_suggestions'].append("Pertimbangkan verifikasi pendidikan dan pengalaman kerja")
        
        if len(credibility['red_flags']) > 2:
            credibility['verification_suggestions'].append("CV memerlukan klarifikasi untuk beberapa poin yang meragukan")
        
        return credibility
    
    def generate_comprehensive_critical_analysis(self, extracted_data):
        """Generate complete critical analysis report"""
        text = extracted_data.get('extracted_text', '')
        extracted_skills = extracted_data.get('extracted_skills', [])
        
        # Perform all analyses
        content_analysis = self.analyze_content_quality(text, extracted_skills)
        gap_analysis = self.identify_critical_gaps(extracted_data)
        credibility_analysis = self.analyze_cv_credibility(text, extracted_data)
        
        # Generate feedback
        critical_feedback = self.generate_critical_feedback(content_analysis, gap_analysis, extracted_data)
        
        # Compile comprehensive report
        report = {
            'overall_score': content_analysis['score'],
            'content_quality': content_analysis,
            'critical_gaps': gap_analysis,
            'credibility_analysis': credibility_analysis,
            'critical_feedback': critical_feedback,
            'analysis_timestamp': datetime.now().isoformat(),
            'analysis_version': '2.0-critical'
        }
        
        return report
