import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="🎓",
    layout="wide"
)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📊 Navigation")
st.sidebar.markdown("**Student Performance Dashboard**")

menu = st.sidebar.radio(
    "Select Page",
    [
        "🏠 About Dataset",
        "📈 Dashboards",
        "🤖 Machine Learning",
        "🔮 Prediction App",
        "📬 Contact Me"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("👩‍🎓 **Nur Ihza Aprilia**")
st.sidebar.caption("Final Project Data Science – Dibimbing")

# =========================
# MAIN HEADER
# =========================
st.title("🎓 Exploratory Analysis of Student Performance and Learning Factors")
st.markdown(
    """
    Analisis ini bertujuan untuk memahami faktor-faktor yang memengaruhi
    **performa akademik siswa** melalui eksplorasi data, visualisasi,
    serta penerapan **machine learning**.
    """
)

st.divider()

# =========================
# PAGE ROUTING
# =========================
if menu == "🏠 About Dataset":
    import about
    about.about_dataset()

elif menu == "📈 Dashboards":
    import visualisasi
    visualisasi.chart()

elif menu == "🤖 Machine Learning":
    import machine_learning
    machine_learning.ml_model()

elif menu == "🔮 Prediction App":
    import prediction
    prediction.prediction_app()

elif menu == "📬 Contact Me":
    import kontak
    kontak.contact_me()
