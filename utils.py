import operator, base64
from typing import Dict, List, Any, Optional, TypedDict
from typing_extensions import Annotated

conversation_history =[]
class AgentState(TypedDict):
    user_input: str
    image_path: Optional[str]
    agent_choice: str
    response: str
    messages: Annotated[List[str], operator.add]

def image_to_base64(image_path: str) -> str:
    """Convert image to base64"""
    with open(image_path, 'rb') as img:
        img_bytes = img.read()
        decoded_img = base64.b64encode(img_bytes).decode('utf-8')
        return decoded_img

def add_to_memory(role: str, content: str):
    """Add message to conversation history"""
    global conversation_history
    conversation_history.append({"role": role, "content": content})
    
    # Keep only last 20 messages
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

def get_conversation_context() -> List[Dict]:
    """Get recent conversation for context"""
    return conversation_history[-5:] if conversation_history else []
