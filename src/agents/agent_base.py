from abc import ABC
import json
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai import ChatOpenAI
from .session_history import get_session_history
from dotenv import load_dotenv
import os

class AgentBase(ABC):
    
    def __init__(self,name,prompt_file,intro_file=None,session_id=None):
        
        load_dotenv(override=True)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_API_BASE")
        self.model = os.getenv("OPENAI_MODEL")
        
        self.name = name
        self.prompt_file = prompt_file
        self.intro_file = intro_file
        self.session_id = session_id if session_id else self.name
        self.prompt = self.load_prompt()
        self.intro_messages = self.load_intro() if self.intro_file else []
        self.chatbot = self.create_chat_bot()
    
    def load_prompt(self):
        try:
            with open(self.prompt_file,"r",encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file {self.prompt_file} not found.")
            
    def load_intro(self):
        try:
            with open(self.intro_file,"r",encoding="utf-8") as f:
                return json.load(f) 
        except FileNotFoundError:
            raise FileNotFoundError(f"Intro file {self.intro_file} not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in {self.intro_file}.")
        
    def create_chat_bot(self):
        system_prompt = ChatPromptTemplate.from_messages([
            ("system",self.prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])
              
        self.chatbot = system_prompt | ChatOpenAI(
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            model=self.model,
            temperature=0.8,
            max_tokens=8192
        )
        
        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot,get_session_history)
    
    def chat_with_history(self,user_input,session_id: str = None):
        if session_id is None:
            session_id = self.name
        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],
            {"configurable":{"session_id":session_id}}
        )
        
        return response.content