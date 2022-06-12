from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
MONGODB_URI=os.environ.get('MONGODB_URI')