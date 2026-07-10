import os
import sys
from pathlib import Path
from dotenv import load_dotenv, find_dotenv


def _load_environment():
    bundled_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    exe_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else bundled_dir
    env_path = exe_dir / ".env"

    if env_path.exists():
        load_dotenv(env_path)
        return

    discovered = find_dotenv()
    if discovered:
        load_dotenv(discovered)


_load_environment()


class Config:
    # Read API keys from environment variables
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
