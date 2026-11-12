# Final Submission Checklist

## Evidence and results
- [ ] Copy the actual `results/results.csv` from `C:\Users\Vishnu\the-relay\results\results.csv` into this repository.
- [ ] Add the locally generated `results/retrieval_comparison.csv`; the reconstructed CSV is only a convenience copy of console output.
- [ ] Include the 15 self-authored real-service questions and actual prompts/conversation excerpts required by the assignment. The five questions currently included are only the retrieval-comparison set.
- [ ] Verify the four manual answer grades against actual answer text and source passages.
- [ ] Add official Groq limit documentation and exact observed error details only if captured. Do not invent numerical quotas.
- [ ] Label stand-in values as simulated.
- [ ] Describe the overload test as concurrent overload, not time-based sustained traffic.

## Security
- [ ] Ensure `.env` is listed in `.gitignore`.
- [ ] Search the repository for API keys before publishing.
- [ ] Revoke any key exposed in chat, terminal screenshots or Git history.
- [ ] Never include `.env` in GitHub or Drive.

## Final review
- [ ] Confirm the report is no more than two pages after PDF export.
- [ ] Confirm all arXiv version identifiers match the assignment.
- [ ] Confirm no fabricated metrics, prompts, citations or API limits are included.
