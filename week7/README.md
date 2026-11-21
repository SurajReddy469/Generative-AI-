# Week 7: Next-Token Probabilities, Logits & Decoding

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?style=flat&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-FFD21E?style=flat&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![Model](https://img.shields.io/badge/Model-GPT--2%20(124M)-lightgrey?style=flat)]()
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat)]()

## Aim
To implement an interactive deep-dive into the token generation pipeline of an autoregressive language model (`openai-community/gpt2`). The tool demonstrates how input text is tokenized into subword IDs, how unnormalized logits across all 50,257 vocabulary tokens are generated during the model's forward pass, how temperature scaling reshapes the distribution via Softmax, and logs top-$k$ predictions to CSV.

---

## The Generation Pipeline

```mermaid
flowchart LR
    A["Input Text: 'The capital of France is'"] --> B["Stage 1: Tokenization\n(BPE Subwords -> IDs)"]
    B --> C["Stage 2: Model Forward Pass\n(Logits Vector z ∈ ℝ^50257)"]
    C --> D["Stage 3: Temperature Scaling\ns_i = z_i / T"]
    D --> E["Stage 4: Softmax Normalization\nP(w_i) = exp(s_i) / Σ exp(s_j)"]
    E --> F["Stage 5: Top-K Extraction & Visual Bars"]
    F --> G["CSV Output: gpt2_next_token_results.csv"]

    style A fill:#1e293b,stroke:#3b82f6,color:#f8fafc
    style C fill:#1e293b,stroke:#a855f7,color:#f8fafc
    style E fill:#1e293b,stroke:#10b981,color:#f8fafc
    style G fill:#1e293b,stroke:#eab308,color:#f8fafc
```

---

## Mathematical Formulation

1. **Unnormalized Model Scores (Logits)**:
   For a vocabulary $V$ (size 50,257 for GPT-2), the final linear layer outputs raw logits:
   $$\mathbf{z} = [z_1, z_2, \dots, z_{|V|}]$$

2. **Temperature Scaling ($T$)**:
   The logits are scaled by a positive temperature parameter $T > 0$:
   $$s_i = \frac{z_i}{T}$$

3. **Softmax Probability Normalization**:
   $$P(w_i) = \frac{e^{s_i}}{\sum_{j=1}^{|V|} e^{s_j}} = \frac{e^{z_i / T}}{\sum_{j=1}^{|V|} e^{z_j / T}}$$

4. **Temperature Dynamics**:
   - **Low Temperature ($T < 1.0$, e.g. $T = 0.3$):** Sharpens differences in logits; probability collapses onto the top candidate (greedy, deterministic).
   - **Baseline ($T = 1.0$):** Standard unmodified Softmax distribution.
   - **High Temperature ($T > 1.0$, e.g. $T = 1.5$):** Flattens the distribution; lower-ranked tail tokens gain higher relative likelihood (creative, diverse, exploratory).

---

## Prerequisites
- **Python 3.10+**
- **PyTorch** (CPU or CUDA-enabled):
  ```powershell
  pip install torch --index-url https://download.pytorch.org/whl/cpu
  ```
- **Hugging Face Transformers**:
  ```powershell
  pip install transformers
  ```

---

## Project Structure
```text
week7/
├── .gitignore                    # Ignores .venv, cache, and CSV results
├── gpt2_next_token_results.csv   # Auto-generated CSV recording prompt runs
├── main.py                       # Interactive next-token distribution analyzer
├── requirements.txt              # Dependencies (torch, transformers)
└── README.md                     # Week 7 guide
```

---

## How to Run Week 7

### Step 1: Install Dependencies
From the repository root (or within `week7/`):
```powershell
pip install -r week7/requirements.txt
```
*(On machines without an NVIDIA GPU, installing the CPU wheel via `pip install torch --index-url https://download.pytorch.org/whl/cpu` is recommended).*

### Step 2: Run the Interactive Tool

#### Option A: Run directly from Repository Root (Recommended)
```powershell
python week7/main.py
```

#### Option B: Run from inside `week7/`
```powershell
cd week7
python main.py
```

---

## Sample Interaction & Live Output

```text
Loading openai-community/gpt2 into memory... (Please wait a few seconds)
Model ready! Results will be saved to 'gpt2_next_token_results.csv'.

Enter prompt (or type 'exit' to quit): The capital of France is
Enter top-k candidates to display [default = 6]: 5
Enter temperature [default = 1.0]: 0.7

==================================================================================
PROMPT: "The capital of France is" | TOP-K: 5 | TEMPERATURE: 0.7
==================================================================================

[STAGE 1] INPUT TOKENIZATION (Text -> Subword IDs)
----------------------------------------------------------------------------------
  Pos 0  | ID: 464    | Token: 'The'
  Pos 1  | ID: 3139   | Token: ' capital'
  Pos 2  | ID: 286    | Token: ' of'
  Pos 3  | ID: 4881   | Token: ' France'
  Pos 4  | ID: 318    | Token: ' is'

[STAGE 2] RAW MODEL SCORES (Logits across all 50,257 vocabulary tokens)
----------------------------------------------------------------------------------
  Min Logit : -11.9542   |   Max Logit : 14.8213

[STAGE 3] TOP-5 NEXT-TOKEN CANDIDATES (After Temperature & Softmax)
----------------------------------------------------------------------------------
Rank  | ID      | Candidate        | Raw Logit  | Scaled    | Prob (%)  | Visual Bar
----------------------------------------------------------------------------------
#1    | 6342    | ' Paris'         |   14.8213  |  21.1733  |   78.43%  | ███████████████████████
#2    | 262     | ' the'           |   11.4510  |  16.3586  |    6.34%  | █
#3    | 319     | ' also'          |   10.8711  |  15.5301  |    2.78%  | 
#4    | 7062    | ' home'          |   10.4201  |  14.8859  |    1.45%  | 
#5    | 257     | ' a'             |   10.1190  |  14.4557  |    0.95%  | 
----------------------------------------------------------------------------------
Cumulative Probability of Top-5: 89.95% | Remaining 50,252 tokens: 10.05%
Saved 5 rows to 'gpt2_next_token_results.csv'
==================================================================================
```

---

## CSV Export Format (`gpt2_next_token_results.csv`)

Every run is automatically appended with `utf-8-sig` encoding (fully readable in Excel):

| Prompt | Temperature | Rank | Token ID | Candidate Token | Raw Logit | Scaled Logit | Probability (%) |
| :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: |
| `The capital of France is` | 0.7 | 1 | 6342 | `' Paris'` | 14.8213 | 21.1733 | 78.43 |
| `The capital of France is` | 0.7 | 2 | 262 | `' the'` | 11.4510 | 16.3586 | 6.34 |
| `The capital of France is` | 0.7 | 3 | 319 | `' also'` | 10.8711 | 15.5301 | 2.78 |

---

## Troubleshooting

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| `No module named 'torch'` | PyTorch is not installed in `.venv` | Install PyTorch CPU: `pip install torch --index-url https://download.pytorch.org/whl/cpu`. |
| `HFValidationError / Download lock` | Corrupted cache lock files from interrupted download | Clear lock files in `~/.cache/huggingface/hub/models--openai-community--gpt2/` and re-run. |
| Memory spikes on low-RAM systems | GPT-2 model size (~500 MB) | GPT-2 (124M parameters) comfortably runs within 1 GB RAM; close unused applications if running on memory-constrained systems. |
