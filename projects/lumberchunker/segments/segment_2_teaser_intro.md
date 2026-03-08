<!-- IMAGE: crown_figure_blog.png -->

LumberChunker lets an LLM decide where a long story should be split, creating more natural chunks that help Retrieval Augmented Generation (RAG) systems retrieve the right information.

## Introduction

Long-form narrative documents usually have an explicit structure, such as chapters or sections, but these units are often too broad for retrieval tasks. At a lower level, important semantic shifts happen inside these larger segments without any visible structural break. When we split text only by formatting cues, like paragraphs or fixed token windows, passages that belong to the same narrative unit may be separated, while unrelated content can be grouped together. This misalignment between structure and meaning produces chunks that contain incomplete or mixed context, which reduces retrieval quality and affects downstream RAG performance. For this reason, segmentation should aim to create chunks that are semantically independent, rather than relying only on document structure.

**So how do we preserve the story's flow and still keep chunking practical?**

In many cases, a reader can easily recognize where the narrative begins to shift—for example, when the text moves to a different scene, introduces a new entity, or changes its objective. The difficulty is that most automated chunking methods do not consider this semantic signal and instead rely only on surface structure. As a result, they may produce segmentations that look reasonable from a formatting perspective but break the underlying narrative coherence.

To make this concrete, consider the short passage below and decide the optimal chunking boundary!

## The LumberChunker Method

In the example above, Option C provides the most coherent segmentation. The boundary aligns with the point where the narrative becomes semantically independent from the preceding context.

Our goal is to make this type of segmentation decision practical at scale. The challenge is that human-quality boundary detection requires understanding narrative context, which is expensive to apply across thousands of paragraphs in long-form documents.
