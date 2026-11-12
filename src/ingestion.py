from pathlib import Path
from pypdf import PdfReader
import json
PAPERS_DIR=Path("data/papers"); OUTPUT_FILE=Path("data/chunks.json")
PAPERS={"Attention_Is_All_You_Need.pdf":"Attention Is All You Need","Moshi.pdf":"Moshi: A Speech-Text Foundation Model","Dynamic_Chunking.pdf":"Dynamic Chunking for End-to-End Hierarchical Sequence Modeling"}
CHUNK_SIZE=1200; CHUNK_OVERLAP=200
def split_text(text):
    chunks=[]; start=0
    while start<len(text):
        end=start+CHUNK_SIZE; chunk=text[start:end].strip()
        if chunk: chunks.append(chunk)
        if end>=len(text): break
        start=end-CHUNK_OVERLAP
    return chunks
def ingest_papers():
    all_chunks=[]
    for filename,paper_name in PAPERS.items():
        pdf_path=PAPERS_DIR/filename
        if not pdf_path.exists(): print(f"Missing PDF: {filename}"); continue
        print(f"\nProcessing: {paper_name}"); reader=PdfReader(str(pdf_path)); paper_chunk_count=0
        for page_number,page in enumerate(reader.pages,start=1):
            text=page.extract_text() or ""
            if not text.strip(): continue
            for chunk_index,chunk in enumerate(split_text(text)):
                all_chunks.append({"chunk_id":f"{filename}_p{page_number}_c{chunk_index}","paper":paper_name,"filename":filename,"page":page_number,"text":chunk}); paper_chunk_count+=1
        print(f"Pages: {len(reader.pages)}"); print(f"Chunks: {paper_chunk_count}")
    OUTPUT_FILE.parent.mkdir(parents=True,exist_ok=True)
    with open(OUTPUT_FILE,"w",encoding="utf-8") as file: json.dump(all_chunks,file,indent=2,ensure_ascii=False)
    print("\n--------------------------------"); print(f"Total chunks created: {len(all_chunks)}"); print(f"Saved to: {OUTPUT_FILE}"); print("--------------------------------")
if __name__=="__main__": ingest_papers()
