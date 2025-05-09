import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("📈 Portfolio Dashboard")

# Load data (replace with actual file path if reading from JSON)
uploaded_file = st.file_uploader("Upload your portfolio JSON", type="json")
if uploaded_file:
    df = pd.read_json(uploaded_file)

    # Clean & filter
    df = df[df["Symbol"].notna()]
    
    # Convert to float safely (handle commas and blanks)
    for col in ["Investment", "Current Value", "Current Gain"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "")
            .replace("", "0")
            .astype(float)
        )
    
    df["Gain%"] = (
        df["Gain%"]
        .astype(str)
        .str.replace("%", "")
        .replace("", "0")
        .astype(float)
    )
    
    df["Position Size"] = (
        df["Position Size"]
        .astype(str)
        .str.replace("%", "")
        .replace("", "0")
        .astype(float)
    )
    # KPIs
    total_investment = df["Investment"].sum()
    total_current_value = df["Current Value"].sum()
    total_gain = total_current_value - total_investment
    gain_percent = (total_gain / total_investment) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Investment", f"₹{total_investment:,.0f}")
    col2.metric("Current Value", f"₹{total_current_value:,.0f}")
    col3.metric("Gain/Loss", f"₹{total_gain:,.0f}", f"{gain_percent:.2f}%")

    st.divider()

    # Top/Bottom Performers
    st.subheader("📈 Top & Bottom 5 Performers (by Gain%)")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Top 5:")
        st.dataframe(df.sort_values("Gain%", ascending=False).head(5)[["Symbol", "Gain%", "Current Gain"]])
    with col2:
        st.write("Bottom 5:")
        st.dataframe(df.sort_values("Gain%").head(5)[["Symbol", "Gain%", "Current Gain"]])

    st.divider()

    # Sector Allocation Pie Chart
    st.subheader("📊 Sector-wise Allocation")
    sector_pie = df.groupby("Sector")["Investment"].sum().reset_index()
    fig = px.pie(sector_pie, names="Sector", values="Investment", title="Investment by Sector")
    st.plotly_chart(fig, use_container_width=True)

    # Market Cap Distribution
    st.subheader("🏢 Market Cap Distribution")
    cap_bar = df.groupby("Cap")["Investment"].sum().reset_index()
    fig = px.bar(cap_bar, x="Cap", y="Investment", title="Investment by Market Cap", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    # Individual Stock Gain
    st.subheader("📶 Stock-wise Gain/Loss")
    fig = px.bar(df.sort_values("Gain%"), x="Symbol", y="Gain%", color="Gain%",
                 title="Gain% by Stock", color_continuous_scale="RdYlGn")
    st.plotly_chart(fig, use_container_width=True)
