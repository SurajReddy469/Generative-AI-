# Week 6: Golden Question Set Evaluation & Baseline Run (Release v0.1)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Evaluation](https://img.shields.io/badge/Evaluation-Golden%20Set%20Benchmark-blueviolet?style=flat)]()
[![Ollama](https://img.shields.io/badge/Model-Llama%203.2-black?style=flat&logo=ollama&logoColor=white)](https://ollama.ai/)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat)]()

## Aim
To establish an automated, reproducible LLM evaluation baseline (**Release v0.1**). The evaluation engine prompts a local `llama3.2` model with a curated **Golden Question Set** of 30 technical Generative AI questions, scores responses against expected domain keywords, and logs detailed outcomes to `baseline_results.csv`.

---

## Evaluation Workflow

```mermaid
flowchart TD
    A["golden_set.json (30 Questions)"] --> B["Evaluation Engine (main.py)"]
    B -->|Prompt (temp=0)| C["Local Ollama (llama3.2)"]
    C -->|Response Text| B
    B --> D["Keyword Coverage Scoring"]
    D -->|Score >= 60%| E["Status: PASS"]
    D -->|Score < 60%| F["Status: REVIEW"]
    E & F --> G["baseline_results.csv"]
    G --> H["Summary Metrics & Dashboard Print"]
```

---

## Prerequisites
- **Python 3.10+**
- **Ollama**: Installed and running at `http://localhost:11434`.
- **Model Download**:
  ```powershell
  ollama pull llama3.2
  ```

---

## Project Structure
```text
week6/
├── .gitignore            # Ignores .venv and cache
├── baseline_results.csv  # Auto-generated CSV containing per-question metrics
├── golden_set.json       # 30 curated benchmark questions with expected answers & keywords
├── main.py               # Evaluation runner and scoring script
├── requirements.txt      # Dependencies (requests)
└── README.md             # Week 6 guide
```

---

## Golden Question Set Breakdown

The 30 questions in `golden_set.json` span foundational and advanced Generative AI concepts:
1. **Tokenization & Encodings**: BPE, WordPiece, SentencePiece, byte fallbacks, vocabulary size.
2. **Transformer Architecture**: Self-attention, multi-head attention, KV cache, feed-forward layers, positional encodings (RoPE).
3. **Sampling & Decoding**: Temperature scaling, top-$k$, top-$p$ (nucleus), greedy decoding.
4. **Context Windows & Attention**: Quadratic complexity, chunking, sliding windows, memory footprint.
5. **Fine-Tuning & Adaptation**: Full fine-tuning, LoRA, QLoRA, parameter efficiency.
6. **Alignment & Safety**: RLHF, DPO, prompt injection, hallucinations.

---

## How to Run Week 6

### Step 1: Confirm Ollama is Running
Ensure the Ollama service is active and `llama3.2` is present:
```powershell
ollama list
```
*(If missing, run `ollama pull llama3.2`)*

### Step 2: Install Dependencies
From the repository root (or within `week6/`):
```powershell
pip install -r week6/requirements.txt
```

### Step 3: Execute the Baseline Evaluation

#### Option A: Run directly from Repository Root (Recommended)
```powershell
python week6/main.py
```

#### Option B: Run from inside `week6/`
```powershell
cd week6
python main.py
```

---

## Expected Output & Summary Report

As each question is evaluated, the terminal prints live progress:
```text
======================================
GOLDEN QUESTION SET
======================================
Total Questions: 30
Model: llama3.2

--------------------------------------
Question 1: Q001
Question: What is Byte Pair Encoding (BPE) and how does it work?

LLM Answer:
Byte Pair Encoding (BPE) is a subword tokenization algorithm that iteratively replaces the most frequent pair of consecutive bytes or characters with a new symbol...
Keywords: ['subword', 'frequency', 'iterative', 'compression']
Matched Keywords: ['subword', 'frequency', 'iterative']
Missing Keywords: ['compression']
Score: 75.0%
Status: PASS

...

======================================
BASELINE SUMMARY REPORT (Release v0.1)
======================================
Model: llama3.2
Total Questions: 30
Passed: 27
Need Review: 3
Average Score: 84.17%
Results exported to baseline_results.csv
```

---

## Output CSV Schema (`baseline_results.csv`)

| Column Header | Description | Example |
| :--- | :--- | :--- |
| `Question_ID` | Unique question code | `Q001` |
| `Question` | Prompt sent to LLM | `What is BPE?` |
| `Expected_Answer` | Reference answer | Subword compression algorithm... |
| `LLM_Answer` | Generated output from `llama3.2` | Full response string |
| `Matched_Keywords` | Keywords found in response | `subword, frequency, iterative` |
| `Missing_Keywords` | Keywords absent in response | `compression` |
| `Score` | Keyword coverage percentage | `75.0` |
| `Status` | Performance category | `PASS` or `REVIEW` |
| `Model` | Target model tested | `llama3.2` |
| `Release` | Dataset version tag | `v0.1` |

---

## Troubleshooting

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| `requests.exceptions.ConnectionError: HTTPConnectionPool` | Ollama daemon is offline | Launch Ollama using `ollama serve` or open the Ollama desktop app. |
| `HTTP 404: model 'llama3.2' not found` | The model is not installed locally | Run `ollama pull llama3.2` in your terminal. |
| Evaluation feels slow | Model running on CPU | Ensure GPU acceleration is available for Ollama if running on hardware with NVIDIA/AMD/Apple Silicon. |
