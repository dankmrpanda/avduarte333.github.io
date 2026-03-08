<!-- IMAGES: great_gatsby.jpeg, pride_and_prejudice.jpeg, moby_dick.jpeg, frankenstein.jpeg -->

## Key Findings

### Retrieval: LumberChunker leads ⭐

LumberChunker leads across both DCG@k and Recall@k. By `k=20`, it reaches **DCG ≈ 62.1%** and **Recall ≈ 77.9%**, showing that better segmentation improves not only which passages appear first, but also how reliably the right context is retrieved.

### Downstream QA: Targeted Retrieval Outperforms Large Context Windows

We find that even with very large context windows, a non-retrieval setup still performs worse than RAG, showing that selecting focused, relevant passages is more effective than simply increasing the amount of raw context. Under this setting, when integrated into a standard RAG pipeline on a GutenQA subset, our **RAG-LumberChunker** is second only to **RAG-Manual**, which uses hand-segmented ground-truth chunks.
