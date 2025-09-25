def get_chatbot_response(client,model,messages,temperature=0):
    input_messages=[]
    for message in messages:
        input_messages.append({"role":message["role"],"content":message["content"]})
    
    ans = client.chat.completions.create(
        model=model,
        messages=input_messages,
        temperature=temperature,
        top_p=0.8,
        max_tokens=2000
    ).choices[0].message.content
    
    return ans


from langchain_huggingface import HuggingFaceEmbeddings
embedding_client = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)
def get_embedding(text_input: str):
    return embedding_client.embed_query(text_input)

def double_check_json_output(client,model_name,json_string):
    prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is correct just return it.

    Do NOT return a single letter outside of the json string.

    {json_string}
    """

    messages = [{"role": "user", "content": prompt}]

    response = get_chatbot_response(client,model_name,messages)

    return response