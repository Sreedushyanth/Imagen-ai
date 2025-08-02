import os
from pathlib import Path
from typing import Optional

class Settings:
    """Secure configuration management for StoryMaker"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.load_environment()
    
    def load_environment(self):
        """Load environment variables"""
        # Try to load from .env file first
        env_file = self.base_dir / ".env"
        if env_file.exists():
            self.load_env_file(env_file)
    
    def load_env_file(self, env_file: Path):
        """Load environment variables from .env file"""
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}")
    
    @property
    def fal_api_key(self) -> Optional[str]:
        """Get Fal API key from environment"""
        return os.getenv("FAL_API_KEY")
    
    @property
    def app_secret_key(self) -> str:
        """Get app secret key"""
        return os.getenv("APP_SECRET_KEY", "your-secret-key-here")
    
    @property
    def debug_mode(self) -> bool:
        """Get debug mode setting"""
        return os.getenv("DEBUG", "False").lower() == "true"
    
    @property
    def max_file_size(self) -> int:
        """Maximum file upload size in bytes"""
        return int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB default
    
    @property
    def generation_timeout(self) -> int:
        """Generation timeout in seconds"""
        return int(os.getenv("GENERATION_TIMEOUT", "300"))  # 5 minutes default

# Global settings instance
settings = Settings()
