from sklearn.linear_model import LogisticRegression
import numpy as np

def train_dummy_model():
    X = np.array([
        [-5, -10, 5],
        [-3, 20, 2],
        [-2, 5, 3],
        [-6, -5, 6],
        [-1, 30, 1]
    ])

    y = [1, 0, 0, 1, 0]

    model = LogisticRegression()
    model.fit(X, y)

    return model


def predict_score(signal_report):
    changes = signal_report["metric_changes"]

    latency = changes["avg_latency"]["percentage_change"]
    error = changes["error_rate"]["percentage_change"]
    throughput = changes["throughput"]["percentage_change"]

    model = train_dummy_model()

    score = model.predict_proba([[latency, error, throughput]])[0][1]

    return round(score * 100, 2)