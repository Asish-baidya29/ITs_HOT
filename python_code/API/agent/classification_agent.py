from openai import OpenAI 
import os
import json
from copy import deepcopy
from .utils import get_chatbot_response
from dotenv import load_dotenv
load_dotenv()


class ClassificationAgent:
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
        messages=deepcopy(messages)
        
        system_prompt = """
            You are an AI assistant for the coffee shop application 'It's Hot'. 
            Your task is to determine **which agent should handle the user's input**. There are three agents:

            1. details_agent: Handles questions about the coffee shop, such as location, delivery areas, working hours, menu item details, or listing available items. Can also clarify "what we have" on the menu.
            2. order_taking_agent: Handles the process of taking orders. Responsible for conversing with the user until the order is complete.
            3. recommendation_agent: Handles user requests for suggestions about what to buy. If the user asks for a recommendation, this agent is responsible.

            Instructions for your output:
            - Always respond in **exactly** this JSON format (keys and values as strings):

            {
            "chain of thought": "<analyze the input and explain which agent is most relevant>",
            "decision": "details_agent" or "order_taking_agent" or "recommendation_agent" or "content_agent",
            "message": ""
            }

            - Your "chain of thought" should briefly reason through the message, referring to the three agents above.
            - The "decision" must be exactly one of the three agent names, no extra text.
            - The "message" must always be an empty string.
            - Do not include anything outside this JSON.
        """

        input_messages = [
            {"role": "system", "content": system_prompt},
        ]

        input_messages += messages[-3:]

        chatbot_output =get_chatbot_response(self.client,self.model,input_messages)
        output = self.postprocess(chatbot_output)
        return output

    def postprocess(self,output):
        output = json.loads(output)    # Convert JSON string to Python dict

        dict_output = {
            "role": "assistant",                   # Always label as assistant
            "content": output['message'],          # Actual message content
            "memory": {"agent":"classification_agent",         # Name of this agent
                       "classification_decision": output['decision']     # Decision metadata
                      }
        }
        return dict_output


        