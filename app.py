import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_loader import load_and_preprocess
from signal_report import generate_signal_report
from decision_logic import DecisionLogic
from ml_model import predict_score

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Decision Intelligence", layout="wide")

# ---- HEADER ----
st.markdown("""
<h2 style='margin-bottom:0;'>🚀 SecondOrder</h2>
<p style='color:gray;'>Smart Deployment Decision Engine</p>
""", unsafe_allow_html=True)

st.divider()

# ---- LOAD DATA ----
version_A, version_B, _ = load_and_preprocess("system_metrics.csv")

# ---- SIDEBAR (SIMULATION CONTROL) ----
st.sidebar.header("🎛️ Simulation Controls")

latency_adjust = st.sidebar.slider("Adjust Latency (%)", -20, 20, 0)
error_adjust = st.sidebar.slider("Adjust Error Rate (%)", -50, 50, 0)
throughput_adjust = st.sidebar.slider("Adjust Throughput (%)", -20, 20, 0)

# Apply simulation
version_B_sim = version_B.copy()
version_B_sim["avg_latency"] *= (1 + latency_adjust / 100)
version_B_sim["error_rate"] *= (1 + error_adjust / 100)
version_B_sim["throughput"] *= (1 + throughput_adjust / 100)

# ---- ANALYSIS ----
signal_report = generate_signal_report(version_A, version_B_sim)
decision = DecisionLogic(signal_report).evaluate()
ml_score = predict_score(signal_report)

# ---- DECISION CARD ----
status = decision["status"]

color_map = {
    "REJECT": "#ff4d4d",
    "HIGH RISK": "#ffa500",
    "UNCERTAIN": "#ffd700",
    "ACCEPT": "#4CAF50"
}

st.markdown(f"""
<div style="
    background:{color_map.get(status, "#999")};
    padding:25px;
    border-radius:12px;
    text-align:center;
    color:white;
    font-size:28px;
    font-weight:bold;">
    🚦 {status}
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,2])

with col1:
    st.metric("⚠️ Risk Score", decision["risk_score"])

with col2:
    st.metric("🤖 ML Confidence", f"{ml_score}%")

st.markdown(f"**🧠 Explanation:** {decision['explanation']}")

st.divider()

# ---- KPI METRICS ----
st.subheader("📊 Key Metrics")

cols = st.columns(3)
metrics = ["avg_latency", "error_rate", "throughput"]

for i, metric in enumerate(metrics):
    mean_A = version_A[metric].mean()
    mean_B = version_B_sim[metric].mean()
    delta = ((mean_B - mean_A) / mean_A) * 100

    cols[i].metric(
        label=metric,
        value=f"{mean_B:.2f}",
        delta=f"{delta:.2f}%"
    )

st.divider()

# ---- GRAPHS ----
st.subheader("📈 Performance Insights")

df = pd.concat([version_A, version_B_sim])

col1, col2 = st.columns(2)

with col1:
    fig_line = px.line(
        df.reset_index(),
        x=df.reset_index().index,
        y="avg_latency",
        color="version",
        title="Latency Trend"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    fig_box = px.box(
        df,
        x="version",
        y="error_rate",
        title="Error Distribution"
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.divider()

# ---- ML GAUGE ----
st.subheader("🤖 Deployment Confidence Gauge")

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=ml_score,
    title={'text': "Confidence Score"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "green"},
        'steps': [
            {'range': [0, 40], 'color': "red"},
            {'range': [40, 70], 'color': "orange"},
            {'range': [70, 100], 'color': "lightgreen"}
        ]
    }
))

st.plotly_chart(fig_gauge, use_container_width=True)