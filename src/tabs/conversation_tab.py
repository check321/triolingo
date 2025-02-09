from utils.logger import LOG
from agents.conversation_agent import ConversationAgent
import gradio as gr

conversation_agent = ConversationAgent()

def handle_conversation(user_input, chat_history):
    LOG.debug(f"[Histories]: {chat_history}")
    bot_message = conversation_agent.chat_with_history(user_input)
    LOG.info(f"[Bot]: {bot_message}")
    return bot_message

def create_conversation_tab():
    with gr.Tab("Dialog Practice"):
        gr.Markdown("## Chat with TrioLingo")
        conversation_chatbot = gr.Chatbot(
            placeholder="How's going today?",
            height=800
        )
        
        gr.ChatInterface(
            chatbot=conversation_chatbot,
            submit_btn="Send",
            clear_btn="Clear",
            retry_btn=None,
            undo_btn=None,
            fn=handle_conversation
        )