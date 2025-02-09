from agents.senario_agent import ScennarioAgent
import gradio as gr

agents = {
    "house_renting": ScennarioAgent("house_renting"),
}

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

def create_scenario_tab():
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