# 🛡️ FairAI LiveGuard
**Enterprise AI Governance & Bias Prevention Platform**

> "We built a real-time AI firewall that prevents biased decisions before they impact real people."

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit dashboard
```bash
streamlit run app.py
```

### 3. (Optional) Run the FastAPI bias firewall
```bash
uvicorn api:app --reload
```
Then open http://localhost:8000/docs for the interactive API docs.

---

## 📂 Project Structure

```
FairAI_LiveGuard/
│
├── app.py            ← Streamlit dashboard (main entry point)
├── api.py            ← FastAPI REST API (Bias Firewall endpoint)
│
├── model.py          ← ML model training & prediction
├── fairness.py       ← Fairness metrics (Demographic Parity, etc.)
├── interceptor.py    ← Bias Firewall logic
├── database.py       ← SQLite decision logging
├── simulation.py     ← Counterfactual / what-if simulation
├── report.py         ← PDF compliance report generator
│
├── data/
│   └── sample.csv    ← Sample hiring dataset
│
├── logs/             ← Auto-created, stores fairai.db
│
└── requirements.txt
```

---

## 🔥 Features

| Feature | Description |
|---|---|
| ⚡ Bias Firewall | Blocks biased AI decisions in real-time |
| ⚖️ Fairness Metrics | Demographic Parity Difference via Fairlearn |
| 👤 Human Override | Admin can approve blocked decisions |
| 🔁 Scenario Simulator | What-if counterfactual analysis |
| 📊 Audit Logs | Full SQLite decision log with export |
| 🧾 Compliance Report | PDF report for regulators/auditors |
| 🌐 REST API | FastAPI endpoint for external integration |

---

## 🌐 API Usage (FastAPI)

### POST /predict
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"age": 30, "gender": 0, "income": 25000}}'
```

**Response (BLOCKED):**
```json
{
  "status": "BLOCKED",
  "prediction": null,
  "fairness_score": 0.3,
  "message": "Biased decision intercepted."
}
```

**Response (APPROVED):**
```json
{
  "status": "APPROVED",
  "prediction": 1,
  "fairness_score": 0.05,
  "message": "Decision passed fairness check."
}
```

---

## 💰 Business Model

| Tier | Price | Features |
|---|---|---|
| Free | $0 | 100 req/day, basic dashboard |
| Pro | $20–50/mo | Full dashboard, bias reports, logs |
| Enterprise | $500+/mo | API, compliance reports, custom rules |

---

## 🎯 Target Customers
- Fintech / lending companies
- Hiring & recruitment platforms
- Healthcare AI systems
- Government / public sector AI

---

## 🏆 Hackathon Pitch Line
**"We built a real-time AI firewall that prevents biased decisions before they impact real people."**

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit, Matplotlib
- **Backend:** FastAPI, Python
- **AI / Fairness:** Scikit-learn, Fairlearn
- **Database:** SQLite (upgrade to PostgreSQL for production)
- **Deployment:** AWS / Google Cloud / Heroku

---

## 📈 Roadmap
- [ ] React frontend
- [ ] PostgreSQL + cloud deployment
- [ ] Auth system (JWT)
- [ ] Deep learning bias detection
- [ ] Multi-model support
- [ ] Slack / email alerts
