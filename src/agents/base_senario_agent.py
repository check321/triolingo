from dotenv import load_dotenv
import os

class ScennarioAgent:
    def __init__(self):
        self.name = "ScenarioAgent"
        load_dotenv(override=True)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_API_BASE")
        
    def respond(self,user_input):
        raise NotImplementedError("SubAgent should implement this method.")
    
    def get_api_key(self):
        return self.api_key
    
    def get_base_url(self):
        return self.base_url