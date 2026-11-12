# The Relay — Reliability Evaluation of a Retrieval-Augmented LLM Pipeline

## 1. System Design
The Relay is a Python retrieval-augmented question-answering pipeline over three arXiv papers: *Attention Is All You Need* (1706.03762v7), *Moshi: A Speech-Text Foundation Model* (2410.00037v1), and *Dynamic Chunking for End-to-End Hierarchical Sequence Modeling* (2507.07955v2). PDF ingestion produced 412 text chunks. Retrieval uses TF-IDF with unigram/bigram features and cosine similarity. Retrieved passages are sent to Groq model `openai/gpt-oss-20b`; responses are streamed and logged. A local stand-in simulates delays, failures, rate limits, load slowdown and budget exhaustion.

## 2. Real Service Evaluation
Fifteen Groq requests were attempted: four succeeded and eleven were rate-limited. No retries were performed. Among four successful requests, first-token latency was p50 620.23 ms and p95 859.69 ms; total latency was p50 905.47 ms and p95 1,107.62 ms. These percentiles are preliminary because the successful sample contains only four requests. The tests confirmed rate limiting but did not establish exact numerical per-minute or daily quota limits. CSV token counts for streamed requests are approximate word-count proxies, not actual provider token counts.

## 3. Stand-in Evaluation
| Scenario | Requests | Successful | Rate-limited |
|---|---:|---:|---:|
| Steady | 10 | 10 | 0 |
| Burst | 15 | 5 | 10 |
| Concurrent overload | 20 | 5 | 15 |
| Per-minute limit halved | 6 | 2 | 4 |
| Daily budget exhausted | 6 | 3 | 3 |

The stand-in completed all steady-traffic requests. It reproduced selected failure patterns using configured delays and simulated limits. Its latency values are simulated estimates, not measurements of Groq infrastructure. The overload test used 20 concurrent requests, not a time-based sustained arrival pattern.

## 4. Retrieval Quality and Cost
Five questions were tested with top-3, top-5 and top-8 retrieval, for 15 comparisons.

| Configuration | Avg. retrieval latency | Avg. context words | Expected-paper match ratio |
|---|---:|---:|---:|
| Top-3 | 3.89 ms | 503 | 0.800 |
| Top-5 | 4.17 ms | 809 | 0.800 |
| Top-8 | 3.91 ms | 1,248 | 0.804 |

Top-8 produced only a marginal increase in expected-paper matching while substantially increasing context size. Top-5 is a practical compromise in this small test. Expected-paper ratio only measures whether a retrieved chunk belongs to the expected paper; it does not establish passage-level semantic relevance or answer correctness.

Three ways a naive retriever can mislead:
1. Lexical mismatch: different wording can cause relevant passages to be missed.
2. Irrelevant extra context: increasing top-k can introduce chunks from unrelated papers.
3. False confidence: a chunk can come from the expected paper without answering the question.

## 5. Limits, Failure Handling and User Experience
The current implementation records rate-limited requests and performed no automatic retries in these experiments. A production implementation should use bounded exponential backoff, avoid retry loops and clearly explain temporary service unavailability. When a daily budget is exhausted, the user should receive a clear limit message rather than an invented answer; local retrieval-only fallback or cached material can be offered where appropriate. The daily-budget scenario is simulated and does not establish Groq's actual reset behaviour. Cost per 1,000 answers was not calculated because complete provider token usage and applicable pricing were not collected.

## 6. Evaluation, Limitations and Learning
Four successful real answers were manually graded: three received grade 2 (correct) and one received grade 1 (partially correct), on a 0–2 scale. Eleven real requests were rate-limited and could not be graded. This is too small a sample for a general accuracy claim. The experiments show that retrieval quality, context size and service availability must be evaluated separately. Further work should include more manually labelled questions, passage-level relevance judgements, repeated latency tests and actual provider token accounting.

## 7. Feedback on Vaani and Reflection
The assignment was useful because it required measurement of the complete pipeline rather than model answers alone. It highlighted rate-limit handling, retrieval quality, latency and honest reporting of missing data. Clearer guidance on evaluation labels, provider quota documentation and the distinction between simulated and measured metrics would improve reproducibility.

**Evidence note:** Aggregated metrics are based on terminal outputs supplied during development. The original `results/results.csv` is included in the repository. PDF inputs and generated `data/chunks.json` are reproducible using the download and ingestion scripts.
