import gradio as gr

from agents.conversation_agent import ConversationAgent
from agents.base_senario_agent import ScennarioAgent
from utils.logger import LOG

conversation_agent = ConversationAgent()
# house_agent = HouseAgent()

agents = {
    "house_renting": ScennarioAgent("house_renting"),
}

def handle_conversation(user_input, chat_history):
    LOG.debug(f"[Histories]: {chat_history}")
    bot_message = conversation_agent.chat_with_history(user_input)
    LOG.info(f"[Bot]: {bot_message}")
    return bot_message

def get_scenario_intro(scenario):
    with open(f"content/page/{scenario}_page.md","r") as f:
        scenario_intro = f.read().strip()
    return scenario_intro

def start_new_senario(scenario):
    init_ai_message = agents[scenario].start_new_session(session_id=None)
    
    return gr.Chatbot(
        value=[(None,init_ai_message)]
        ,height=600
    )

def handle_scenario(user_input,chat_history,scenario):
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
        scenario_chatbot = gr.Chatbot(
            placeholder="Select a scenario and let's start!",
            height=600,
        )
        
        scenario.change(
            fn=lambda s: (get_scenario_intro(s),start_new_senario(s)),inputs=scenario,outputs=[scenario_intro,scenario_chatbot])
        
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