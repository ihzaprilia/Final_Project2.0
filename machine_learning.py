import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from statsmodels.stats.outliers_influence import variance_inflation_factor
import joblib


def ml_model():

    # =========================
    # CUSTOM CSS (PINK THEME)
    # =========================
    st.markdown(
        """
        <style>
        .stApp { background-color: #FDF2F8; }
        section[data-testid="stSidebar"] { background-color: #FADADD; }
        h1, h2, h3, h4 { color: #831843; }
        hr { border-top: 1px solid #F9A8D4; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # TITLE
    # =========================
    st.title("📊 Student Performance Analysis & Modeling")

    df = pd.read_excel("Student Performance Data.xlsx")

    # =========================
    # 1. IDENTIFIKASI TIPE DATA
    # =========================
    numbers = df.select_dtypes(include=["number"]).columns

    # =========================
    # 2. OUTLIER HANDLING
    # =========================
    st.header("❶ Deteksi dan Penanganan Outlier (IQR Method)")

    Q1 = df[numbers].quantile(0.25)
    Q3 = df[numbers].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    st.write(f"Jumlah data sebelum pembersihan: **{df.shape[0]} baris**")
    df = df[~((df[numbers] < lower_bound) | (df[numbers] > upper_bound)).any(axis=1)]
    st.write(f"Jumlah data setelah pembersihan outlier: **{df.shape[0]} baris**")

    # =========================
    # 3. PREVIEW DATA
    # =========================
    df_select = df[numbers]
    st.dataframe(df.head(), use_container_width=True)

    # =========================
    # 4. KORELASI
    # =========================
    
    st.header("❷ Analisis Korelasi Antar Variabel Numerik")

    col1, col2 = st.columns([6, 4])

    PINK_BG = "#FDF2F8"  # pink muda pastel

    with col1:
        st.subheader("📈 Correlation Heatmap")

        corr = df_select.corr().round(2)

        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdPu"
        )

        fig.update_layout(
            paper_bgcolor=PINK_BG,
            plot_bgcolor=PINK_BG,
            title_font=dict(size=16),
            coloraxis_colorbar=dict(
                bgcolor=PINK_BG
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📝 Interpretasi Korelasi")
        st.write(
            """
            - **Mother Education – Father Education (0.63)**
            Korelasi positif kuat.
            Tingkat pendidikan ibu cenderung sejalan dengan tingkat pendidikan ayah.
            - **Mother Education – Grade (0.24)**
            Korelasi positif lemah.
            Pendidikan ibu memiliki hubungan positif kecil terhadap nilai akhir siswa.
            - **Father Education – Grade (0.19)**
            Korelasi positif lemah.
            Pendidikan ayah sedikit berhubungan dengan peningkatan nilai siswa.
            - **Age – Grade (-0.20)**
            Korelasi negatif lemah.
            Semakin bertambah usia siswa, nilai akhir cenderung sedikit menurun.
            - **Study Time – Grade (0.10)**
            Korelasi positif sangat lemah.
            Waktu belajar memiliki pengaruh kecil terhadap nilai akhir.
            - **Travel Time – Grade (-0.11)**
            Korelasi negatif sangat lemah.
            Waktu perjalanan yang lebih lama sedikit berkaitan dengan penurunan nilai.
            - **Absences – Grade (0.07)**
            Korelasi positif sangat lemah.
            Jumlah ketidakhadiran hampir tidak berpengaruh terhadap nilai akhir.
            - **Health – Grade (-0.05)**
            Korelasi sangat lemah (mendekati nol).
            Kondisi kesehatan tidak menunjukkan hubungan berarti dengan nilai.

            """
        )


    # =========================
    # 5. SPLIT VARIABEL
    # =========================
    X = df_select.drop("grade", axis=1)
    y = df_select["grade"]

    # =========================
    # 6. VIF
    # =========================
    st.header("❸ Uji Multikolinearitas (VIF)")

    vif_df = pd.DataFrame()
    vif_df["Feature"] = X.columns
    vif_df["VIF"] = [
        variance_inflation_factor(X.values, i)
        for i in range(X.shape[1])
    ]
    st.dataframe(vif_df, use_container_width=True)

    # =========================
    # 7. TRAIN TEST SPLIT
    # =========================
    st.header("❹ Train Test Split")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    st.write("Jumlah data train:", len(X_train))
    st.write("Jumlah data test:", len(X_test))

    tab1, tab2 = st.tabs(["📘 Data Train", "📕 Data Test"])
    with tab1:
        st.subheader("X_train")
        st.dataframe(X_train.head())
        st.subheader("y_train")
        st.dataframe(y_train.head())

    with tab2:
        st.subheader("X_test")
        st.dataframe(X_test.head())
        st.subheader("y_test")
        st.dataframe(y_test.head())


    # =========================
    # 8. SCALING
    # =========================
    st.header("❺ Standard Scaler")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # =========================
    # 9. LINEAR REGRESSION
    # =========================
    st.header("❻ Linear Regression")

    linreg = LinearRegression()
    linreg.fit(X_train, y_train)

    coef_df = pd.DataFrame({
        "Feature": X.columns,
        "Coefficient": linreg.coef_
    })
    st.dataframe(coef_df, use_container_width=True)

    # =========================
    # 10. HYPERPARAMETER TUNING
    # =========================
    st.header("❼ Hyperparameter Tuning")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Tuning Ridge"):
            ridge = Ridge()
            grid = GridSearchCV(
                ridge,
                {"alpha": np.logspace(-3, 3, 20)},
                cv=10,
                scoring="neg_mean_squared_error"
            )
            grid.fit(X_train_scaled, y_train)
            st.success(f"Best Alpha Ridge: {grid.best_params_['alpha']}")

    with col2:
        if st.button("Tuning Lasso"):
            lasso = Lasso(max_iter=10000)
            grid = GridSearchCV(
                lasso,
                {"alpha": np.logspace(-3, 3, 20)},
                cv=10,
                scoring="neg_mean_squared_error"
            )
            grid.fit(X_train_scaled, y_train)
            st.success(f"Best Alpha Lasso: {grid.best_params_['alpha']}")

    # =========================
    # 11. RIDGE & LASSO
    # =========================
    st.header("❽ Model Evaluation")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📘 Ridge Regression")
        ridge = Ridge(alpha=112)
        ridge.fit(X_train_scaled, y_train)

        y_pred = ridge.predict(X_test_scaled)

        st.metric("MAE", round(mean_absolute_error(y_test, y_pred), 3))
        st.metric("RMSE", round(np.sqrt(mean_squared_error(y_test, y_pred)), 3))
        st.metric("R²", round(ridge.score(X_test_scaled, y_test), 3))

    with col2:
        st.subheader("📕 Lasso Regression")
        lasso = Lasso(alpha=0.33)
        lasso.fit(X_train_scaled, y_train)

        y_pred = lasso.predict(X_test_scaled)

        st.metric("MAE", round(mean_absolute_error(y_test, y_pred), 3))
        st.metric("RMSE", round(np.sqrt(mean_squared_error(y_test, y_pred)), 3))
        st.metric("R²", round(lasso.score(X_test_scaled, y_test), 3))

    # =========================
    # 12. LINEAR REGRESSION METRICS
    # =========================
    st.subheader("📊 Linear Regression")

    y_pred = linreg.predict(X_test)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("MAE", round(mean_absolute_error(y_test, y_pred), 3))
    col2.metric(
        "MAPE (%)",
        round(np.mean(np.abs((y_test - y_pred) / y_test)) * 100, 2)
    )
    col3.metric("RMSE", round(np.sqrt(mean_squared_error(y_test, y_pred)), 3))
    col4.metric("R²", round(r2_score(y_test, y_pred), 3))

    # =========================
    # 13. SAVE MODEL
    # =========================
    st.header("💾 Save Model")

    joblib.dump(ridge, "model_ridge.pkl")
    joblib.dump(X.columns, "numeric_columns.pkl")

    st.success("Model berhasil disimpan ✅")
