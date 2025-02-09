import gradio as gr
from agents.vocab_agent import VocabAgent

vocab_agent = VocabAgent()

feature = "vocab_study"

def get_page_desc(feature):
    try:
        with open(f"content/page/{feature}.md","r",encoding="utf-8") as f:
            scenario_intro = f.read().strip()
        return scenario_intro
    except FileNotFoundError:
        return "Scenario intro is not found."
    
def handle_vocab(user_input,chat_history):
    bot_message = vocab_agent.chat_with_history(user_input)
    return bot_message

def restart_vocab_study_chatbot():
    vocab_agent.restart_session()
    
    _next_round_greeting = "Let's begin!"
    bot_message = vocab_agent.chat_with_history(_next_round_greeting)
    
    return gr.Chatbot(
        value=[(_next_round_greeting,bot_message)],
        height=800,
    )    
    

def create_vocab_tab():
    with gr.Tab("Vocabulary"):
        gr.Markdown("## Vocabulary Challenge")
        gr.Markdown(get_page_desc(feature))
        
        vocab_study_chatbot = gr.Chatbot(
            placeholder="Let's learn vocabulary!",
            height=800,
        )
        
        restart_btn = gr.Button(value="Next Stage")
        restart_btn.click(
            fn=restart_vocab_study_chatbot,
            inputs=None,
            outputs=vocab_study_chatbot,
        )
        
        gr.ChatInterface(
            fn=handle_vocab,
            chatbot=vocab_study_chatbot,
            retry_btn=None,
            undo_btn=None,
            clear_btn=None,
            submit_btn="Send"
        )