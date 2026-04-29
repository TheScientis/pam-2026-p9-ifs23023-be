import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'motivation-app-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///motivation.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-2.5-flash')
    APP_PORT = int(os.getenv('APP_PORT', 5000))
