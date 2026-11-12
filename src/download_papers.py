import requests
from pathlib import Path
papers={"1706.03762v7":"Attention_Is_All_You_Need.pdf","2410.00037v1":"Moshi.pdf","2507.07955v2":"Dynamic_Chunking.pdf"}
folder=Path("data/papers"); folder.mkdir(parents=True,exist_ok=True)
for paper_id,filename in papers.items():
    url=f"https://arxiv.org/pdf/{paper_id}"
    print(f"\nDownloading {paper_id}...")
    try:
        response=requests.get(url,timeout=90); response.raise_for_status()
        if not response.content.startswith(b"%PDF"): raise ValueError("Invalid PDF response")
        path=folder/filename; path.write_bytes(response.content); print(f"Downloaded: {filename}")
    except Exception as error: print(f"Error: {error}")
print("\nDownload process finished.")
