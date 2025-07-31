# Multi-Agent Chatbot with LangGraph

A sophisticated conversational AI system that uses **3 specialized agents** to provide expert responses across different domains. Built with **LangGraph** and **OpenAI GPT-4**.

##  **Overview**

Instead of using a single general-purpose chatbot, this system employs **intelligent routing** to automatically select the most appropriate specialist agent for each user query:

- **TEXT AGENT**  - General conversations, Q&A, image analysis
- **CODER AGENT**  - Programming, debugging, code generation  
- **SEARCH AGENT**  - Information retrieval, factual queries
- **IMAGE AGENT**  - Information retrieval, factual queries

## 🏗️ **Architecture**

```
User Input → Router Agent → Specialized Agent → Final Response
                ↓
    ┌─────────────────────────────┐
    │   Router Agent              │
    │  (Keyword-based routing)    │
    └─────────────────────────────┘
                ↓
    ┌─────────┬──────────┬──────────┬──────────┐
    │ TEXT    │ CODER    │ SEARCH   │ IMAGE    │
    │ AGENT   │ AGENT    │ AGENT    │  AGENT   │
    └─────────┴──────────┴──────────┴──────────┘
                ↓
    ┌─────────────────────────────┐
    │   Final Processor           │
    │  (Memory + Response)        │
    └─────────────────────────────┘
```

## **Quick Start**

### **1. Installation**
```bash
pip install langgraph langchain-openai openai python-dotenv transformers
```

### **2. Environment Setup**
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### **3. Run the Chatbot**
```python
python chatbot.py
```

### **4. Basic Usage**
```python
# Direct API calls
from chatbot import chat, chat_with_image, reset_chat

# Text chat
response = chat("Write a Python function to sort numbers")  # → CODER AGENT
response = chat("What is quantum computing?")              # → SEARCH AGENT
response = chat("Hello, how are you?")                     # → TEXT AGENT
response = chat("Hello, what is in this image")                                                    # → Image AGENT

# Image analysis
response = chat_with_image("What's in this image?", "photo.jpg")

# Reset conversation
reset_chat()
```

## 🎮 **Interactive Commands**

| Command | Description |
|---------|-------------|
| `quit` | Exit the chatbot |
| `clear` | Clear conversation memory |
| `save` | Save conversation to file |
| `load` | Load previous conversation |
| `history` | Show message count |
| `image: path/to/image.jpg` | Include image in conversation |

## 🧠 **Agent Routing Logic**

The router automatically selects agents based on keywords:

```python
# CODER AGENT triggers
"code", "program", "function", "script", "debug", "python", "javascript", "html"

# SEARCH AGENT triggers  
"search", "find", "what is", "who is", "when", "where", "current", "news"

# TEXT AGENT (default)
Everything else, including general conversation and image analysis
```

##  **Features**

###  **Core Features**
- **Intelligent Routing** - Automatic agent selection
- **Conversation Memory** - Maintains context across sessions
- **Multi-modal Support** - Text and image processing
- **Error Handling** - Graceful fallbacks and recovery
- **Persistent Storage** - Save/load conversation history

###  **Agent Specializations**
- **TEXT AGENT**: General chat, explanations, image analysis
- **CODER AGENT**: Code generation, debugging, best practices
- **SEARCH AGENT**: Information retrieval, factual queries
- **IMAGE AGENT**: Analysis image and get information
<!-- 
## 🔧 **Configuration**

### **Global Settings**
```python
MODEL = "gpt-4o"          # OpenAI model
MAX_TOKENS = 500          # Response length limit
MAX_HISTORY = 20          # Conversation memory limit
```

### **Customization**
```python
# Add new routing keywords
def router_agent(state):
    if "new_keyword" in user_input:
        state["agent_choice"] = "new_agent"
    
# Create new specialized agent
def new_agent(state):
    # Your specialized logic here
    return state
``` -->

##  **Example Interactions**

### **Programming Help**
```
You: "Write a function to calculate factorial"
 [CODER AGENT] Here's a Python function with error handling:

def factorial(n):
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
```

### **Information Query**
```
You: "What is artificial intelligence?"
 [SEARCH AGENT] Artificial intelligence (AI) refers to the simulation 
of human intelligence in machines...
```

### **General Conversation**
```
You: "How was your day?"
 [TEXT AGENT] I appreciate you asking! As an AI, I don't experience 
days in the traditional sense, but I'm here and ready to help...
```

<!-- ## 🚀 **Advanced Usage**

### **API Integration**
```python
# Simple chat function
def simple_chat():
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = chat(user_input)
        print(f"Bot: {response}")

# Batch processing
def process_queries(queries):
    results = []
    for query in queries:
        response = chat(query)
        results.append({"query": query, "response": response})
    return results
```

### **Memory Management**
```python
# Check conversation length
print(f"Messages: {len(conversation_history)}")

# Clear specific conversation parts
conversation_history = conversation_history[-10:]  # Keep last 10

# Export conversation
import json
with open('chat_export.json', 'w') as f:
    json.dump(conversation_history, f, indent=2)
``` -->

<!-- ## 🛠️ **Development**

### **Project Structure**
```
chatbot/
├── chatbot.py          # Main application
├── .env               # Environment variables
├── README.md          # This file
├── conversation.json  # Saved conversations
└── requirements.txt   # Dependencies
``` -->

### **Dependencies**
```txt
langgraph>=0.0.20
langchain-openai>=0.0.5
openai>=1.0.0
python-dotenv>=1.0.0
transformers>=4.30.0
typing-extensions>=4.5.0
```


##  **Troubleshooting**

### **Common Issues**
1. **"OpenAI API Error"** - Check your API key in `.env`
2. **"Module not found"** - Run `pip install -r requirements.txt`
3. **"Image processing error"** - Verify image file path and format
4. **"Memory issues"** - Use `clear` command to reset conversation


## 🔗 **Related Projects**

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [LangChain Framework](https://python.langchain.com/)

---

**Built with ❤️ using LangGraph and OpenAI GPT-4**