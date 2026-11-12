import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
ROOT=Path(__file__).resolve().parents[1]; CHUNKS_FILE=ROOT/"data"/"chunks.json"
class PaperRetriever:
    def __init__(self,chunks_file=CHUNKS_FILE):
        with open(chunks_file,"r",encoding="utf-8") as f: self.chunks=json.load(f)
        self.texts=[item.get("text","") for item in self.chunks]
        self.vectorizer=TfidfVectorizer(ngram_range=(1,2),max_features=50000,sublinear_tf=True,strip_accents="unicode",token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9_-]+\b")
        self.matrix=self.vectorizer.fit_transform(self.texts)
        print("\n========== RETRIEVER INITIALIZED =========="); print("Total chunks:",len(self.chunks)); print("Vocabulary size:",len(self.vectorizer.vocabulary_)); print("Matrix shape:",self.matrix.shape); print("Non-zero values:",self.matrix.nnz); print("===========================================\n")
    def search(self,query,top_k=5):
        query_vector=self.vectorizer.transform([query]); print("Query:",query); print("Query tokens matched:",query_vector.nnz)
        if query_vector.nnz==0: return []
        scores=cosine_similarity(query_vector,self.matrix).flatten(); ranked_indices=scores.argsort()[::-1]; results=[]
        for index in ranked_indices:
            score=float(scores[index])
            if score<=0: continue
            item=self.chunks[index].copy(); item["score"]=score; results.append(item)
            if len(results)>=top_k: break
        return results
