import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #f3e5f5, #fff3e0);
    }

    /* Main title */
    .main-title {
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        color: #1565c0;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #555555;
        margin-bottom: 30px;
    }

    /* Metric cards */
    .metric-card {
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        color: white;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.15);
        margin-bottom: 15px;
    }

    .temperature {
        background: linear-gradient(135deg, #ff6f61, #ff9800);
    }

    .maximum {
        background: linear-gradient(135deg, #f44336, #e91e63);
    }

    .minimum {
        background: linear-gradient(135deg, #2196f3, #00bcd4);
    }

    .rainfall {
        background: linear-gradient(135deg, #3949ab, #7e57c2);
    }

    .humidity {
        background: linear-gradient(135deg, #00897b, #26a69a);
    }

    .metric-title {
        font-size: 16px;
        font-weight: bold;
    }

    .metric-value {
        font-size: 28px;
        font-weight: bold;
    }

    /* Section headings */
    .section-title {
        font-size: 27px;
        font-weight: bold;
        color: #333333;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Information box */
    .info-box {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255,255,255,0.8);
        box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🌦️ Weather Data Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Explore temperature, rainfall and humidity data 📊</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚙️ Dashboard Settings")

uploaded_file = st.sidebar.file_uploader(
    "📁 Upload Weather CSV",
    type=["csv"]
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("weather_data.csv")


# Convert date
data["date"] = pd.to_datetime(data["date"])


# --------------------------------------------------
# SIDEBAR DATE FILTER
# --------------------------------------------------

st.sidebar.subheader("📅 Date Filter")

min_date = data["date"].min().date()
max_date = data["date"].max().date()

start_date = st.sidebar.date_input(
    "Start Date",
    min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End Date",
    max_date,
    min_value=min_date,
    max_value=max_date
)


# Filter data
filtered_data = data[
    (data["date"].dt.date >= start_date) &
    (data["date"].dt.date <= end_date)
]


# --------------------------------------------------
# CALCULATE STATISTICS
# --------------------------------------------------

average_temp = filtered_data["temperature"].mean()
maximum_temp = filtered_data["temperature"].max()
minimum_temp = filtered_data["temperature"].min()

total_rainfall = filtered_data["rainfall"].sum()
average_humidity = filtered_data["humidity"].mean()


# --------------------------------------------------
# WEATHER SUMMARY
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📊 Weather Summary</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.markdown(f"""
    <div class="metric-card temperature">
        <div class="metric-title">🌡️ Average Temperature</div>
        <div class="metric-value">{average_temp:.1f} °C</div>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown(f"""
    <div class="metric-card maximum">
        <div class="metric-title">🔥 Maximum Temperature</div>
        <div class="metric-value">{maximum_temp:.1f} °C</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown(f"""
    <div class="metric-card minimum">
        <div class="metric-title">❄️ Minimum Temperature</div>
        <div class="metric-value">{minimum_temp:.1f} °C</div>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown(f"""
    <div class="metric-card rainfall">
        <div class="metric-title">🌧️ Total Rainfall</div>
        <div class="metric-value">{total_rainfall:.1f} mm</div>
    </div>
    """, unsafe_allow_html=True)


with col5:
    st.markdown(f"""
    <div class="metric-card humidity">
        <div class="metric-title">💧 Avg Humidity</div>
        <div class="metric-value">{average_humidity:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3 = st.tabs([
    "📈 Temperature",
    "🌧️ Rainfall",
    "📋 Data"
])


# --------------------------------------------------
# TEMPERATURE TAB
# --------------------------------------------------

with tab1:

    st.markdown(
        '<div class="section-title">🌡️ Temperature Trend</div>',
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        filtered_data["date"],
        filtered_data["temperature"],
        marker="o",
        linewidth=2
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature Over Time")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

    st.info(
        "💡 This graph shows how temperature changes over the selected period."
    )


# --------------------------------------------------
# RAINFALL TAB
# --------------------------------------------------

with tab2:

    st.markdown(
        '<div class="section-title">🌧️ Rainfall Analysis</div>',
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.bar(
        filtered_data["date"],
        filtered_data["rainfall"]
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Rainfall (mm)")
    ax.set_title("Rainfall Over Time")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

    st.info(
        "💡 The bars represent the amount of rainfall recorded on each day."
    )


# --------------------------------------------------
# DATA TAB
# --------------------------------------------------

with tab3:

    st.markdown(
        '<div class="section-title">📋 Weather Dataset</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        filtered_data,
        use_container_width=True,
        height=400
    )

    csv = filtered_data.to_csv(index=False)

    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name="weather_data_filtered.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# MONTHLY ANALYSIS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📅 Monthly Analysis</div>',
    unsafe_allow_html=True
)

filtered_data["month"] = filtered_data["date"].dt.month_name()

monthly = (
    filtered_data
    .groupby("month")["temperature"]
    .mean()
    .reset_index()
)

monthly.columns = [
    "Month",
    "Average Temperature"
]

st.dataframe(
    monthly,
    use_container_width=True
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#666;">
        🌦️ Weather Data Analyzer | Built with Python & Streamlit 🚀
    </div>
    """,
    unsafe_allow_html=True
)