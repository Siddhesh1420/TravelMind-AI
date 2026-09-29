import os 
from dotenv import load_dotenv
import time

load_dotenv()

use_local=os.getenv("USE_LOCAL","False").lower()=="true"

def get_model():
    if use_local:
        from langchain_ollama import ChatOllama
        model=ChatOllama(model="qwen2.5:7b",temperature=0.1)
        
    else:
        from groq import Groq
        groq_api=os.getenv('GROQ_API_KEY')
        model=Groq(api_key=groq_api)
        # from huggingface_hub import InferenceClient
        # hf_api=os.getenv('HUGGINGFACE_API')
        # model=InferenceClient(api_key=hf_api)
        
    return model
        
def invoke_model(model,prompt):
    """
    Invoking model based on used_local
    """
    time.sleep(3)
    if use_local:
        result=model.invoke(prompt)
        return result.content
    else:
        result=model.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.1
        )
    #     result = model.chat.completions.create(
    #     model="zai-org/GLM-5.2",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ],
    #     max_tokens=4000
    # )

        
        return result.choices[0].message.content