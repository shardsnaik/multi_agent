from openai import OpenAI
from utils import *
client = OpenAI()
# CODER AGENT
def coder_agent(state: AgentState) -> AgentState:
    """Handle coding and programming tasks"""
    try:
        # Enhanced system prompt for coding
        system_prompt = """You are a specialized coding assistant. Provide:
        1. Clean, well-commented code
        2. Clear explanations
        3. Best practices and error handling
        4. Examples when helpful
        Focus on practical, working solutions."""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation context
        for msg in get_conversation_context():
            if msg["role"] != "system":
                messages.append(msg)
        
        # Add current request
        messages.append({"role": "user", "content": state["user_input"]})
        
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=messages,
            max_tokens=500
        )
        
        state["response"] = response.choices[0].message.content
        state["messages"] = [f"[CODER AGENT] Generated code solution"]
        
    except Exception as e:
        state["response"] = f"Coder agent error: {str(e)}"
        state["messages"] = [f"[CODER AGENT] Error occurred"]
    
    return state
