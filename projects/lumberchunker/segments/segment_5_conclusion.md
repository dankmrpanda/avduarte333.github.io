### A Sweet Spot Around θ ≈ 550 Tokens

We sweep `θ ∈ [450, 1000]` tokens and find that **θ ≈ 550** consistently maximizes retrieval quality: large enough for context, small enough to keep the model focused on the current turn in the story.

This does not mean the resulting chunks are large. In practice, as the table shows, the average chunk size is about **334 tokens**, which suggests that LumberChunker often detects earlier semantic shifts within the window.

## Conclusion

LumberChunker reframes document chunking as a semantic boundary detection problem. Instead of relying on fixed token limits or surface structure, it uses a rolling context window to identify the earliest point where the meaning of the text becomes independent from what came before, producing segments that better align with the underlying narrative structure.

On the GutenQA benchmark, LumberChunker consistently improves retrieval and downstream QA over traditional fixed-size and recursive methods, approaching the quality of manual, human-curated segmentations.

These results suggest that segmentation is not just a preprocessing step, but a core design choice for retrieval systems. By creating semantically independent chunks, LumberChunker provides a practical way to improve how long-form documents are retrieved and used in RAG pipelines.

## Citation

If you find LumberChunker useful in your research, please consider citing:

```bibtex
@inproceedings{duarte-etal-2024-lumberchunker,
    title = "{L}umber{C}hunker: Long-Form Narrative Document Segmentation",
    author = "Duarte, Andr{\'e} V.  and Marques, Jo{\~a}o DS  and Gra{\c{c}}a, Miguel  and Freire, Miguel  and Li, Lei  and Oliveira, Arlindo L.",
    editor = "Al-Onaizan, Yaser  and Bansal, Mohit  and Chen, Yun-Nung",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2024",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.findings-emnlp.377/",
    doi = "10.18653/v1/2024.findings-emnlp.377",
    pages = "6473--6486",
    abstract = "LumberChunker reframes document chunking as a semantic boundary detection problem..."
}
```

---

Blog created by Raymond Jiang and André Duarte

This website is licensed under a [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Website template adapted from [Nerfies](https://github.com/nerfies/nerfies.github.io).
