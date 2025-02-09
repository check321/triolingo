import random
from .agent_base import AgentBase
from .session_history import get_session_history
from langchain_core.messages import AIMessage


class ScennarioAgent(AgentBase):
    def __init__(self,scenario_name,session_id: str | None = None):
        prompt_file = f"prompts/{scenario_name}_prompt.txt"
        intro_file = f"content/intro/{scenario_name}.json"
        super().__init__(
            name = scenario_name,
            prompt_file=prompt_file,
            intro_file=intro_file,
            session_id=session_id
        )

    def start_new_session(self,session_id: str | None = None):
        if session_id is None:
            session_id = self.name
        
        history = get_session_history(session_id)
        
        if not history.messages:
            initial_ai_message = random.choice(self.intro_messages)
            history.add_message(AIMessage(content=initial_ai_message))
            return initial_ai_message
        else:
            # 默认最近一条信息
            return history.messages[-1].content