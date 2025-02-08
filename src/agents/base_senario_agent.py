from dotenv import load_dotenv
import json
import os
import random
from .session_history import get_session_history
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai import ChatOpenAI

class ScennarioAgent:
    def __init__(self,scenario_name):
        self.name = scenario_name
        load_dotenv(override=True)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_API_BASE")
        self.model = os.getenv("OPENAI_MODEL")
        self.prompt_file = f"prompts/{self.name}_prompt.txt"
        self.intro_file = f"content/intro/{self.name}.json"
        self.intro_messages = self.load_intro()
        self.prompt = self.load_prompt()
        self.create_chat_bot()
        
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
    
    def start_new_session(self,session_id: str | None = None):
        if session_id is None:
            session_id = self.name
        
        history = get_session_history(session_id)
        
        if not history.messages:
            initial_ai_message = random.choice(self.intro_messages)
            history.add_message(AIMessage(content=initial_ai_message))
            return initial_ai_message
        else:
            # 默认最近一条信息
            return history.messages[-1].content
    
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
            
    def get_api_key(self):
        return self.api_key
    
    def get_base_url(self):
        return self.base_url