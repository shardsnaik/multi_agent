from utils import *
from openai import OpenAI
client = OpenAI()
def image_agent(state: AgentState) -> AgentState:
        """Agent specialized in image analysis"""
        try:
            content = []
            
            # Add text input
            if state["user_input"]:
                content.append({'type': 'text', 'text': state["user_input"]})
            
            # Add image if present
            if state.get("image_path"):
                decoded_image = image_to_base64(state["image_path"])
                content.append({
                    'type': 'image_url',
                    'image_url': {
                        "url": f"data:image/jpeg;base64,{decoded_image}"
                    }
                })
            
            # Prepare messages with conversation history
            messages = []
           
            messages.append({"role": "user", "content": content})
            
            response = client.chat.completions.create(
                model= 'gpt-4o',
                messages=messages,
                max_tokens=500
            )
            
            state["response"] = response.choices[0].message.content
            state["messages"] = [f"[IMAGE AGENT] Processed general conversation"]

        except Exception as e:
            state["response"] = f"Image agent error: {str(e)}"
        
        return state