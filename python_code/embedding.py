"""import firebase_admin
from firebase_admin import credentials,storage
from firebase_admin import db """

from langchain_huggingface import HuggingFaceEmbeddings
import pandas as pd
from langchain.schema import Document
from langchain.vectorstores import FAISS
from time import time
import pandas as pd 
import os 
import dotenv

dotenv.load_dotenv()


#------------------------------------------
#firebase init
#------------------------------------------

"""service_account_info = {
    "type":os.getenv("FIREBASE_TYPE"),
    "project_id":os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id":os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key":os.getenv("FIREBASE_PRIVATE_KEY"),
    "client_email":os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id":os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri":os.getenv("FIREBASE_AUTH_URI"),
    "token_uri":os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url":os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url":os.getenv("FIREBASE_CLIENT_CERT_URL"),
    "universe_domain":os.getenv("FIREBASE_UNIVERSE_DOMAIN")
}
"""
"""cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred,{
    'storageBucket':'',
    'databaseURL':'https://coffee-e5b94-default-rtdb.firebaseio.com/'
})"""

#---------------------
# vectordb
#---------------------
from pinecone import Pinecone,ServerlessSpec
from openai import OpenAI


token = os.getenv("HF_TOKEN")
index_name = os.getenv("pinecone_index_name")
Pinecone_api_key = os.getenv("vectorDB_API")
pc = Pinecone(api_key=Pinecone_api_key)
embedding_client = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)

x="""hi my name is asish"""
output = embedding_client.embed_query(x)

len(output)

df = pd.read_json("../python_code/products/products.jsonl",lines=True)
df['text']=df['name']+" : "+df["description"]+\
    " -- Ingredients: "+df["ingredients"].astype(str) +\
    " -- Price: "+ df["price"].astype(str) +\
    " -- rating: "+ df["rating"].astype(str)
    
df['text'].head(4)

texts = df['text'].tolist()
with open("../python_code/products/about_US.txt") as f:
    Its_hot_about_section =f.read()
    
Its_hot_about_section="About our coffee shop It's Hot : "+ Its_hot_about_section
texts.append(Its_hot_about_section)

with open("../python_code/products/ITsHOT_menu.txt") as f:
    Menu_Items_text =f.read()
    
Menu_Items_text="Menu Items: "+ Menu_Items_text
texts.append(Menu_Items_text)


# Generate Embeddings for our txts
embeddings = embedding_client.embed_documents(texts)

index_name = "coffeeshop"

pc.create_index(
    name=index_name,
    dimension=384, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

# Wait for the index to be ready
while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)

index = pc.Index(index_name)

vectors = []
for text, e in zip(texts, embeddings):
    entry_id = text.split(":")[0].strip()
    vectors.append({
        "id": entry_id,
        "values": e,
        "metadata": {'text': text}
    })
    
index.upsert(
    vectors=vectors,
    namespace="ns1"
)


embeddings = embedding_client.embed_documents(["price of Cappuccino ?"])
print(type(embeddings))  # list[list[float]]
print(len(embeddings[0]))


results = index.query(
    namespace="ns1",
    vector=embeddings,
    top_k=3,
    include_values=False,
    include_metadata=True
)

print(results)


"""# text to documents
documents = [Document(page_content=text) for text in texts]
# Create a FAISS vector store 
vector_store = FAISS.from_documents(documents, embedding_client)

# Example: search for similar content
query = "price of Cappuccino "
results = vector_store.similarity_search(query, k=8)

for r in results:
    print(r.page_content)"""
    
    

"""# save documents 
import pickle

with open("documents.pkl", "wb") as f:
    pickle.dump(documents, f)
    
# save vector_store
vector_store.save_local("faiss_index")"""


    
    







