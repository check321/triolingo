import gradio as gr

from agents.conversation_agent import ConversationAgent
from agents.house_agent import HouseAgent
from utils.logger import LOG

conversation_agent = ConversationAgent()
house_agent = HouseAgent()

def handle_conversation(user_input, chat_history):
    LOG.debug(f"[Histories]: {chat_history}")
    bot_message = conversation_agent.chat_with_history(user_input)
    LOG.info(f"[Bot]: {bot_message}")
    return bot_message

def get_scenario_intro(scenario):
    with open(f"content/{scenario}_page.md","r") as f:
        scenario_intro = f.read().strip()
    return scenario_intro

def handle_scenario(user_input,chat_history,scenario):
    agents = {
        "house_renting": house_agent,
    }
    bot_message = agents[scenario].chat_with_history(user_input)
    return bot_message

with gr.Blocks(title="TrioLingo") as triolingo_app:
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
    
    with gr.Tab("Scenario Dialog"):
        gr.Markdown("## Select Scenario")
        
        scenario = gr.Radio(
            choices = [
                ("House Renting", "house_renting"),
            ],
            label="Scenario",
        )
        
        scenario_intro = gr.Markdown()
        
        scenario.change(fn=get_scenario_intro,inputs=scenario,outputs=scenario_intro)
        
        scenario_chatbot = gr.Chatbot(
            placeholder="Select a scenario and let's start!",
            height=600,
        )
        
        gr.ChatInterface(
            chatbot=scenario_chatbot,
            additional_inputs=scenario,
            submit_btn="Send",
            clear_btn="Clear",
            retry_btn=None,
            undo_btn=None,
            fn=handle_scenario
        )       
        
if __name__ == "__main__":
    triolingo_app.launch(share=False,server_name="0.0.0.0",server_port=9090)