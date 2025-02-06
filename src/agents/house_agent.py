from .base_senario_agent import ScennarioAgent
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory
)
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage

memory = {}

def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in memory:
        memory[session_id] = InMemoryChatMessageHistory()
    return memory[session_id]

class HouseAgent(ScennarioAgent):
    def __init__(self):
        super().__init__()
        self.name = "HouseAgent"
        
        with open("prompts/house_agent_prompt.txt", "r", encoding="utf-8") as f:
            self.system_prompt = f.read().strip()
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        self.chatbot = self.prompt | ChatOpenAI(
            model="gpt-4o",
            base_url = self.get_base_url(),
            api_key=self.get_api_key(),
            temperature=0.7,
            max_tokens=8192,
        )
        
        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot,get_session_history=get_session_history)
        
        self.config = {"configurable": {"session_id": "xyz123"}}
    
    def chat_with_history(self,user_input):
        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],
            self.config,
        )
        return response.content