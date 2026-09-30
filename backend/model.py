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
    time.sleep(5)
    if use_local:
        result=model.invoke(prompt)
        return result.content
    else:
        for attempt in range(3):
            try:
                result = model.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=4000,
                    temperature=0.1
                )
                return result.choices[0].message.content
            except Exception as e:
                error_str = str(e)
                if "429" in error_str and "tokens per minute" in error_str and attempt < 2:
                    wait = 15 * (attempt + 1)
                    print(f"TPM rate limited — waiting {wait}s...")
                    time.sleep(wait)
                elif "429" in error_str and "tokens per day" in error_str:
                    print("Daily token limit hit")
                    return ""
                else:
                    raise e
            return ""
        
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
