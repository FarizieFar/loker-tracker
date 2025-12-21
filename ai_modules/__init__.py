"""
AI Modules Package
Provides AI-powered features for the job tracker application
"""

# Import all AI modules for easy access
from .nlp_processor import NLPProcessor
from .cv_analyzer import CVAnalyzer
from .job_matcher import JobMatcher
from .insights_generator import InsightsGenerator
from .ai_service import AIService

__version__ = "1.0.0"
__all__ = [
    'NLPProcessor',
    'CVAnalyzer', 
    'JobMatcher',
    'InsightsGenerator',
    'AIService'
]
