# Siamese Transformer Address Matching Animation

A [Manim](https://www.manim.community/) animation visualizing the **Siamese Transformer architecture** for address matching using a Bi-encoder + Cross-encoder pipeline.

## 📺 Overview

This animation demonstrates a three-phase address matching system:

1. **Database Pre-Embedding** — Addresses are encoded via a Bi-Encoder into embeddings and partitioned into 9 auxiliary databases
2. **Predicting Module** — Un-normalized input addresses are encoded and matched against candidates using cosine similarity search
3. **Re-Ranking Module** — Top candidates are re-ranked to find the best match, achieving **95.3% door accuracy**

## 🛠️ Setup

### Prerequisites

- Python 3.11+
- Conda (recommended)

### Installation

```bash
# Create environment from file
conda env create -f environment.yml

# Activate environment
conda activate manim_stable
```

## ▶️ Rendering

```bash
# Preview (low quality)
manim -pql --renderer=cairo address_matching.py AddressMatchingArchitecture

# High quality render
manim -pqh --renderer=cairo address_matching.py AddressMatchingArchitecture

# Production quality (4K)
manim -pqk --renderer=cairo address_matching.py AddressMatchingArchitecture
```

## 📁 Project Structure

```
manim/
├── address_matching.py    # Main animation scene
├── environment.yml        # Conda environment specification
├── media/                 # Rendered output directory
└── README.md
```

## 🎨 Customization

Key configuration options at the top of `address_matching.py`:

| Variable | Description |
|----------|-------------|
| `BI_ENCODER_COLOR` | Color for bi-encoder boxes |
| `CROSS_ENCODER_COLOR` | Color for cross-encoder boxes |
| `BACKGROUND_COLOR` | Scene background color |
| `CLEAN_FONT` | Font used for text elements |
