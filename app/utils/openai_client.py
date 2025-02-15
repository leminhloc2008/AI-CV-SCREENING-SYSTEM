from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAIClientManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClientManager, cls).__new__(cls)
            cls._instance.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        return cls._instance
    
    def get_client(self):
        return self.client

# Singleton instance
openai_client = OpenAIClientManager() 