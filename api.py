from fastapi import FastAPI
from pydantic import BaseModel
from interceptor import intercept_decision
import numpy as np

app = FastAPI(title="FairAI LiveGuard API Gateway")

class ModelRequest(BaseModel):
    features: dict
    fairness_score: float = 0.2
    threshold: float = 0.15

@app.post("/verify")
async def verify_decision(req: ModelRequest):
    """
    Enterprise API endpoint to verify AI decisions in real-time.
    """
    # Mock prediction logic for API demo
    prediction = np.random.choice([0, 1])
    status = intercept_decision(prediction, req.fairness_score, req.threshold)
    
    return {
        "status": status,
        "prediction": int(prediction) if status == "APPROVED" else None,
        "bias_risk": "HIGH" if status == "BLOCKED" else "LOW",
        "action_required": "Human Review" if status == "BLOCKED" else "Proceed"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
