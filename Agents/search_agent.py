from openai import OpenAI
client = OpenAI()
from utils import AgentState, get_conversation_context
# SEARCH AGENT
def search_agent(state: AgentState) -> AgentState:
    """Handle search and information retrieval tasks"""
    try:
        # Enhanced system prompt for search/info tasks
        system_prompt = """You are an information specialist. Provide:
        1. Accurate, factual information
        2. Well-structured responses
        3. Clear sources when possible
        4. Up-to-date information from your training
        If you don't have current information, clearly state limitations."""
        
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
        state["messages"] = [f"[SEARCH AGENT] Retrieved information"]
        
    except Exception as e:
        state["response"] = f"Search agent error: {str(e)}"
        state["messages"] = [f"[SEARCH AGENT] Error occurred"]
    
    return state
