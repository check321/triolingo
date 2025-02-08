from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory
)

memory = {}

def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in memory:
        memory[session_id] = InMemoryChatMessageHistory()
    return memory[session_id]