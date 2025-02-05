from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory
)
from langchain_openai import ChatOpenAI
from utils.logger import LOG
from dotenv import load_dotenv
import os

memory = {}

def get_chat_session(session_id: str) -> BaseChatMessageHistory:
    if session_id not in memory:
        memory[session_id] = InMemoryChatMessageHistory()
    return memory[session_id]

class ConversationAgent:
    def __init__(self):
        load_dotenv(override=True)
        self.name = "ConversationAgent"
        with open("prompts/conversation_propmt.txt", "r", encoding="utf-8") as f:
            self.system_prompt = f.read().strip()

        # 加载提示词
        self.propmt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        # 初始化聊天Bot
        self.chatbot = self.propmt | ChatOpenAI(
            model=os.getenv("OPENAI_MODEL"),
            base_url=os.getenv("OPENAI_API_BASE"),
            max_tokens=8192,
            temperature=0.7,
        )

        # 记忆能力
        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot,get_session_history=get_chat_session)
        self.config = {"configurable": {"session_id": "xyz123"}}
    
    # def chat(self,user_input):
    #     resp = self.chatbot.invoke(
    #         [HumanMessage(content=user_input)],
    #     )
        
    #     return resp.content
    
    def chat_with_history(self,user_input):
        resp = self.chatbot_with_history.invoke(
            HumanMessage(content=user_input),
            config=self.config,
        )
        LOG.debug(resp)
        return resp.content