from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'FA6lzrvg8RlJ8Ez3')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://admin:FA6lzrvg8RlJ8Ez3@mongo1.feazht7.mongodb.net/')