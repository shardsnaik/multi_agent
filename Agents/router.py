from utils import *
# ROUTER AGENT
def router_agent(state: AgentState) -> AgentState:
    """Route to appropriate agent based on user input"""
    user_input = state["user_input"].lower()
    
    # Simple keyword-based routing
    if any(word in user_input for word in ["code", "program", "function", "script", "debug", "python", "javascript", "html", "css"]):
        state["agent_choice"] = "coder"
    elif any(word in user_input for word in ["search", "find", "what is", "who is", "when", "where", "current", "news", "latest"]):
        state["agent_choice"] = "search"
    elif any(word in user_input for word in ["image", "IMAGE", "imges  ", "IMG", "imagess", "Img", "Images", "iMAGES", "img"]):
        state["agent_choice"] = "image"
    else:
        state["agent_choice"] = "text"
    
    return state

def route_to_agent(state: AgentState) -> str:
    """Return the chosen agent"""
    return state["agent_choice"]
