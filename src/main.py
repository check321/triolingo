from tabs.conversation_tab import create_conversation_tab
from tabs.scenario_tab import create_scenario_tab
from tabs.vocab_tab import create_vocab_tab
import gradio as gr

def main():
    with gr.Blocks(title="TrioLingo") as triolingo_app:   
        create_conversation_tab()
        create_scenario_tab()
        create_vocab_tab()
        
    triolingo_app.launch(share=False,server_name="0.0.0.0",server_port=9090)
        
if __name__ == "__main__":
    main()