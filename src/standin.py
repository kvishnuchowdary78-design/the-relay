import asyncio,random,time
class StandInModel:
    def __init__(self,requests_per_minute=60,daily_budget=10000,base_latency=.8,failure_rate=.02,timeout_seconds=8.0,seed=42):
        self.requests_per_minute=requests_per_minute; self.daily_budget=daily_budget; self.base_latency=base_latency; self.failure_rate=failure_rate; self.timeout_seconds=timeout_seconds; self.request_times=[]; self.daily_requests=0; self.active_requests=0; self.random=random.Random(seed)
    async def request(self,prompt,stream=True):
        started=time.perf_counter(); self.active_requests+=1
        try:
            now=time.monotonic(); self.request_times=[t for t in self.request_times if now-t<60]; tokens_in=len(prompt.split())
            if self.daily_requests>=self.daily_budget: return self.make_result("rate_limited",started,tokens_in,0)
            if len(self.request_times)>=self.requests_per_minute: return self.make_result("rate_limited",started,tokens_in,0)
            self.request_times.append(now); self.daily_requests+=1; load_factor=1+max(0,self.active_requests-1)*.25; delay=self.base_latency*load_factor+self.random.uniform(.05,.30)
            if delay>self.timeout_seconds:
                await asyncio.sleep(self.timeout_seconds); return self.make_result("timeout",started,tokens_in,0)
            if self.random.random()<self.failure_rate:
                await asyncio.sleep(min(delay,.3)); return self.make_result("error",started,tokens_in,0)
            await asyncio.sleep(delay*.65); response="The retrieved research passages support this answer. The system uses retrieval to provide relevant context and generates a response grounded in that context."; words=response.split(); streamed_parts=[]
            if stream:
                for i in range(0,len(words),5): streamed_parts.extend(words[i:i+5]); await asyncio.sleep(.015)
            else: streamed_parts=words
            text=" ".join(streamed_parts); result=self.make_result("ok",started,tokens_in,len(text.split()),text); result["ttft_ms"]=delay*.65*1000; return result
        finally: self.active_requests-=1
    @staticmethod
    def make_result(status,started,tokens_in,tokens_out,text=""):
        return {"status":status,"text":text,"ttft_ms":None,"total_ms":(time.perf_counter()-started)*1000,"tokens_in":tokens_in,"tokens_out":tokens_out}
