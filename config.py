import os
from dataclasses import dataclass

@dataclass
class Config:
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    GITHUB_TOKEN: str = os.getenv('GITHUB_TOKEN', '')
    DEFAULT_REPO: str = ''
    APP_NAME: str = "Gemini Coding Manager"
    VERSION: str = "1.0.0"
    SUPPORTED_LANGUAGES: list = None
    
    def __post_init__(self):
        self.SUPPORTED_LANGUAGES = [
            'python', 'javascript', 'java', 'cpp', 'c#', 'ruby', 
            'go', 'rust', 'php', 'swift', 'kotlin', 'typescript'
        ]

config = Config()
