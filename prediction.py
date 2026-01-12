import streamlit as st
import pandas as pd
import joblib

def prediction_app():

    # =========================
    # STYLE (PASTEL THEME)
    # =========================
    st.markdown(
        """
        <style>
        /* Background utama */
        .stApp {
            background-color: #FDF2F8; /* pink muda */
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #FADADD; /* pink pastel */
        }

        /* Header */
        h1, h2, h3, h4 {
            color: #831843;
        }

        /* Divider */
        hr {
            border-top: 1px solid #F9A8D4;
        }
        </style>
        """,
        unsafe_allow_html=True
    )



    # =========================
    # LOAD MODEL
    # =========================
    @st.cache_resource
    def load_model():
        model = joblib.load("model_ridge.pkl")
        features = joblib.load("numeric_columns.pkl")
        return model, features

    model, feature_columns = load_model()

    # =========================
    # HEADER
    # =========================
    st.title("🧑🏻‍🎓 Student Grade Prediction")
    st.markdown(
        """
        Masukkan **data numerik siswa** di bawah ini untuk memprediksi **nilai akhir (grade)** berdasarkan model *Machine Learning*.
        """
    )

    st.divider()

    # =========================
    # INPUT FORM
    # =========================
    with st.form("prediction_form"):
        st.subheader("📌 Student Input Data")

        inputs = {}
        cols = st.columns(2)

        i = 0
        for feature in feature_columns:
            if feature not in ["grade", "study_efficiency"]:
                with cols[i % 2]:
                    inputs[feature] = st.number_input(
                        label=feature.replace("_", " ").title(),
                        value=0.0,
                        step=1.0
                    )
                i += 1

        st.markdown("---")
        submitted = st.form_submit_button("🔮 Predict Grade")

    # =========================
    # PREDICTION RESULT
    # =========================
    if submitted:
        input_df = pd.DataFrame([inputs])
        prediction = model.predict(input_df)[0]

        prediction = max(0, min(100, prediction))

        st.divider()
        st.subheader("📊 Prediction Result")

        if prediction >= 75:
            level = "High Performance 🏆"
            color = "#E6F4EA"  # pastel green
        elif prediction >= 50:
            level = "Medium Performance ⚠️"
            color = "#FFF7E6"  # pastel yellow
        else:
            level = "Low Performance 🚨"
            color = "#FDEAEA"  # pastel red

        st.markdown(
    f"""
    <div class="prediction-card"
         style="
            background-color:{color};
            border-radius:18px;
            padding:25px;
            text-align:center;
            box-shadow:0 6px 15px rgba(0,0,0,0.12);
         ">
        Final Grade Prediction<br>
        <span style="font-size:42px; font-weight:700;">
            {round(prediction, 2)}
        </span><br>
        {level}
    </div>
    """,
    unsafe_allow_html=True
)
