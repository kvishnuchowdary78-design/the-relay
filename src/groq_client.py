import os,time
from dotenv import load_dotenv
from groq import Groq
load_dotenv(override=True)
client=Groq(api_key=os.getenv("GROQ_API_KEY"),max_retries=0,timeout=60.0)
MODEL="openai/gpt-oss-20b"
def test_streaming():
    start=time.perf_counter(); first_token_ms=None; output_parts=[]
    print("\nConnecting to Groq..."); print("Model:",MODEL)
    try:
        stream=client.chat.completions.create(model=MODEL,messages=[{"role":"user","content":"Explain multi-head attention in the Transformer architecture in 3 sentences."}],max_completion_tokens=1024,temperature=0.6,reasoning_effort="low",include_reasoning=False,stream=True)
        print("\n========== STREAMING RESPONSE ==========\n")
        for chunk in stream:
            if not chunk.choices: continue
            content=chunk.choices[0].delta.content
            if content:
                if first_token_ms is None: first_token_ms=(time.perf_counter()-start)*1000
                output_parts.append(content); print(content,end="",flush=True)
        total_ms=(time.perf_counter()-start)*1000; answer="".join(output_parts)
        print("\n\n========== MEASUREMENTS =========="); print("TTFT:",first_token_ms,"ms"); print("Total latency:",round(total_ms,2),"ms"); print("Response characters:",len(answer)); print("Status:","SUCCESS" if answer else "EMPTY_RESPONSE")
    except Exception as error:
        print("\nRequest failed!"); print("Error:",type(error).__name__); print("Details:",str(error))
if __name__=="__main__": test_streaming()
