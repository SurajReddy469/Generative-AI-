# Week 5: Token Economics – Cost and Rate-Limit Budgeting Before Building an LLM Feature

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Economics](https://img.shields.io/badge/FinOps-Token%20Economics-2E7D32?style=flat)]()
[![pytest](https://img.shields.io/badge/Testing-pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)](https://pytest.org/)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat)]()

## Aim
To design and implement a pre-deployment mathematical budgeting engine for Generative AI applications. The tool forecasts daily and monthly token consumption, models API financial costs, evaluates traffic surges against provider RPM (Requests Per Minute) and TPM (Tokens Per Minute) quotas with custom safety margins, and generates a structured Go / No-Go deployment recommendation.

---

## Mathematical Formulation

Let:
- $R$ = Expected requests per day
- $I$ = Average input tokens per request
- $O$ = Average output tokens per request
- $P_i$ = Input token price per 1,000,000 tokens (USD)
- $P_o$ = Output token price per 1,000,000 tokens (USD)
- $M = 1 + \frac{\text{Safety Margin } \%}{100}$

$$\text{Input Tokens/Day} = R \times I$$
$$\text{Output Tokens/Day} = R \times O$$
$$\text{Total Tokens/Day} = R \times (I + O)$$
$$\text{Daily Cost (USD)} = \frac{(R \times I \times P_i) + (R \times O \times P_o)}{1,000,000}$$
$$\text{Monthly Cost (USD)} = \text{Daily Cost} \times 30$$
$$\text{Peak RPM (with Margin)} = \text{Peak Requests/Minute} \times M$$
$$\text{Peak TPM (with Margin)} = \text{Peak Requests/Minute} \times (I + O) \times M$$

---

## Project Structure
```text
week5/
├── .env.example       # Template for traffic assumptions and price ceilings
├── .env               # Local assumptions (git-ignored)
├── .gitignore         # Ignores .env and test caches
├── budget.py          # FeatureBudget dataclass and economic calculation engine
├── test_budget.py     # Automated unit test suite verifying capacity & pricing
├── requirements.txt   # Dependencies (python-dotenv, pytest)
└── README.md          # Week 5 guide
```

---

## How to Run Week 5

### Step 1: Install Dependencies
From the repository root (or within `week5/`):
```powershell
pip install -r week5/requirements.txt
```

### Step 2: Configure Planning Assumptions in `.env`
Copy `.env.example` to `.env`:

**PowerShell (Windows):**
```powershell
Copy-Item week5\.env.example week5\.env
```

**Bash (Linux / macOS):**
```bash
cp week5/.env.example week5/.env
```

Review or modify `week5/.env`:
```env
# All prices are USD per 1,000,000 tokens
INPUT_PRICE_PER_MILLION=0.30
OUTPUT_PRICE_PER_MILLION=1.20
REQUESTS_PER_DAY=2000
AVG_INPUT_TOKENS=1200
AVG_OUTPUT_TOKENS=300
PEAK_REQUESTS_PER_MINUTE=30

# Rate limits & financial budget thresholds
RPM_LIMIT=60
TPM_LIMIT=100000
MONTHLY_BUDGET_USD=50
DAILY_BUDGET_USD=2
SAFETY_MARGIN_PERCENT=20
```

### Step 3: Run Automated Unit Tests
Verify that boundary conditions, over-budget detection, and capacity checks pass:

```powershell
# From repository root
pytest week5/test_budget.py -v

# Or using unittest
python -m unittest week5/test_budget.py
```

### Step 4: Run the Budget Planner

#### Option A: Run directly from Repository Root (Recommended)
```powershell
python week5/budget.py
```

#### Option B: Run from inside `week5/`
```powershell
cd week5
python budget.py
```

---

## Expected Output

```text
TOKEN ECONOMICS REPORT
-----------------------------------
Input tokens/day:  2,400,000
Output tokens/day: 600,000
Total tokens/day:  3,000,000
Estimated daily cost:   $1.4400
Estimated monthly cost: $43.20
Peak RPM with margin: 36.0
Peak TPM with margin: 54,000

CHECKS
RPM capacity: PASS
TPM capacity: PASS
Daily budget: PASS
Monthly budget: PASS

Recommendation: WITHIN configured planning limits.
```

---

## What-If Sensitivity Matrix

| Scenario | Parameter Altered | Engineering Impact | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **User Base Growth** | Increase `REQUESTS_PER_DAY` | Total cost scales linearly; daily budget threshold may breach. | Apply caching for frequent queries or introduce tiered rate limits. |
| **Larger Context Prompts** | Increase `AVG_INPUT_TOKENS` | Substantial input cost and peak TPM increase. | Truncate conversation history or use vector search (RAG) to narrow context. |
| **Verbose Model Responses**| Increase `AVG_OUTPUT_TOKENS` | Output token generation is 4x more expensive than input on most models. | Constrain `max_output_tokens` or enforce concise system prompts. |
| **Sudden Traffic Spike** | Increase `PEAK_REQUESTS_PER_MINUTE` | RPM / TPM capacity limits fail against provider quotas. | Introduce queueing (e.g. Celery / Redis) with client backpressure. |
| **Model Migration** | Switch `INPUT/OUTPUT_PRICE` | Direct financial variance without changing architecture. | Benchmark cost vs quality trade-offs (e.g. Flash-Lite vs Pro). |

---

## Troubleshooting

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| `ValueError: Usage assumptions cannot be negative` | A parameter in `.env` was entered as negative | Ensure all token counts, prices, and requests are $\ge 0$. |
| `AssertionError: False is not True` during test | A modified test parameter triggered an intentional boundary failure | Review test inputs against configured limits in `test_budget.py`. |
