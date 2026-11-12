import asyncio,csv,sys,uuid,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from standin import StandInModel
RESULTS_DIR=ROOT/"results"; RESULTS_DIR.mkdir(exist_ok=True); CSV_FILE=RESULTS_DIR/"results.csv"
HEADERS=["request_id","scenario","source","start_time","first_token_ms","total_ms","status","retries","tokens_in","tokens_out","retrieval_setting","answer_grade"]
def ensure_csv():
    if not CSV_FILE.exists():
        with open(CSV_FILE,"w",newline="",encoding="utf-8") as f: csv.writer(f).writerow(HEADERS)
def save_row(row):
    with open(CSV_FILE,"a",newline="",encoding="utf-8") as f: csv.writer(f).writerow(row)
async def run_one(model,scenario,retry_limit=0):
    prompt="Explain multi-head attention using retrieved research papers."; request_id=str(uuid.uuid4()); start_time=datetime.now(timezone.utc).isoformat(); overall_start=time.perf_counter(); retries=0
    while True:
        result=await model.request(prompt,stream=True)
        if result["status"]=="ok": break
        if retries>=retry_limit: break
        retries+=1; await asyncio.sleep(0.05)
    total_ms=(time.perf_counter()-overall_start)*1000
    save_row([request_id,scenario,"stand-in",start_time,round(result["ttft_ms"],2) if result["ttft_ms"] is not None else "",round(total_ms,2),result["status"],retries,result["tokens_in"],result["tokens_out"],"simulated",""])
    return result
async def run_sequential(model,scenario,count,retry_limit=0):
    results=[]
    for _ in range(count): results.append(await run_one(model,scenario,retry_limit))
    return results
async def run_burst(model,scenario,count,retry_limit=0):
    tasks=[run_one(model,scenario,retry_limit) for _ in range(count)]
    return await asyncio.gather(*tasks)
async def main():
    ensure_csv(); print("\n========== STAND-IN EXPERIMENTS ==========\n"); print("1. Steady traffic")
    steady=StandInModel(requests_per_minute=60,daily_budget=10000,base_latency=0.8,failure_rate=0.02,seed=10); await run_sequential(steady,"steady",10,retry_limit=1)
    print("2. Burst traffic"); burst=StandInModel(requests_per_minute=5,base_latency=0.8,failure_rate=0.02,seed=20); await run_burst(burst,"burst",15)
    print("3. Sustained overload"); overload=StandInModel(requests_per_minute=5,base_latency=1.2,failure_rate=0.08,seed=30); await run_burst(overload,"sustained_overload",20)
    print("4. Per-minute limit halved"); halved=StandInModel(requests_per_minute=2,base_latency=0.8,failure_rate=0.0,seed=40); await run_sequential(halved,"per_minute_limit_halved",6)
    print("5. Daily budget exhausted"); exhausted=StandInModel(requests_per_minute=60,daily_budget=3,base_latency=0.8,failure_rate=0.0,seed=50); await run_sequential(exhausted,"daily_budget_exhausted",6)
    print("\nExperiments completed."); print("CSV saved to:",CSV_FILE)
if __name__=="__main__": asyncio.run(main())
