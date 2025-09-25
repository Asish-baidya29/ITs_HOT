import json
import pandas as pd
import os
from .utils import get_chatbot_response
from openai import OpenAI
from copy import deepcopy
from dotenv import load_dotenv
load_dotenv()

class RecommendationAgent():
    
    def __init__(self,apriori_recommendation_path,popular_recommendation_path):
        
        self.base_url = os.getenv('BASE_URL')
        self.api_key = os.getenv('HF_TOKEN')
        self.model = os.getenv('MODEL_NAME')
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

        with open(apriori_recommendation_path, 'r') as file:
            self.apriori_recommendations = json.load(file)

        self.popular_recommendations = pd.read_csv(popular_recommendation_path)
        self.products = self.popular_recommendations['product'].tolist()
        self.product_categories = self.popular_recommendations['product_category'].tolist()
    
    def get_apriori_recommendation(self,products,top_k=5):
        recommendation_list = []
        for product in products:
            if product in self.apriori_recommendations:
                recommendation_list += self.apriori_recommendations[product]
        
        # Sort recommendation list by "confidence"
        recommendation_list = sorted(recommendation_list,key=lambda x: x['confidence'],reverse=True)

        recommendations = []
        recommendations_per_category = {}
        for recommendation in recommendation_list:
            # If Duplicated recommendations then skip
            if recommendation in recommendations:
                continue 

            # Limit 2 recommendations per category
            product_catory = recommendation['product_category']
            if product_catory not in recommendations_per_category:
                recommendations_per_category[product_catory] = 0
            
            if recommendations_per_category[product_catory] >= 2:
                continue

            recommendations_per_category[product_catory]+=1

            # Add recommendation
            recommendations.append(recommendation['product'])

            if len(recommendations) >= top_k:
                break

        return recommendations 

    def get_popular_recommendation(self,product_categories=None,top_k=5):
        recommendations_df = self.popular_recommendations
        
        if type(product_categories) == str:
            product_categories = [product_categories]

        if product_categories is not None:
            recommendations_df = self.popular_recommendations[self.popular_recommendations['product_category'].isin(product_categories)]
        recommendations_df = recommendations_df.sort_values(by='numb_of_transactions',ascending=False) 
        
        if recommendations_df.shape[0] == 0:
            return []

        recommendations = recommendations_df['product'].tolist()[:top_k]
        return recommendations

    def recommendation_classification(self,messages):
        system_prompt = f"""
            You are a helpful AI assistant for a coffee shop application called "It's Hot" which serves drinks and pastries. 
            We have three types of recommendations:

            1. Apriori Recommendations: Recommendations based on the user's order history. Recommend items that are frequently bought together with items in the user's order.
            2. Popular Recommendations: Recommendations based on item popularity across all customers. No additional parameters required.
            3. Popular Recommendations by Category: Recommendations based on popularity within a specific category requested by the user. For example, if the user asks "Which coffee should I get?", recommend popular items in the 'coffee' category.

            Available items in the coffee shop:
            {', '.join(self.products)}

            Available categories in the coffee shop:
            {', '.join(self.product_categories)}

            Instructions:
            - Determine which type of recommendation is appropriate based on the user's message.
            - Respond in **exactly** this JSON format (keys and values as strings):

            {{
            "chain of thought": "<briefly reason about which recommendation type fits the user's input>",
            "recommendation_type": "apriori" or "popular" or "popular by category",
            "parameters": "<python list of items for apriori, or list of categories for popular by category; leave empty list for popular>"
            }}

            - Use **exact item and category names** from the lists above.
            - Do not include any text outside the JSON.
        """


        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]

        chatbot_output =get_chatbot_response(self.client,self.model,input_messages)
        output = self.postprocess_classfication(chatbot_output)
        return output

    def get_response(self,messages):
        messages = deepcopy(messages)

        recommendation_classification = self.recommendation_classification(messages)
        recommendation_type = recommendation_classification['recommendation_type']
        recommendations = []
        if recommendation_type == "apriori":
            recommendations = self.get_apriori_recommendation(recommendation_classification['parameters'])
        elif recommendation_type == "popular":
            recommendations = self.get_popular_recommendation()
        elif recommendation_type == "popular by category":
            recommendations = self.get_popular_recommendation(recommendation_classification['parameters'])
        
        if recommendations == []:
            return {"role": "assistant", "content":"Sorry, I can't help with that. Can I help you with your order?"}
        
        # Respond to User
        recommendations_str = ", ".join(recommendations)
        
        system_prompt = f"""
            You are a helpful AI assistant for a coffee shop application called **"It's Hot"** which serves drinks and pastries. 
            Your task is to recommend items to the user based on their input message. 

            Instructions:
            - Respond in a **friendly, playful, flirty, and slightly sexy tone**—like a waiter teasing a customer in a fun way.
            - Use an **unordered list** to display the items, with a **very short description** for each.
            - Only recommend the items I provide; do not add any extra items.
            - Keep your response concise, engaging, and “It's Hot”-style.

            Example format:
            - Item 1: Short flirty description.
            - Item 2: Short flirty description.
        """

        prompt = f"""
        {messages[-1]['content']}

        Please recommend exactly these items: {recommendations_str}
        """



        messages[-1]['content'] = prompt
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]

        chatbot_output =get_chatbot_response(self.client,self.model,input_messages)
        output = self.postprocess(chatbot_output)

        return output



    def postprocess_classfication(self,output):
        output = json.loads(output)

        dict_output = {
            "recommendation_type": output['recommendation_type'],
            "parameters": output['parameters'],
        }
        return dict_output

    def get_recommendations_from_order(self,messages,order):
        products = []
        for product in order:
            products.append(product['item'])

        recommendations = self.get_apriori_recommendation(products)
        recommendations_str = ", ".join(recommendations)

        system_prompt = f"""
            You are a helpful AI assistant for a coffee shop application which serves drinks and pastries.
            Your task is to recommend items to the user based on their order.
            - Your reply should be **sexy, funny, and flirty**, reflecting the personality of our coffee shop "It's Hot".
            - Keep the recommendations friendly, playful, and engaging.

            I will provide the items you should recommend to the user based on their order in the user's message.
        """

        prompt = f"""
        User message:
        {messages[-1]['content']}

        Please recommend the following items exactly as provided: {recommendations_str}
        """


        messages[-1]['content'] = prompt
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]

        chatbot_output =get_chatbot_response(self.client,self.model,input_messages)
        output = self.postprocess(chatbot_output)

        return output
    
    def postprocess(self,output):
        output = {
            "role": "assistant",
            "content": output,
            "memory": {"agent":"recommendation_agent"
                      }
        }
        return output