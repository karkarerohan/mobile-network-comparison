import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Mobile Network Comparison Tool",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Mobile Communication Network Comparison Tool")

st.write(
    "Welcome! This tool compares GSM, GPRS, WCDMA, LTE, and WiMAX networks."
)

st.info(
    "Educational simulation: results are based on simplified models, "
    "not live mobile network measurements."
)

st.subheader("Select Networks")

networks = st.multiselect(
    "Choose the networks you want to compare:",
    ["GSM", "GPRS", "WCDMA", "LTE", "WiMAX"],
    default=["GSM", "LTE", "WiMAX"]
)

if networks:
    data = pd.DataFrame({
        "Network": ["GSM", "GPRS", "WCDMA", "LTE", "WiMAX"],
        "Typical Data Rate (Mbps)": [0.014, 0.114, 2, 100, 70],
        "Illustrative Latency (ms)": [500, 300, 100, 40, 50]
    })

    comparison = data[data["Network"].isin(networks)]

    st.subheader("Network Comparison")

    st.dataframe(comparison, use_container_width=True)

    st.subheader("Data Rate Comparison")

    fig = px.bar(
        comparison,
        x="Network",
        y="Typical Data Rate (Mbps)",
        title="Illustrative Data Rate by Network"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Latency Comparison")

    fig2 = px.bar(
        comparison,
        x="Network",
        y="Illustrative Latency (ms)",
        title="Illustrative Latency by Network"
    )

    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Please select at least one network.")
    st.subheader("📶 Signal Strength Simulator")

signal_strength = st.slider(
    "Adjust Signal Strength (%)",
    min_value=10,
    max_value=100,
    value=80,
    step=5
)

st.write("Current Signal Strength:", signal_strength, "%")

st.caption(
    "Educational simulation only. This is not a real mobile signal measurement."
)
st.subheader("📊 Simulated Network Performance")

network_data = {
    "GSM": {"rate": 0.014, "latency": 500},
    "GPRS": {"rate": 0.114, "latency": 300},
    "WCDMA": {"rate": 2, "latency": 100},
    "LTE": {"rate": 100, "latency": 40},
    "WiMAX": {"rate": 70, "latency": 50}
}

signal_factor = signal_strength / 100

if networks:
    results = []

    for network in networks:
        base_rate = network_data[network]["rate"]
        base_latency = network_data[network]["latency"]

        simulated_rate = base_rate * signal_factor
        simulated_latency = base_latency / signal_factor
        packet_loss = (100 - signal_strength) * 0.1

        results.append({
            "Network": network,
            "Data Rate (Mbps)": round(simulated_rate, 3),
            "Latency (ms)": round(simulated_latency, 1),
            "Packet Loss (%)": round(packet_loss, 1)
        })

    performance = pd.DataFrame(results)

    st.dataframe(performance, use_container_width=True)

    st.subheader("⚡ Data Rate")
    st.bar_chart(
        performance.set_index("Network")[["Data Rate (Mbps)"]]
    )

    st.subheader("⏱️ Latency")
    st.bar_chart(
        performance.set_index("Network")[["Latency (ms)"]]
    )

    st.subheader("📉 Packet Loss")
    st.bar_chart(
        performance.set_index("Network")[["Packet Loss (%)"]]
    )
    st.subheader("📡 Network Signal Status")

if signal_strength >= 80:
    st.success("Strong Signal 🟢 - Excellent signal strength!")

elif signal_strength >= 50:
    st.warning("Moderate Signal 🟡 - Signal strength is acceptable.")

else:
    st.error("Weak Signal 🔴 - Signal strength is low!")

st.write("Current Signal Strength:", signal_strength, "%")
st.subheader("🏆 Best Network Recommendation")

if networks:
    best_network = max(
        results,
        key=lambda item: item["Data Rate (Mbps)"]
    )

    st.success(
        f"Recommended Network: {best_network['Network']}"
    )

    st.write(
        f"Simulated Data Rate: "
        f"{best_network['Data Rate (Mbps)']} Mbps"
    )

    st.write(
        f"Simulated Latency: "
        f"{best_network['Latency (ms)']} ms"
    )

    st.info(
        "Recommendation is based on simulated data rate only. "
        "Real network performance may differ."
    )
else:
    st.warning("Please select at least one network.")
    st.subheader("⭐ Network Performance Score")

if networks:
    scores = []

    for item in results:
        rate = item["Data Rate (Mbps)"]
        latency = item["Latency (ms)"]

        max_rate = network_data[item["Network"]]["rate"]
        base_latency = network_data[item["Network"]]["latency"]

        rate_score = (rate / max_rate) * 50
        latency_score = (base_latency / latency) * 50

        total_score = round(rate_score + latency_score)

        scores.append({
            "Network": item["Network"],
            "Performance Score": total_score
        })

    score_df = pd.DataFrame(scores)

    st.dataframe(score_df, use_container_width=True)

    st.bar_chart(
        score_df.set_index("Network")
    )

    st.caption(
        "Score is an illustrative educational score based on "
        "simulated data rate and latency, not a real-world benchmark."
    )
    