# Week 4: Tokenizer Lab – BPE vs. WordPiece vs. SentencePiece

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-FFD21E?style=flat&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![NLP](https://img.shields.io/badge/NLP-Subword%20Tokenization-FF6F00?style=flat)]()
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat)]()

## Aim
To evaluate and compare three major subword tokenization algorithms—**Byte Pair Encoding (BPE)**, **WordPiece**, and **SentencePiece**—across three distinct natural languages (**English**, **Telugu**, and **Hindi**), observing subword fragmentation, tokenizer fertility rate, and byte-level fallback behaviors.

---

## Algorithms & Models Evaluated

| Tokenizer Algorithm | Model Implementation | Primary Design & Subword Prefix |
| :--- | :--- | :--- |
| **Byte Pair Encoding (BPE)** | `openai-community/gpt2` | Byte-level BPE, Latin/English-optimized, uses `Ġ` to indicate leading spaces |
| **WordPiece** | `bert-base-multilingual-cased` | Greedy longest-match tokenization, uses `##` to denote subword continuation |
| **SentencePiece** | `xlm-roberta-base` | Language-agnostic Unigram model, treats space as regular symbol ` ` |

---

## Project Structure
```text
week4/
├── .gitignore               # Ignores .venv, cache, and checkpoints
├── requirements.txt         # Dependencies (transformers, sentencepiece)
├── tokenizer_comparison.py  # Benchmark script executing all 3 tokenizers
└── README.md                # Week 4 guide
```

---

## How to Run Week 4

### Step 1: Install Dependencies
From the repository root (or within `week4/`):
```powershell
pip install -r week4/requirements.txt
```
> [!NOTE]
> `sentencepiece` is required by XLM-RoBERTa for loading the Unigram vocabulary.

### Step 2: Run the Benchmark Script

#### Option A: Run directly from Repository Root (Recommended)
```powershell
python week4/tokenizer_comparison.py
```

#### Option B: Run from inside `week4/`
```powershell
cd week4
python tokenizer_comparison.py
```

---

## Benchmark Results & Empirical Findings

| Language | Input Sentence | BPE (GPT-2) | WordPiece (mBERT) | SentencePiece (XLM-R) |
| :--- | :--- | :---: | :---: | :---: |
| **English** | *Artificial intelligence is changing the world.* | **8** | 10 | 10 |
| **Telugu** | *కృత్రిమ మేధస్సు ప్రపంచాన్ని మారుస్తోంది.* | 112 | 18 | **14** |
| **Hindi** | *कृत्रिम बुद्धिमत्ता दुनिया को बदल रही है।* | 68 | 17 | **14** |

### Key Observations & Insights:
1. **English Parity**:
   All three tokenizers segment English text efficiently (8–10 tokens) with minimal fertility because English is heavily represented in their training corpora.
2. **The "Indic Token Tax" in GPT-2 BPE**:
   GPT-2's vocabulary does not contain pre-merged subwords for Telugu and Hindi scripts. As a result, it falls back to raw UTF-8 bytes (`à`, `°`, `ķ`...), generating **112 tokens for an 4-word Telugu sentence** (a fertility rate exceeding 25x).
3. **Multilingual Synergy in WordPiece and SentencePiece**:
   Both Multilingual BERT and XLM-RoBERTa include dedicated Indic vocabulary subwords, consolidating complex conjunct consonants into 14–18 tokens and drastically reducing compute and latency costs for non-English languages.

---

## Troubleshooting

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| `ImportError: SentencePiece is required` | The `sentencepiece` library is missing from the environment | Run `pip install sentencepiece` or `pip install -r week4/requirements.txt`. |
| `HTTPSConnectionPool / Hugging Face Timeout` | Initial download of tokenizer configs was interrupted | Ensure internet access is active. Hugging Face caches files automatically in `~/.cache/huggingface/hub/`. |
