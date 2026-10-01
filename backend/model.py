import time
from config.settings import (
    USE_LOCAL, GROQ_MODEL, OLLAMA_MODEL,
    LLM_TEMPERATURE, LLM_MAX_TOKENS, LLM_SLEEP_SECONDS,
    GROQ_API_KEY, RETRY_BACKOFF,MAX_RETRIES
)

print("USE_LOCAL : ",USE_LOCAL)
def get_model():
    if USE_LOCAL:
        from langchain_ollama import ChatOllama
        model=ChatOllama(model=OLLAMA_MODEL,temperature=LLM_TEMPERATURE)
        
    else:
        from groq import Groq
        model=Groq(api_key=GROQ_API_KEY)
        # from huggingface_hub import InferenceClient
        # hf_api=os.getenv('HUGGINGFACE_API')
        # model=InferenceClient(api_key=hf_api)
        
    return model
        
def invoke_model(model,prompt):
    """
    Invoking model based on used_local
    """
    time.sleep(LLM_SLEEP_SECONDS)
    if USE_LOCAL:
        result=model.invoke(prompt)
        return result.content
    else:
        for attempt in range(MAX_RETRIES):
            try:
                result = model.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=LLM_MAX_TOKENS,
                    temperature=LLM_TEMPERATURE
                )
                content = result.choices[0].message.content
                print(f"Raw content: '{content[:100] if content else 'NONE'}'")
                print(f"Finish reason: {result.choices[0].finish_reason}")
                return content
            except Exception as e:
                error_str = str(e)
                print(f"Groq error: {error_str}")
                if "429" in error_str and "tokens per minute" in error_str and attempt < 2:
                    wait = RETRY_BACKOFF * (attempt + 1)
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
