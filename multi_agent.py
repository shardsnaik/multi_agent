from transformers import pipeline
from openai import OpenAI
import base64, os
from dotenv import load_dotenv
os.environ['TF_ENABLE_ONEDNN_OPTS'] ='0'
load_dotenv()
client = OpenAI()

class Multiagent:
        def image_to_base64(self, image_path:str)-> str:
            '''
            Function to decode the image
                Args: 
                    image_path (str): Path to the image file
                Returns:
                    str: Base64 encoded image
            '''
            with open(image_path, 'rb') as img:
                image_bytes = img.read()
                decoded_imge = base64.b64encode(image_bytes).decode('utf-8')
                # return base64.b64encode(img.read()).decode('utf-8')
                return decoded_imge

        def run_agent(self, image_src: str = None, text_input: str= None)-> str:
            '''
            Input: 
            The fucntion that takes image and text as input 
            Return:
                Model Generated Text
            '''
            content = []
            if not text_input and not image_src:
                 return 'Please proivde either text input or image input'
            if text_input:
                content.append({'type':'text', 'text': text_input})
            if image_src:
                try:
                     decoded_image = self.image_to_base64(image_path=image_src)
                     content.append({
                    'type': 'image_url',
                    'image_url':{
                        "url": f"data:image/jpeg;base64,{decoded_image}"
        
                    }
                })
                except Exception as e:
                     return f'Error processing image: {str(e)}'
            # Adding user messages to memory 
            self.add_to_memory('user', content)
            
            response= client.chat.completions.create(
                model = "gpt-4.1",
                messages=[
                    {"role": "user", "content": content}
                ],
                max_tokens=300
            )
            assistant_response = response.choices[0].message.content
            self.add_to_memory('assitant', assistant_response)
            
            return assistant_response
        
        def add_to_memory(self, role:str, content):
             ''''
             add message to conversation memory

             Args:
                role(str): 'user' or 'assistant'
                content: Generated messages or user input (query)
             '''
             self.conversation_history = []
             self.max_history = 50
             messages = {'role': role, 'content': content}
             self.conversation_history.append(messages)
             
             if len(self.conversation_history)> self.max_history:
                  if self.conversation_history[0].get('role') == 'system':
                       self.conversation_history = [self.conversation_history[0] ] + self.conversation_history[-(self.max_history-1):]
                  else:
                       self.conversation_history = self.conversation_history[-self.max_history:]
        def set_system_message(self, system_messages:str):
             """
        Set or update the system message
        
        Args:
            system_message (str): System prompt to guide the assistant's behavior
        """
             if self.conversation_history and self.conversation_history[0].get("role") == "system":
                  self.conversation_history.pop(0)
        
        # Add new system message at the beginning
             self.conversation_history.insert(0, {"role": "system", "content": system_messages})

        def get_conversation_history(self):
             '''
             Get the current conversation history

             Returns: 
                 list: List of conversation messages
             '''
             return self.conversation_history
        def clear_history(self):
             '''
             Clearing the conversation history 
             '''
             system_msg = None
             if self.conversation_history and self.conversation_history[0].get('role') == 'system':
                  system_msg = self.conversation_history[0]
             self.conversation_history = []

             if system_msg:
                  self.conversation_history.append(system_msg)

        def save_conversation(self, filename: str):
             ''' 
             Function which saves the conversation history
             
             Args:
                  filename (str): Path to save the conversation
            '''
             import json, datetime
             chat_name = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
             with open(chat_name, 'w', encoding='utf-8') as f:
                  json.dump(self.conversation_history, f, indent=2)
                  print(f'Conversation History saved to file: {chat_name}')             
                  
    
if __name__ == '__main__':
     agent = Multiagent()
while True:
    user_input = input('\nGive Text Input or Image or both but while giving image input mention image:"Your Image"\nYou:').strip()
    image_path = None
    if 'image' in user_input.lower():
        parts = user_input.split('"')[1]
        print(parts)
        # if len(parts) > 1:
        #         image_path = parts[1].strip()
        # user_input = input("Enter your question about the image: ").strip()
        
        # Get response from chatbot
        response = agent.run_agent(image_src=parts, text_input=user_input)
        print(f"\nAssistant: {response}")
    
    else:
         response = agent.run_agent(image_src=image_path, text_input=user_input)
         print(f"\nAssistant: {response}")
        # Show memory usage
        # print(f"[Memory: {len(conversation_history)} messages]")

    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("Goodbye")
        break
    elif user_input.lower()  == 'clear':
        agent.clear_history()
        print('History cleared')
        continue
    elif user_input.lower().startswith('save '):
        filename = user_input[5:].strip()
        agent.save_conversation()
        continue
    elif user_input.lower().startswith('load '):
        filename = user_input[5:].strip()
        agent.get_conversation_history()
        continue
     
    