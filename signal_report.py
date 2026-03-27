from scipy.stats import ttest_ind

def generate_signal_report(version_A, version_B):
    report = {}

    # Welch's T-test
    t_stat, p_value = ttest_ind(
        version_A['avg_latency'],
        version_B['avg_latency'],
        equal_var=False
    )

    report['statistical_test'] = {
    'metric': 'avg_latency',
    't_statistic': float(t_stat),
    'p_value': float(p_value),
    'significant': bool(p_value < 0.05)
    }

    def percentage_change(a, b):
        return ((b - a) / a) * 100

    metrics = ['avg_latency', 'error_rate', 'throughput']
    changes = {}

    for m in metrics:
        mean_A = version_A[m].mean()
        mean_B = version_B[m].mean()
        pct = percentage_change(mean_A, mean_B)

        if m in ['avg_latency', 'error_rate']:
            status = "Improved" if pct < 0 else "Worsened"
        else:
            status = "Improved" if pct > 0 else "Worsened"

        changes[m] = {
        "mean_A": float(mean_A),
        "mean_B": float(mean_B),
        "percentage_change": float(pct),
        "status": status
        }

    report['metric_changes'] = changes

    report['summary'] = {
        "improved": [m for m in changes if changes[m]['status'] == "Improved"],
        "worsened": [m for m in changes if changes[m]['status'] == "Worsened"]
    }

    return report