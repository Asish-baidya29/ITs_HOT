import json 
import os 
from openai import OpenAI
from copy import deepcopy
from .utils import get_chatbot_response, get_embedding
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
import dotenv
dotenv.load_dotenv()


class DetailsAgent():
    def __init__(self):
        
        self.base_url = os.getenv('BASE_URL')
        self.api_key = os.getenv('HF_TOKEN')
        self.model_name = os.getenv('MODEL_NAME')
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX_NAME")        
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        
        self.embedding_client = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2'
        )
        
        """# load faiss vdb
        if os.path.exists("faiss_index"):
            self.vector_store = FAISS.load_local(
                "faiss_index",
                self.embedding_client,
                allow_dangerous_deserialization=True
            )
        else:
            self.vector_store = None  # fallback

        if not all([self.base_url, self.api_key, self.model_name]):
            raise ValueError("Missing environment variables for OpenAI client.")"""

    
    def get_closest_results(self,index_name,input_embeddings,top_k=3):
        
        index = self.pc.Index(index_name)
        
        results = index.query(
            namespace="ns1",
            vector=input_embeddings,
            top_k=top_k,
            include_values=False,
            include_metadata=True
        )

        return results
    
        """if not self.vector_store:
            raise ValueError("Vector store not built.")
        return self.vector_store.similarity_search(query, k=k)"""

    
    def get_response(self, messages): # Generate a response
        messages_copy = deepcopy(messages)
        user_message = messages_copy[-1]["content"]
        
        # Retrieve docs 
        embedding = get_embedding(user_message)[0]
            
        result = self.get_closest_results(self.index_name,embedding)                                        
        source_knowledge = "\n".join([x['metadata']['text'].strip()+'\n' for x in result['matches'] ])
        
        # RAG-augmented prompt
        prompt = f"""
        Using the contexts below, answer the query.

        Contexts:
        {source_knowledge}

        Query: {user_message}
        """
        
        # System role
        system_prompt = """
            You are a customer support agent for the coffee shop **'It's Hot'**. 
            Always act and respond like a friendly, playful waiter. 

            Guidelines:
            1. Stay in character as a waiter from 'It's Hot'—be polite, warm, and slightly flirty/funny when appropriate.
            2. Answer all questions about orders, menu items, ingredients, location, hours, and availability.
            3. Help customers place and update their orders smoothly, step by step.
            4. If a user asks for recommendations, suggest drinks or bakery items in a fun and engaging way.
            5. Always keep your answers concise, natural, and conversational—avoid sounding robotic or overly formal.
            6. If the user asks something unrelated to the coffee shop, politely steer them back to their order or menu.

            Tone:
            - Be playful and witty and little flirting, as if chatting with a café guest.
            - Use phrases that match the vibe of 'It's Hot', like teasing about how "hot" the drinks (and maybe the customer) are.
        """
        
        # Final messages: system + last 3 messages + RAG prompt as user input
        messages[-1]['content'] = prompt
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]
    
        
        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)
        return self.postprocess(chatbot_output)
    
    
    def postprocess(self, output):
        """
        Return structured response.
        """
        return {
            "role": "assistant",
            "content": output,
            "memory": {"agent": "details_agent"}
        }
        
        




