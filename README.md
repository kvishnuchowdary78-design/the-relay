# The Relay

A retrieval-augmented question-answering pipeline and reliability experiment using three research papers, Groq-hosted inference, and a configurable local stand-in.

## Contents
- `REPORT.md` — two-page report draft (export and check page count before submission).
- `results/retrieval_comparison_reconstructed.csv` — comparison reconstructed from console output; retain the locally generated CSV as primary evidence.
- `experiments/questions_for_retrieval.csv` — five retrieval-comparison questions and expected paper labels.
- `SUBMISSION_CHECKLIST.md` — final verification checklist.

## Local project
The complete working project is on the developer's Windows machine at `C:\Users\Vishnu\the-relay`. Source files and the original full `results/results.csv` still need to be pushed from that local working tree.

## Run locally
Activate the virtual environment, install requirements, configure `GROQ_API_KEY` in `.env`, then run:
```cmd
python experiments\run_experiments.py
python experiments\analyze_results.py
python experiments\compare_retrieval.py
```

Never commit `.env` or API keys. Search the repository and Git history for secrets before publishing.

## Evidence distinctions
The reconstructed retrieval CSV is based on terminal output, not direct access to the local CSV file. Stand-in measurements are simulated. Real pipeline token counts are approximate word-count proxies unless provider usage was explicitly captured.
