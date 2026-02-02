import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration for the CRE Parsing application"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '4096'))
    
    # Parsing Configuration
    USE_OPENAI_EXTRACTION = os.getenv('USE_OPENAI_EXTRACTION', 'true').lower() == 'true'
    ENABLE_FALLBACK = os.getenv('ENABLE_FALLBACK', 'true').lower() == 'true'
    
    # Flask Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    
    @classmethod
    def validate_openai_config(cls) -> bool:
        """Validate that OpenAI is properly configured"""
        return bool(cls.OPENAI_API_KEY)
