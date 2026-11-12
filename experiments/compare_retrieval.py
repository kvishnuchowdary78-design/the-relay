import csv,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from retrieval import PaperRetriever
OUTPUT_FILE=ROOT/"results"/"retrieval_comparison.csv"
QUESTIONS=[
{"id":"Q1","question":"What is the Transformer architecture?","expected_paper":"Attention Is All You Need"},
{"id":"Q2","question":"How does multi-head attention work?","expected_paper":"Attention Is All You Need"},
{"id":"Q3","question":"What is scaled dot-product attention?","expected_paper":"Attention Is All You Need"},
{"id":"Q4","question":"How does Moshi support real-time speech dialogue?","expected_paper":"Moshi: A Speech-Text Foundation Model"},
{"id":"Q5","question":"What is dynamic chunking in hierarchical sequence modeling?","expected_paper":"Dynamic Chunking for End-to-End Hierarchical Sequence Modeling"}]
TOP_K_VALUES=[3,5,8]
def main():
    retriever=PaperRetriever(); rows=[]
    for item in QUESTIONS:
        for top_k in TOP_K_VALUES:
            start=time.perf_counter(); results=retriever.search(item["question"],top_k=top_k); elapsed_ms=(time.perf_counter()-start)*1000
            retrieved_papers=sorted({result.get("paper","Unknown") for result in results}); retrieved_pages=sorted({str(result.get("page","Unknown")) for result in results})
            context_words=sum(len(result.get("text","").split()) for result in results)
            relevant_count=sum(1 for result in results if result.get("paper")==item["expected_paper"])
            relevance_ratio=relevant_count/len(results) if results else 0
            rows.append({"question_id":item["id"],"question":item["question"],"expected_paper":item["expected_paper"],"top_k":top_k,"retrieval_latency_ms":round(elapsed_ms,3),"returned_chunks":len(results),"context_words":context_words,"expected_paper_chunks":relevant_count,"expected_paper_ratio":round(relevance_ratio,3),"retrieved_papers":" ; ".join(retrieved_papers),"retrieved_pages":" ; ".join(retrieved_pages)})
            print(f'{item["id"]} | top_k={top_k} | {len(results)} chunks | {elapsed_ms:.2f} ms | {context_words} words | expected-paper ratio={relevance_ratio:.2f}')
    OUTPUT_FILE.parent.mkdir(parents=True,exist_ok=True)
    with open(OUTPUT_FILE,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys())); writer.writeheader(); writer.writerows(rows)
    print("\nRetrieval comparison completed."); print("Configurations:",TOP_K_VALUES); print("Questions:",len(QUESTIONS)); print("Total experiments:",len(rows)); print("Saved to:",OUTPUT_FILE)
if __name__=="__main__": main()
