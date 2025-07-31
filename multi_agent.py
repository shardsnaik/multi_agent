from transformers import pipeline
from openai import OpenAI
import base64
from dotenv import load_dotenv
import json
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from utils import AgentState, get_conversation_context, image_to_base64, add_to_memory
load_dotenv()
from Agents.coder_agent import coder_agent
from Agents.search_agent import search_agent
from Agents.text_agent import text_agent
from Agents.image_agent import image_agent
from Agents.router import *
# Global variables
client = OpenAI()
conversation_history = []
MODEL = "gpt-4o"
MAX_TOKENS = 500

# Define the state


# FINAL PROCESSOR
def final_processor(state: AgentState) -> AgentState:
    """Process final response and update memory"""
    # Add to conversation memory
    add_to_memory("user", state["user_input"])
    add_to_memory("assistant", state["response"])
    
    # Add agent info to response
    agent_name = state["agent_choice"].upper()
    state["response"] += f"\n\n[Processed by: {agent_name} AGENT]"
    
    return state

# CREATE WORKFLOW
def create_workflow():
    """Create the LangGraph workflow"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("router", router_agent)
    workflow.add_node("text", text_agent)
    workflow.add_node("coder", coder_agent)
    workflow.add_node("search", search_agent)
    workflow.add_node('image', image_agent)
    workflow.add_node("final", final_processor)
    
    # Set entry point
    workflow.set_entry_point("router")
    
    # Add conditional edges from router
    workflow.add_conditional_edges(
        "router",
        route_to_agent,
        {
            "text": "text",
            "coder": "coder", 
            "search": "search",
            "image": "image"
        }
    )
    
    # All agents go to final processor
    workflow.add_edge("text", "final")
    workflow.add_edge("coder", "final")
    workflow.add_edge("search", "final")
    workflow.add_edge("image", "final")
    
    # Final processor ends workflow
    workflow.add_edge("final", END)
    
    return workflow.compile()

# Initialize the workflow
app = create_workflow()

# MAIN FUNCTIONS
def run_agent(text_input: str = None, image_src: str = None) -> str:
    """Main function to run the multi-agent system"""
    if not text_input:
        return "Please provide text input."
    
    # Create initial state
    initial_state = {
        "user_input": text_input,
        "image_path": image_src,
        "agent_choice": "",
        "response": "",
        "messages": []
    }
    
    try:
        # Run the workflow
        result = app.invoke(initial_state)
        conversation_history.append({
            "user_input": text_input,
            "response": result["response"]
        })
        return result["response"]
    except Exception as e:
        return f"System error: {str(e)}"

def clear_memory():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return "Memory cleared!"

def save_conversation(filename: str = "conversation.json"):
    """Save conversation to file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(conversation_history, f, indent=2, ensure_ascii=False)
        return f"Conversation saved to {filename}"
    except Exception as e:
        return f"Error saving: {str(e)}"

def load_conversation(filename: str = "conversation.json"):
    """Load conversation from file"""
    global conversation_history
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            conversation_history = json.load(f)
        return f"Conversation loaded from {filename}"
    except Exception as e:
        return f"Error loading: {str(e)}"

def show_history():
    """Show conversation history summary"""
    return f"Conversation has {len(conversation_history)} messages"

# EXAMPLE USAGE
if __name__ == "__main__":
    print("🤖 Multi-Agent Chatbot System Initialized!")
    print("=" * 60)
    print('\nGive Text Input or Image or both but while giving image input mention image:"Your Image"\nYou:')
    print("🧠 Available Agents:")
    print("   📝 TEXT AGENT    - General conversations & image analysis")
    print("   💻 CODER AGENT   - Programming & code generation") 
    print("   🔍 SEARCH AGENT  - Information retrieval & research")
    print("   🔍 IMAGE AGENT  - Analysis the image ")
    print("Commands: 'clear', 'save', 'load', 'history', 'quit'")
    print("-" * 60)
    
    while True:
        user_input = input("\n You: ").strip()
        
        if user_input.lower() == 'quit':
            print(" Goodbye!")
            break
        elif user_input.lower() == 'clear':
            print(clear_memory())
            continue
        elif user_input.lower() == 'save':
            print(save_conversation())
            continue
        elif user_input.lower() == 'load':
            print(load_conversation())
            continue
        elif user_input.lower() == 'history':
            print(show_history())
            continue
        
        # Handle image input
        image_path = None
        if 'image:' in user_input.lower():
            parts = user_input.split('"')[1]
            print(parts)
            response = run_agent(text_input=user_input, image_src=parts)
            print(f"\n Assistant: {response}")
            # conversation_history.append()
            
        
        # Get response
        else:
            print(" Processing...")
            response = run_agent(text_input=user_input, image_src=image_path)
            print(f"\n Assistant: {response}")
            
            # Show status
            print(f"[Messages in memory: {len(conversation_history)}]")
