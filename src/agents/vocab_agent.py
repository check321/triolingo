from .agent_base import AgentBase
from .session_history import get_session_history

class VocabAgent(AgentBase):
    
    def __init__(self,session_id=None):
        super().__init__(
            name="vocab_study",
            prompt_file = "prompts/vocab_study_prompt.txt",
            session_id=session_id
        )
    
    def restart_session(self,session_id=None):
        if session_id is None:
            session_id = self.session_id
        
        history = get_session_history(session_id)
        history.clear()
        
        return history
       