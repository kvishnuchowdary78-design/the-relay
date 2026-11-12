# The Relay

A retrieval-augmented question-answering pipeline and reliability experiment using three research papers, Groq-hosted inference, and a configurable local stand-in.

## Project structure
- `src/` — paper download, PDF ingestion, TF-IDF retrieval, Groq streaming client and RAG pipeline.
- `experiments/` — stand-in experiments, result analysis, retrieval comparison and grading scripts.
- `results/results.csv` — raw real-service and stand-in experiment records.
- `results/retrieval_comparison.csv` — original top-k retrieval comparison output.
- `REPORT.md` — report draft; check it is no more than two pages after PDF export.
- `SUBMISSION_CHECKLIST.md` — final verification checklist.

## Setup (Windows)
```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
```
Add your own Groq API key to `.env` as `GROQ_API_KEY=your_key_here`. Never commit `.env`.

## Download papers and build the index
```cmd
python src\download_papers.py
python src\ingestion.py
```
The downloader uses the exact arXiv versions listed in the assignment. The PDFs and generated `data/chunks.json` are not stored in this repository; regenerate them with the commands above.

## Run
```cmd
python src\groq_client.py
python src\pipeline.py
python experiments\run_experiments.py
python experiments\compare_retrieval.py
python experiments\analyze_results.py
```

## Evidence notes
- Real-service test: 15 requests, 4 successful and 11 rate-limited.
- The 4 successful answers have manual grades recorded in `results/results.csv`; the grade rubric is 0–2.
- Stand-in values are simulated, not Groq measurements.
- Pipeline token counts are approximate word-count proxies, not exact provider token usage.
- The overload experiment is 20 concurrent requests, not a time-based sustained-arrival test.
- The original results CSV and retrieval comparison are included. PDF inputs and generated chunks can be recreated using the scripts.
