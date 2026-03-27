from fastapi import FastAPI

from data_loader import load_and_preprocess
from signal_report import generate_signal_report
from decision_logic import DecisionLogic
from ml_model import predict_score

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Decision Intelligence API Running"}


@app.get("/analyze")
def analyze():
    # Load data
    version_A, version_B, _ = load_and_preprocess("system_metrics.csv")

    # Generate signals
    signal_report = generate_signal_report(version_A, version_B)

    # Decision
    decision = DecisionLogic(signal_report).evaluate()

    # ML score
    ml_score = predict_score(signal_report)

    # Return everything
    return {
        "signal_report": signal_report,
        "decision": decision,
        "ml_score": ml_score
    }