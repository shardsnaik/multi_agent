from openai import OpenAI
from utils import AgentState,get_conversation_context, image_to_base64
client = OpenAI()
# TEXT AGENT
def text_agent(state: AgentState) -> AgentState:
    """Handle general text conversations"""
    try:
        # Prepare messages with context
        messages = []
        
        # Add conversation context
        for msg in get_conversation_context():
            messages.append(msg)
        
        # Add current user input
        content = []
        content.append({'type': 'text', 'text': state["user_input"]})
        
        # Add image if present
        if state.get("image_path"):
            decoded_image = image_to_base64(state["image_path"])
            content.append({
                'type': 'image_url',
                'image_url': {"url": f"data:image/jpeg;base64,{decoded_image}"}
            })
        
        messages.append({"role": "user", "content": content})
        
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=messages,
            max_tokens=500
        )
        
        state["response"] = response.choices[0].message.content
        state["messages"] = [f"[TEXT AGENT] Processed general conversation"]
        
    except Exception as e:
        state["response"] = f"Text agent error: {str(e)}"
        state["messages"] = [f"[TEXT AGENT] Error occurred"]
    
    return state
