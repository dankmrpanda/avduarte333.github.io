**LumberChunker** approaches this by treating segmentation as a boundary-finding problem: given a short sequence of consecutive paragraphs, we ask a language model to identify the earliest point where the content clearly shifts. This formulation allows segments to vary in length while remaining aligned with the underlying narrative structure. In practice, LumberChunker consists of these steps:

### 1) Document Paragraph Extraction

Cleanly split the book into paragraphs and assign stable IDs (`ID:1, ID:2, …`). This preserves the document's natural discourse units and gives us safe candidate boundaries.

> **Example:** From a novel, we extract:
>
> `ID:1` "The morning sun filtered through the dusty windows..."
> `ID:2` "She walked slowly to the door, hesitating..."
> `ID:3` "Meanwhile, across town, Detective Morrison reviewed the case files..."
> `ID:4` "The previous night's events had left him puzzled..."
>
> Each paragraph gets a unique ID for tracking boundaries.

### 2) IDs Grouping for LLM

Build a group `G_i` by appending paragraphs until the group's length reaches a token budget `θ`. This provides enough context for the model to judge when a topic/scene actually shifts.

> **Example:** With `θ = 550` tokens, we build, per example:
>
> `G_1` = [`ID:1`, `ID:2`, `ID:3`, `ID:4`, `ID:5`, `ID:6`]
>
> This window, by spanning multiple paragraphs, increases the chance that at least one meaningful narrative shift is present within the context.

### 3) LLM Query

Prompt the model with the paragraphs in `G_i` and ask it to return the *first paragraph where content clearly changes relative to what came before*. Use that returned ID as the chunk boundary; start the next group at that paragraph and repeat to the end of the book.

> **Example:** Given `G_1` = [`p1`, `p2`, `p3`, `p4`, `p5`, `p6`], the LLM responds: `p3`
>
> **Answer Extraction:**
> We extract `p3` as the boundary. This creates:
> - **Chunk 1**: [`p1`, `p2`]
> - **Next group (`G_2`) starts at** `p3`

## GutenQA: A Benchmark for Long-Form Narrative Retrieval

To evaluate our chunking approach, we introduce [**GutenQA**](https://huggingface.co/datasets/LumberChunker/GutenQA), a benchmark of **100** carefully cleaned public-domain books paired with **3,000** needle-in-a-haystack type of questions. This allows us to measure retrieval quality directly and then observe how better retrieval leads to more accurate answers in a RAG system.
