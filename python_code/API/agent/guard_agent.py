from openai import OpenAI 
import os
import json
from copy import deepcopy
from .utils import get_chatbot_response
from dotenv import load_dotenv
load_dotenv()


class GuardAgent:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL')
        self.api_key = os.getenv('HF_TOKEN')
        self.model = os.getenv('MODEL_NAME')

        if not all([self.base_url, self.api_key, self.model]):
            raise ValueError("Missing environment variables for OpenAI client.")

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        
    def get_response(self,messages):
        messages = deepcopy(messages)
                            
        system_prompt = """
            You are an AI assistant for the coffee shop **'It's Hot'**, which serves drinks, bakery items, and chocolate drinks. 
            Your task is to determine whether a user's message is relevant to the coffee shop or supported content, and respond accordingly.

            Allowed user intents:
            1. Questions about the coffee shop (location, working hours, menu items, etc.).
            2. Questions about menu items (ingredients, details, descriptions).
            3. Placing an order.
            4. Asking for recommendations on what to buy.
            5. Requests to read content such as stories, poetry, or jokes, optionally in a specific language.

            Not allowed user intents:
            1. Questions unrelated to the coffee shop or the supported content above.
            2. Questions about staff or how to make menu items.

            Reply style:
            - When replying to allowed coffee shop messages, your tone should be **funny, playful, or flirty**, optionally adapting to gender cues if provided in the user’s message.
            - When replying to allowed content requests (jokes, poetry, stories), keep it friendly and engaging.

            Output instructions:
            - Always respond in **exactly** this JSON format (keys and values as strings):

            {
            "chain of thought": "<analyze the message and explain which allowed/not allowed point it corresponds to>",
            "decision": "allowed" or "not allowed",
            "message": "<leave empty if allowed; if not allowed, write: 'Sorry, I can't help with that. Can I help you with your order or content?'>"
            }

            - Your "chain of thought" should briefly reason through the message, referring to the points above.
            - The "decision" must be exactly 'allowed' or 'not allowed'.
            - The "message" must follow the instructions above without variation.
            - Do not include anything outside this JSON.
        """
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]    # Only last 3 user messages + system prompt

        chatbot_output =get_chatbot_response(self.client,self.model,input_messages)
        output = self.postprocess(chatbot_output)
        
        return output
    
    def postprocess(self,output):
        output = json.loads(output)   # Convert the raw JSON string from the chatbot into a Python dictionary

        # Create a structured dictionary to return
        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory": {"agent":"guard_agent",
                       "guard_decision": output['decision']
                      }
        }
        return dict_output
                
              
                

