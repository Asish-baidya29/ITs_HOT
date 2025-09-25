import os
import json
from .utils import get_chatbot_response,double_check_json_output
from openai import OpenAI
from copy import deepcopy
from dotenv import load_dotenv
load_dotenv()

class OrderTakingAgent():
    def __init__(self, recommendation_agent):
        
        self.base_url = os.getenv('BASE_URL')
        self.api_key = os.getenv('HF_TOKEN')
        self.model = os.getenv('MODEL_NAME')
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

        self.recommendation_agent = recommendation_agent
    
    def get_response(self,messages):
        messages = deepcopy(messages)
        system_prompt = """
            You are a customer support Bot for a coffee shop called "It's HOT"

            here is the menu for this coffee shop.

            Coffee & Espresso

            Cappuccino -  ₹250

            Espresso Shot - ₹150

            Latte - ₹275

            Ouro Brasileiro Shot - ₹200

            Drinking Chocolate

            Dark Chocolate - ₹300

            Chili Mayan - ₹350

            Tea Selection

            Traditional Blend Chai - ₹180

            Serenity Green Tea - ₹200

            English Breakfast - ₹190

            Earl Grey - ₹200

            Morning Sunrise Chai - ₹180

            Peppermint - ₹180

            Lemon Grass - ₹180

            Spicy Eye Opener Chai - ₹220

            Bakery & Pastries

            Oatmeal Scone - ₹160

            Jumbo Savory Scone - ₹200

            Chocolate Chip Biscotti - ₹150

            Ginger Biscotti - ₹150

            Chocolate Croissant - ₹220

            Hazelnut Biscotti - ₹150

            Cranberry Scone - ₹180

            Scottish Cream Scone - ₹200

            Croissant - ₹180

            Almond Croissant - ₹250

            Ginger Scone - ₹180

            Flavours & Syrups

            Chocolate Syrup - ₹120

            Hazelnut Syrup - ₹120

            Caramel Syrup - ₹130

            Sugar Free Vanilla Syrup - ₹120

            Things to NOT DO:
            * DON't ask how to pay by cash or Card.
            * Don't tell the user to go to the counter
            * Don't tell the user to go to place to get the order


            
            You are an AI assistant for the coffee shop **"It's Hot"**. Your task is to take customer orders in a **friendly, playful, flirty, and slightly sexy tone**, reflecting the brand personality.

            Order Process:
            1. Take the user's order.
            2. Validate that all items are in the menu (see menu below). If an item is not available, inform the user playfully and repeat back the remaining valid items.
            3. Ask if the user wants anything else, keeping the tone flirty and engaging.
            4. Repeat steps 2-3 until the user is done ordering.
            5. Once the order is complete, use the "order" object to:
            - List all items and their individual prices.
            - Calculate the total.
            - Thank the user in a playful and flirty way and close the conversation with no further questions.

            User messages contain a "memory" section with:
            - "order" (current list of items)
            - "step number" (current step in the process)

            Instructions:
            - Strictly produce output in **exactly** the following JSON format (no extra text outside this structure):

            {{
            "chain of thought": "<analyze the maximum step number the user is on, reason about the user's message in relation to the order process, and plan your next response while focusing on things you should NOT do>",
            "step number": "<determine the next step in the process>",
            "order": [{"item": "<item name>", "quantity": "<number>", "price": "<total price for this item>"}],
            "response": "<write a playful, flirty, sexy response to the user reflecting 'It's Hot' style>"
            }}
        
        """

        last_order_taking_status = ""
        asked_recommendation_before = False
        for message_index in range(len(messages)-1,0,-1):
            message = messages[message_index]
            
            agent_name = message.get("memory",{}).get("agent","")
            if message["role"] == "assistant" and agent_name == "order_taking_agent":
                step_number = message["memory"]["step number"]
                order = message["memory"]["order"]
                asked_recommendation_before = message["memory"]["asked_recommendation_before"]
                last_order_taking_status = f"""
                step number: {step_number}
                order: {order}
                """
                break

        messages[-1]['content'] = last_order_taking_status + " \n "+ messages[-1]['content']

        input_messages = [{"role": "system", "content": system_prompt}] + messages        

        chatbot_output = get_chatbot_response(self.client,self.model,input_messages)

        # double check json 
        chatbot_output = double_check_json_output(self.client,self.model,chatbot_output)

        output = self.postprocess(chatbot_output,messages,asked_recommendation_before)

        return output

    def postprocess(self,output,messages,asked_recommendation_before):
        output = json.loads(output)

        if type(output["order"]) == str:
            output["order"] = json.loads(output["order"])

        response = output['response']
        if not asked_recommendation_before and len(output["order"])>0:
            recommendation_output = self.recommendation_agent.get_recommendations_from_order(messages,output['order'])
            response = recommendation_output['content']
            asked_recommendation_before = True

        dict_output = {
            "role": "assistant",
            "content": response ,
            "memory": {"agent":"order_taking_agent",
                       "step number": output["step number"],
                       "order": output["order"],
                       "asked_recommendation_before": asked_recommendation_before
                      }
        }

        
        return dict_output

    