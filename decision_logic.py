class DecisionLogic:
    def __init__(self, signal_report):
        self.report = signal_report

    def evaluate(self):
        p_value = self.report['statistical_test']['p_value']
        changes = self.report['metric_changes']

        error_change = changes['error_rate']['percentage_change']
        latency_change = changes['avg_latency']['percentage_change']

        explanation = []
        risk_score = 0
        status = "ACCEPT"

        # Rule 1: Statistical significance
        if p_value > 0.05:
            status = "UNCERTAIN"
            explanation.append("Change is not statistically significant.")
            risk_score += 2

        # Rule 2: Error spike
        if error_change > 10:
            status = "REJECT"
            explanation.append(f"Error rate increased by {error_change:.2f}%.")
            risk_score += 5

        # Rule 3: Trade-off
        if latency_change < 0 and error_change > 0:
            if status != "REJECT":
                status = "HIGH RISK"
            explanation.append("Latency improved but error increased.")
            risk_score += 3

        risk_score = min(risk_score, 10)

        return {
            "status": status,
            "risk_score": risk_score,
            "explanation": " ".join(explanation)
        }