import os,sys,csv,time,uuid
from pathlib import Path
from datetime import datetime,timezone
from dotenv import load_dotenv
from groq import Groq
sys.path.insert(0,str(Path(__file__).resolve().parent))
from retrieval import PaperRetriever
ROOT=Path(__file__).resolve().parents[1]; RESULTS_DIR=ROOT/"results"; RESULTS_DIR.mkdir(exist_ok=True); CSV_FILE=RESULTS_DIR/"results.csv"
load_dotenv(ROOT/".env"); API_KEY=os.getenv("GROQ_API_KEY")
if not API_KEY: raise RuntimeError("GROQ_API_KEY not found in .env")
MODEL="openai/gpt-oss-20b"; MIN_SCORE=0.05; TOP_K=5
client=Groq(api_key=API_KEY,max_retries=0,timeout=60); retriever=PaperRetriever()
SYSTEM_PROMPT="""
You are a research assistant.
Answer questions ONLY using the supplied research paper passages.
Rules:
1. Do not use outside knowledge.
2. Do not invent technical details.
3. If the passages do not contain enough evidence, refuse politely.
4. Every factual claim must have a citation.
5. Use this exact citation format: [Paper Name, Page X]
6. Use the exact paper name and page from the passages.
7. Never use generic citations such as [Source 1].
8. Do not guess missing information.
"""
def ensure_csv():
    if not CSV_FILE.exists():
        with open(CSV_FILE,"w",newline="",encoding="utf-8") as f:
            csv.writer(f).writerow(["request_id","scenario","source","start_time","first_token_ms","total_ms","status","retries","tokens_in","tokens_out","retrieval_setting","answer_grade"])
def append_result(row):
    ensure_csv()
    with open(CSV_FILE,"a",newline="",encoding="utf-8") as f: csv.writer(f).writerow(row)
def approximate_tokens(text):
    # Approximate word-count proxy, not exact API tokens.
    return len(text.split())
def build_context(passages):
    blocks=[]
    for item in passages:
        blocks.append(f"Paper: {item.get('paper','Unknown Paper')}\nPage: {item.get('page','Unknown')}\nPassage:\n{item.get('text','')}")
    return "\n\n".join(blocks)
def ask_question(question,scenario="manual"):
    request_id=str(uuid.uuid4()); start_time=datetime.now(timezone.utc).isoformat(); start=time.perf_counter()
    print("\nSearching research papers...\n"); passages=retriever.search(question,top_k=TOP_K); retrieval_setting="tfidf_top5_threshold_0.05"
    if not passages or passages[0]["score"]<MIN_SCORE:
        answer="The provided research papers do not contain sufficient information to answer this question."
        total_ms=(time.perf_counter()-start)*1000; print("\n========== ANSWER ==========\n"); print(answer)
        append_result([request_id,scenario,"real",start_time,"",round(total_ms,2),"ok",0,approximate_tokens(question),approximate_tokens(answer),retrieval_setting,"refused_correctly"])
        return answer
    context=build_context(passages)
    user_prompt=f"""
Research question:
{question}
Retrieved passages:
{context}
Answer using only these passages.
Cite factual claims using [Paper Name, Page X].
If the evidence is insufficient, refuse.
"""
    first_token_time=None; answer_parts=[]; status="ok"
    print("\nGenerating answer using Groq...\n")
    try:
        stream=client.chat.completions.create(model=MODEL,messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_prompt}],temperature=0.2,max_completion_tokens=1024,reasoning_effort="low",include_reasoning=False,stream=True)
        for chunk in stream:
            if not chunk.choices: continue
            content=chunk.choices[0].delta.content
            if content:
                if first_token_time is None: first_token_time=(time.perf_counter()-start)*1000
                answer_parts.append(content); print(content,end="",flush=True)
        answer="".join(answer_parts)
        if not answer.strip(): status="error"; answer="The model returned an empty response."
    except Exception as exc:
        error_name=type(exc).__name__
        if error_name=="RateLimitError": status="rate_limited"; answer="The model service rate limit was reached."
        elif error_name in ("APITimeoutError","Timeout"): status="timeout"; answer="The model request timed out."
        else: status="error"; answer=f"Model request failed: {error_name}"
        print("\n",answer)
    total_ms=(time.perf_counter()-start)*1000; tokens_in=approximate_tokens(user_prompt); tokens_out=approximate_tokens(answer)
    print("\n\n========== PERFORMANCE ==========")
    print("First token:",round(first_token_time,2) if first_token_time is not None else "Not measured")
    print("Total latency:",round(total_ms,2),"ms"); print("Retrieved passages:",len(passages)); print("Input tokens (approx.):",tokens_in); print("Output tokens (approx.):",tokens_out)
    print("\n========== SOURCES ==========")
    for item in passages: print(item.get("paper"),"- Page",item.get("page"),"- Score:",round(item.get("score",0),4))
    print("\n========== STATUS =========="); print(status)
    append_result([request_id,scenario,"real",start_time,round(first_token_time,2) if first_token_time is not None else "",round(total_ms,2),status,0,tokens_in,tokens_out,retrieval_setting,""])
    return answer
if __name__=="__main__":
    print("================================"); print("       THE RELAY ASSISTANT"); print("================================")
    while True:
        question=input("\nAsk a research question (or type exit): ").strip()
        if question.lower() in ("exit","quit"): break
        if question: ask_question(question)
