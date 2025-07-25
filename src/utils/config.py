import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:

    # Get the Google API Key and Langchain_API_KEY
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    LANGSMITH_API_KEY= os.getenv("LANGCHAIN_API_KEY")

config= Config()