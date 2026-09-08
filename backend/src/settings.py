import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv('APP_NAME', 'StudyBot API')
    environment: str = os.getenv('ENVIRONMENT', 'development')
    database_url: str = os.getenv('DATABASE_URL', '')
    session_cookie_name: str = os.getenv('SESSION_COOKIE_NAME', 'studybot_session')
    session_expire_hours: int = int(os.getenv('SESSION_EXPIRE_HOURS', '24'))
    frontend_url: str = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    tamil_email: str = os.getenv('TAMIL_EMAIL', 'tamil@example.com')
    tamil_password: str = os.getenv('TAMIL_PASSWORD', '')
    nvidia_api_key: str = os.getenv('NVIDIA_API_KEY', '')
    @property
    def secure_cookies(self) -> bool: return self.environment.lower() == 'production'

settings = Settings()
