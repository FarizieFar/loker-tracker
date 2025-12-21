"""
Feedback Generator Module
Generates intelligent, specific, and actionable feedback for CV improvements
"""

import json
from datetime import datetime
from collections import defaultdict

class FeedbackGenerator:
    """Intelligent feedback generation system for CV improvements"""
    
    def __init__(self):
        # Indonesian business culture feedback templates
        self.feedback_templates = {
            'critical_ats': {
                'title': '🚨 KRITIS: Optimasi ATS Mendesak',
                'content': 'CV Anda tidak akan terdeteksi dengan baik oleh sistem rekrutmen otomatis. Segera lakukan optimasi berikut:',
                'actions': [
                    'Tambahkan 15-20 keywords spesifik dari job descriptions target',
                    'Gunakan section headers standar: "Pengalaman Kerja", "Pendidikan", "Keahlian"',
                    'Hilangkan formatting kompleks (tabel, teksbox, gambar)',
                    'Pastikan informasi kontak di bagian paling atas'
                ]
            },
            'low_skills': {
                'title': '⚠️ PENTING: Portfolio Keahlian Perlu Diperluas',
                'content': 'CV Anda menunjukkan terlalu sedikit keahlian untuk menarik perhatian recruiter:',
                'actions': [
                    'Tambahkan minimal 8-10 keahlian teknis relevan',
                    'Group skills berdasarkan kategori (Programming, Tools, dll)',
                    'Include both hard skills dan soft skills',
                    'Pastikan skills sesuai dengan posisi yang ditarget'
                ]
            },
            'missing_contact': {
                'title': '🚨 KRITIS: Informasi Kontak Tidak Lengkap',
                'content': 'Informasi kontak adalah elemen wajib yang hilang dari CV Anda:',
                'actions': [
                    'Tambahkan email profesional (nama@perusahaan.com)',
                    'Sertakan nomor telepon dengan format (+62 xxx xxxx xxxx)',
                    'Pertimbangkan menambah LinkedIn profile',
                    'Pastikan semua informasi kontak up-to-date'
                ]
            },
            'achievement_gap': {
                'title': '📊 PENTING: Kekurangan Pencapaian Terukur',
                'content': 'CV Anda kurang menunjukkan impact konkret dari kontribusi Anda:',
                'actions': [
                    'Tambahkan angka spesifik: "Meningkatkan penjualan 25%"',
                    'Gunakan action verbs: "Mengelola", "Menciptakan", "Mengoptimalkan"',
                    'Sebutkan team size yang pernah dikelola',
                    'Highlight project budget yang pernah ditangani'
                ]
            },
            'indonesian_context': {
                'title': '🇮🇩 KONTEKS INDONESIA: Sesuaikan dengan Budaya Bisnis Lokal',
                'content': 'Untuk pasar kerja Indonesia, pertimbangkan hal-hal berikut:',
                'actions': [
                    'Gunakan bahasa Indonesia yang formal dan profesional',
                    'Sebutkan institusi pendidikan yang terakreditasi BAN-PT',
                    'Highlight pengalaman di perusahaan besar Indonesia',
                    'Tambahkan sertifikasi yang diakui di Indonesia'
                ]
            }
        }
        
        # Industry-specific feedback patterns
        self.industry_feedback = {
            'technology': {
                'missing_skills': [
                    '💻 KEANEHAN TEKNOLOGI: Tambahkan programming languages (Python, Java, JavaScript)',
                    '💻 KEANEHAN TEKNOLOGI: Include cloud platforms (AWS, Azure, GCP)',
                    '💻 KEANEHAN TEKNOLOGI: Mention framework expertise (React, Angular, Spring)',
                    '💻 KEANEHAN TEKNOLOGI: Tambahkan DevOps tools (Docker, Kubernetes, CI/CD)'
                ],
                'strengths': [
                    '✅ TEKNOLOGI: Strong technical foundation terdeteksi',
                    '✅ TEKNOLOGI: Modern technology stack awareness',
                    '✅ TEKNOLOGI: Programming skills well-documented'
                ]
            },
            'finance': {
                'missing_skills': [
                    '💰 KEUANGAN: Sertakan financial modeling skills (Excel, Bloomberg)',
                    '💰 KEUANGAN: Tambahkan regulatory knowledge (OJK, Bank Indonesia)',
                    '💰 KEUANGAN: Highlight risk management experience',
                    '💰 KEUANGAN: Mention audit dan compliance skills'
                ],
                'strengths': [
                    '✅ KEUANGAN: Strong analytical skills base',
                    '✅ KEUANGAN: Financial industry knowledge',
                    '✅ KEUANGAN: Quantitative analysis capability'
                ]
            },
            'marketing': {
                'missing_skills': [
                    '📱 MARKETING: Include digital marketing tools (Google Ads, Facebook Ads)',
                    '📱 MARKETING: Tambahkan analytics skills (Google Analytics, Facebook Analytics)',
                    '📱 MARKETING: Highlight content creation abilities',
                    '📱 MARKETING: Mention SEO/SEM expertise'
                ],
                'strengths': [
                    '✅ MARKETING: Strong communication skills',
                    '✅ MARKETING: Creative thinking capability',
                    '✅ MARKETING: Customer-focused mindset'
                ]
            },
            'healthcare': {
                'missing_skills': [
                    '🏥 KESEHATAN: Sertakan medical knowledge dan certifications',
                    '🏥 KESEHATAN: Tambahkan patient care experience',
                    '🏥 KESEHATAN: Highlight healthcare technology familiarity',
                    '🏥 KESEHATAN: Mention regulatory compliance (HIPAA, Kemenkes)'
                ],
                'strengths': [
                    '✅ KESEHATAN: Strong patient care orientation',
                    '✅ KESEHATAN: Medical knowledge foundation',
                    '✅ KESEHATAN: Healthcare industry understanding'
                ]
            }
        }
        
        # Career level specific advice
        self.career_level_advice = {
            'junior': {
                'focus_areas': [
                    '🎯 FOKUS KARIR JUNIOR: Highlight learning ability dan eagerness to grow',
                    '🎯 FOKUS KARIR JUNIOR: Mention academic projects dan internship experience',
                    '🎯 FOKUS KARIR JUNIOR: Showcase technical foundation dan certifications',
                    '🎯 FOKUS KARIR JUNIOR: Emphasize team collaboration skills'
                ],
                'common_mistakes': [
                    '❌ MISTAKE JUNIOR: Jangan overstated experience - be honest about skill level',
                    '❌ MISTAKE JUNIOR: Hindari responsibilities yang unrealistic untuk junior level',
                    '❌ MISTAKE JUNIOR: Jangan focus pada leadership yang belum pernah dilakukan'
                ]
            },
            'mid': {
                'focus_areas': [
                    '🎯 FOKUS KARIR MID-LEVEL: Showcase project management experience',
                    '🎯 FOKUS KARIR MID-LEVEL: Highlight problem-solving dan process improvement',
                    '🎯 FOKUS KARIR MID-LEVEL: Demonstrate mentoring junior team members',
                    '🎯 FOKUS KARIR MID-LEVEL: Emphasize technical expertise dan specializations'
                ],
                'common_mistakes': [
                    '❌ MISTAKE MID-LEVEL: Jangan focus terlalu banyak pada technical details',
                    '❌ MISTAKE MID-LEVEL: Hindari generic achievements tanpa impact metrics',
                    '❌ MISTAKE MID-LEVEL: Jangan underestimate strategic thinking contributions'
                ]
            },
            'senior': {
                'focus_areas': [
                    '🎯 FOKUS KARIR SENIOR: Emphasize leadership dan team management',
                    '🎯 FOKUS KARIR SENIOR: Highlight strategic planning dan business impact',
                    '🎯 FOKUS KARIR SENIOR: Showcase cross-functional collaboration',
                    '🎯 FOKUS KARIR SENIOR: Demonstrate change management capabilities'
                ],
                'common_mistakes': [
                    '❌ MISTAKE SENIOR: Jangan focus terlalu detail pada tactical execution',
                    '❌ MISTAKE SENIOR: Hindari tidak quantified business results',
                    '❌ MISTAKE SENIOR: Jangan forget stakeholder management achievements'
                ]
            }
        }
        
        # Indonesian specific CV improvement advice
        self.indonesian_specific_advice = {
            'formal_language': [
                '🇮🇩 BAHASA FORMAL: Gunakan "Saya" bukan "Gw", "saya" bukan "aq"',
                '🇮🇩 BAHASA FORMAL: Hindari singkatan seperti "tdk", "gk", "bgt"',
                '🇮🇩 BAHASA FORMAL: Gunakan struktur kalimat formal Indonesia',
                '🇮🇩 BAHASA FORMAL: Avoid emoji dalam deskripsi professional'
            ],
            'education_context': [
                '🇮🇩 PENDIDIKAN: Mention IPK jika ≥ 3.5',
                '🇮🇩 PENDIDIKAN: Sertakan institusi terakreditasi BAN-PT',
                '🇮🇩 PENDIDIKAN: Highlight achievements (cum laude, beasiswa, etc)',
                '🇮🇩 PENDIDIKAN: Include relevant coursework untuk posisi target'
            ],
            'experience_context': [
                '🇮🇩 PENGALAMAN: Mention company reputation dan industry position',
                '🇮🇩 PENGALAMAN: Sertakan scale of operations (employee count, revenue)',
                '🇮🇩 PENGALAMAN: Highlight experience dengan multinational companies',
                '🇮🇩 PENGALAMAN: Include experience dengan Indonesian government projects'
            ]
        }
    
    def generate_priority_based_feedback(self, extracted_data, critical_analysis):
        """Generate feedback organized by priority levels"""
        feedback = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
            'strategic': []
        }
        
        # Extract data for analysis
        ats_score = extracted_data.get('ats_score', 0)
        skills_count = len(extracted_data.get('extracted_skills', []))
        contact_info = extracted_data.get('contact_info', {})
        industry_benchmarks = extracted_data.get('industry_benchmarks', {})
        content_score = critical_analysis.get('overall_score', 0)
        
        # CRITICAL PRIORITY
        if ats_score < 50:
            feedback['critical'].append(self._format_feedback_block(
                self.feedback_templates['critical_ats']
            ))
        
        if not contact_info.get('email') or not contact_info.get('phone'):
            feedback['critical'].append(self._format_feedback_block(
                self.feedback_templates['missing_contact']
            ))
        
        if skills_count < 3:
            feedback['critical'].append(self._format_feedback_block(
                self.feedback_templates['low_skills']
            ))
        
        # HIGH PRIORITY
        if 50 <= ats_score < 70:
            feedback['high'].append("🟡 ATS SCORE PERLU PERBAIKAN: CV bisa terdeteksi tapi perlu optimasi keywords dan formatting")
        
        if skills_count < 8:
            feedback['high'].append("🟡 PORTFOLIO SKILLS KURANG: Perluas dengan 8-10 keahlian relevan untuk pasar kerja")
        
        if industry_benchmarks and industry_benchmarks.get('essential_skills_missing', []):
            missing_essential = industry_benchmarks['essential_skills_missing']
            feedback['high'].append(
                f"🟡 KEANEHAN INDUSTRI MISSING: Tambahkan {len(missing_essential)} keahlian inti: {', '.join(missing_essential[:3])}"
            )
        
        # MEDIUM PRIORITY
        if content_score < 60:
            feedback['medium'].append("🟢 KUALITAS KONTEN PERLU PERBAIKAN: Enhance achievement descriptions dengan metrics konkret")
        
        detected_industry = extracted_data.get('detected_industry', 'general')
        if detected_industry != 'general':
            industry_advice = self._get_industry_specific_feedback(detected_industry, 'missing_skills')
            feedback['medium'].extend(industry_advice)
        
        # LOW PRIORITY
        education_level = extracted_data.get('education_level', 'unknown')
        if education_level == 'unknown':
            feedback['low'].append("🔵 PENDIDIKAN TIDAK JELAS: Sertakan informasi pendidikan yang jelas")
        
        experience_level = extracted_data.get('experience_level', 'unknown')
        if experience_level == 'unknown':
            feedback['low'].append("🔵 TINGKAT PENGALAMAN TIDAK JELAS: Clarify experience level dalam CV")
        
        # STRATEGIC PRIORITY
        strategic_advice = self._generate_strategic_advice(extracted_data, critical_analysis)
        feedback['strategic'].extend(strategic_advice)
        
        return feedback
    
    def _get_industry_specific_feedback(self, industry, feedback_type):
        """Get industry-specific feedback"""
        if industry in self.industry_feedback and feedback_type in self.industry_feedback[industry]:
            return self.industry_feedback[industry][feedback_type]
        return []
    
    def _format_feedback_block(self, template):
        """Format feedback template into readable block"""
        formatted = f"**{template['title']}**\n\n"
        formatted += f"{template['content']}\n\n"
        formatted += "**Action Items:**\n"
        for i, action in enumerate(template['actions'], 1):
            formatted += f"{i}. {action}\n"
        return formatted
    
    def _generate_strategic_advice(self, extracted_data, critical_analysis):
        """Generate strategic long-term advice"""
        strategic_advice = []
        
        content_score = critical_analysis.get('overall_score', 0)
        ats_score = extracted_data.get('ats_score', 0)
        experience_level = extracted_data.get('experience_level', 'unknown')
        industry = extracted_data.get('detected_industry', 'general')
        
        # High-quality CV strategy
        if content_score >= 80 and ats_score >= 80:
            strategic_advice.append(
                "🚀 STRATEGIS: CV berkualitas tinggi - fokus pada personal branding dan networking untuk posisi strategis"
            )
            strategic_advice.append(
                "🚀 STRATEGIS: Pertimbangkan consulting atau freelance opportunities untuk maximize earning potential"
            )
        
        # Mid-quality CV strategy
        elif content_score >= 60 and ats_score >= 60:
            strategic_advice.append(
                "📈 STRATEGIS: CV solid foundation - implement continuous improvement untuk competitive advantage"
            )
            strategic_advice.append(
                "📈 STRATEGIS: Focus pada targeted job applications untuk roles yang match current skill level"
            )
        
        # Low-quality CV strategy
        else:
            strategic_advice.append(
                "⚡ STRATEGIS: Prioritaskan fundamental improvements sebelum apply ke posisi senior"
            )
            strategic_advice.append(
                "⚡ STRATEGIS: Consider additional training atau certification untuk strengthen market position"
            )
        
        # Career level specific strategic advice
        if experience_level in self.career_level_advice:
            career_advice = self.career_level_advice[experience_level]['focus_areas']
            strategic_advice.extend(career_advice)
        
        # Industry-specific strategic advice
        if industry != 'general':
            strategic_advice.append(
                f"🏢 INDUSTRI {industry.upper()}: Research salary trends dan growth opportunities di sektor ini"
            )
        
        return strategic_advice
    
    def generate_improvement_timeline(self, extracted_data, critical_analysis):
        """Generate prioritized improvement timeline"""
        timeline = {
            'week_1': [],
            'week_2': [],
            'month_1': [],
            'month_2_3': [],
            'ongoing': []
        }
        
        ats_score = extracted_data.get('ats_score', 0)
        skills_count = len(extracted_data.get('extracted_skills', []))
        contact_info = extracted_data.get('contact_info', {})
        industry_benchmarks = extracted_data.get('industry_benchmarks', {})
        
        # Week 1: Critical fixes
        if ats_score < 70:
            timeline['week_1'].extend([
                "Hari 1-2: Research 20 job descriptions untuk extract keywords",
                "Hari 3-4: Implement ATS optimization (headers, formatting, keywords)",
                "Hari 5-7: Test CV dengan ATS scanners (JobScan, Resume Worded)"
            ])
        
        if not contact_info.get('email') or not contact_info.get('phone'):
            timeline['week_1'].append("Hari 1: Update informasi kontak dengan lengkap")
        
        if skills_count < 5:
            timeline['week_1'].extend([
                "Hari 5-6: Expand skills section dengan minimal 5 keahlian tambahan",
                "Hari 7: Organize skills by categories (Technical, Soft Skills, Tools)"
            ])
        
        # Week 2: Content enhancement
        timeline['week_2'].extend([
            "Hari 8-10: Enhance achievement descriptions dengan quantified results",
            "Hari 11-12: Add specific examples dan project details",
            "Hari 13-14: Polish language dan formatting consistency"
        ])
        
        # Month 1: Strategic improvements
        if industry_benchmarks and industry_benchmarks.get('essential_skills_missing', []):
            missing_skills = industry_benchmarks['essential_skills_missing']
            timeline['month_1'].append(
                f"Minggu 3-4: Develop {len(missing_skills)} missing industry skills through online courses"
            )
        
        timeline['month_1'].extend([
            "Minggu 3: Create portfolio showcase (GitHub, website, atau project samples)",
            "Minggu 4: Network building - connect dengan professionals di target industry"
        ])
        
        # Month 2-3: Advanced optimization
        timeline['month_2_3'].extend([
            "Bulan 2: Industry-specific certifications atau advanced training",
            "Bulan 2: Personal branding - LinkedIn optimization, professional website",
            "Bulan 3: Advanced networking - industry events, conferences, mentorship"
        ])
        
        # Ongoing activities
        timeline['ongoing'].extend([
            "Ongoing: Continuous learning - stay updated dengan industry trends",
            "Ongoing: Regular CV updates - quarterly review dan improvement",
            "Ongoing: Skill development - focus pada emerging technologies atau methods"
        ])
        
        return timeline
    
    def generate_competitive_analysis(self, extracted_data):
        """Generate competitive positioning analysis"""
        analysis = {
            'positioning': '',
            'competitive_advantages': [],
            'improvement_areas': [],
            'market_readiness': ''
        }
        
        ats_score = extracted_data.get('ats_score', 0)
        skills_count = len(extracted_data.get('extracted_skills', []))
        content_score = 70  # Assume moderate content score for now
        industry = extracted_data.get('detected_industry', 'general')
        
        # Positioning analysis
        if ats_score >= 80 and skills_count >= 10:
            analysis['positioning'] = "🟢 STRONG COMPETITOR: CV competitive untuk senior positions"
        elif ats_score >= 60 and skills_count >= 5:
            analysis['positioning'] = "🟡 MODERATE COMPETITOR: CV suitable untuk mid-level positions"
        else:
            analysis['positioning'] = "🔴 NEEDS IMPROVEMENT: Focus pada fundamentals sebelum competitive applications"
        
        # Competitive advantages
        if skills_count >= 10:
            analysis['competitive_advantages'].append(f"Comprehensive skill portfolio ({skills_count} skills)")
        
        if extracted_data.get('experience_level') == 'senior':
            analysis['competitive_advantages'].append("Senior-level experience dan leadership capability")
        
        if extracted_data.get('education_level') in ['master', 'phd']:
            analysis['competitive_advantages'].append("Advanced educational qualifications")
        
        # Improvement areas
        if ats_score < 70:
            analysis['improvement_areas'].append("ATS optimization untuk better visibility")
        
        if skills_count < 8:
            analysis['improvement_areas'].append("Expand technical skill set untuk market relevance")
        
        if industry == 'general':
            analysis['improvement_areas'].append("Industry specialization untuk targeted positioning")
        
        # Market readiness
        if ats_score >= 80 and skills_count >= 8 and content_score >= 70:
            analysis['market_readiness'] = "🟢 HIGH: Ready untuk competitive job market"
        elif ats_score >= 60 and skills_count >= 5:
            analysis['market_readiness'] = "🟡 MODERATE: Suitable untuk standard job applications"
        else:
            analysis['market_readiness'] = "🔴 LOW: Needs significant improvement untuk market competitiveness"
        
        return analysis
    
    def generate_comprehensive_feedback(self, extracted_data, critical_analysis):
        """Generate complete feedback report"""
        # Generate different types of feedback
        priority_feedback = self.generate_priority_based_feedback(extracted_data, critical_analysis)
        improvement_timeline = self.generate_improvement_timeline(extracted_data, critical_analysis)
        competitive_analysis = self.generate_competitive_analysis(extracted_data)
        
        # Compile comprehensive report
        comprehensive_feedback = {
            'priority_based_feedback': priority_feedback,
            'improvement_timeline': improvement_timeline,
            'competitive_analysis': competitive_analysis,
            'indonesian_specific_advice': self._get_indonesian_specific_advice(),
            'generated_timestamp': datetime.now().isoformat(),
            'feedback_version': '2.0-intelligent'
        }
        
        return comprehensive_feedback
    
    def _get_indonesian_specific_advice(self):
        """Get Indonesian-specific career advice"""
        return {
            'formal_language': self.indonesian_specific_advice['formal_language'],
            'education_context': self.indonesian_specific_advice['education_context'],
            'experience_context': self.indonesian_specific_advice['experience_context'],
            'business_culture': [
                '🇮🇩 BUDAYA BISNIS: Shows respect untuk hierarchy dan seniority',
                '🇮🇩 BUDAYA BISNIS: Emphasize teamwork dan collaborative spirit',
                '🇮🇩 BUDAYA BISNIS: Highlight adaptability dan willingness to learn',
                '🇮🇩 BUDAYA BISNIS: Mention experience dengan Indonesian regulatory environment'
            ]
        }
    
    def generate_actionable_recommendations(self, extracted_data, critical_analysis):
        """Generate very specific, actionable recommendations"""
        recommendations = []
        
        # ATS-specific recommendations
        ats_score = extracted_data.get('ats_score', 0)
        if ats_score < 70:
            recommendations.append({
                'category': 'ATS Optimization',
                'priority': 'Critical',
                'action': 'Optimasi ATS Score',
                'specific_steps': [
                    'Tambahkan exact phrases dari 10 job descriptions target',
                    'Gunakan keywords: "project management", "team leadership", "data analysis"',
                    'Hilangkan graphics, tables, dan complex formatting',
                    'Pastikan file dalam format .docx atau .pdf searchable'
                ],
                'timeline': '1-2 minggu',
                'expected_improvement': '+20-30 points ATS score'
            })
        
        # Skills enhancement recommendations
        skills_count = len(extracted_data.get('extracted_skills', []))
        if skills_count < 10:
            recommendations.append({
                'category': 'Skills Portfolio',
                'priority': 'High',
                'action': 'Expand Technical Skills',
                'specific_steps': [
                    'Tambahkan 5-7 skills baru dari job market analysis',
                    'Group skills: "Programming (Python, Java)", "Tools (Excel, SQL)"',
                    'Include proficiency levels: "Advanced", "Intermediate", "Basic"',
                    'Add emerging technologies relevant to industry'
                ],
                'timeline': '2-3 minggu',
                'expected_improvement': 'Better job matching +15-25%'
            })
        
        # Achievement enhancement
        recommendations.append({
            'category': 'Achievement Enhancement',
            'priority': 'High',
            'action': 'Quantify Impact',
            'specific_steps': [
                'Transform "Responsible for" menjadi "Managed 5-person team delivering $2M project"',
                'Add metrics: percentages, dollar amounts, team sizes, timeframes',
                'Use action verbs: "Achieved", "Improved", "Reduced", "Increased"',
                'Include before/after scenarios untuk clarity'
            ],
            'timeline': '1-2 minggu',
            'expected_improvement': '+25-40% content quality score'
        })
        
        # Industry-specific recommendations
        industry = extracted_data.get('detected_industry', 'general')
        if industry in self.industry_feedback:
            recommendations.append({
                'category': 'Industry Specialization',
                'priority': 'Medium',
                'action': f'Optimasi untuk {industry.title()} Industry',
                'specific_steps': self.industry_feedback[industry]['missing_skills'][:3],
                'timeline': '1 bulan',
                'expected_improvement': '+20% industry relevance score'
            })
        
        return recommendations
