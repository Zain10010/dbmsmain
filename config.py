from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    # Using PyMySQL as the database driver
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:2006@127.0.0.1/alumni_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 