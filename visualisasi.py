import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Student Performance Dashboard",
    layout="wide"
)

# =========================
# CUSTOM CSS (PINK THEME)
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
# PASTEL COLOR PALETTE
# =========================
PASTEL_COLORS = [
    "#FADADD",  # pink
    "#E3F2FD",  # blue
    "#E8F5E9",  # green
    "#FFF3E0",  # peach
    "#E6E6FA",  # lavender
    "#ECEFF1"   # grey
]

# =========================
# MAIN FUNCTION
# =========================
def chart():
    df = pd.read_excel("Student Performance Data.xlsx")

    # =========================
    # SIDEBAR FILTER
    # =========================
    st.sidebar.title("🔍 Filter Data")

    gender_filter = st.sidebar.multiselect(
        "Sex",
        options=df["sex"].unique(),
        default=df["sex"].unique()
    )

    performance_filter = st.sidebar.multiselect(
        "Performance Level",
        options=df["grade"].dropna().unique(),
        default=df["grade"].dropna().unique()
    )

    filtered_df = df[
        (df["sex"].isin(gender_filter)) &
        (df["grade"].isin(performance_filter))
    ]

    # =========================
    # TITLE
    # =========================
    st.title("🎓 Student Performance Dashboard")
    st.markdown(
        "Analisis performa akademik siswa berdasarkan perilaku, dukungan, dan latar belakang."
    )

    st.divider()

    # =========================
    # KPI METRICS
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_grade = filtered_df["grade"].mean()
        st.markdown(
            f"""
            <div style="background-color:#E3F2FD; padding:16px; border-radius:16px; text-align:center;">
                <h4>Average Grade</h4>
                <h2>{avg_grade:.2f}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        avg_attendance = filtered_df["absences"].mean()
        st.markdown(
            f"""
            <div style="background-color:#FFF3E0; padding:16px; border-radius:16px; text-align:center;">
                <h4>Average Absences</h4>
                <h2>{avg_attendance:.2f}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        total_students = filtered_df.shape[0]
        st.markdown(
            f"""
            <div style="background-color:#E8F5E9; padding:16px; border-radius:16px; text-align:center;">
                <h4>Total Students</h4>
                <h2>{total_students}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        high_risk_students = filtered_df[filtered_df["grade"] < 50].shape[0]
        st.markdown(
            f"""
            <div style="background-color:#FADADD; padding:16px; border-radius:16px; text-align:center;">
                <h4>High Risk Students</h4>
                <h2>{high_risk_students}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # DATAFRAME
    # =========================
    st.write("**1. Menampilkan DataFrame**")
    st.dataframe(filtered_df.head(), use_container_width=True)

    # =========================
    # PARENT JOB VISUALIZATION
    # =========================
    st.write("**2. Tipe Pekerjaan Orang Tua**")

    col1, col2 = st.columns(2)

    PINK_BG = "#FDF2F8"   # pink muda (samakan dengan background web)

    with col1:
        father_job = filtered_df["father_job"].value_counts()

        fig_father = px.bar(
            x=father_job.index,
            y=father_job.values,
            title="Tipe Pekerjaan Ayah",
            color_discrete_sequence=PASTEL_COLORS
        )

        fig_father.update_layout(
            paper_bgcolor=PINK_BG,
            plot_bgcolor=PINK_BG,
            title_font=dict(size=16)
        )

        st.plotly_chart(fig_father, use_container_width=True)

    with col2:
        mother_job = filtered_df["mother_job"].value_counts()

        fig_mother = px.bar(
            x=mother_job.index,
            y=mother_job.values,
            title="Tipe Pekerjaan Ibu",
            color_discrete_sequence=PASTEL_COLORS
        )

        fig_mother.update_layout(
            paper_bgcolor=PINK_BG,
            plot_bgcolor=PINK_BG,
            title_font=dict(size=16)
        )

        st.plotly_chart(fig_mother, use_container_width=True)


    # =========================
    # PINK BACKGROUND SETTING
    # =========================
    PINK_BG = "#FDF2F8"  # pink muda pastel

    # =========================
    # DISTRIBUTION
    # =========================
    st.write("**3. Distribusi Nilai Siswa**")

    fig_grade = px.histogram(
        filtered_df,
        x="grade",
        nbins=30,
        title="Distribusi Nilai Siswa",
        color_discrete_sequence=["#F9A8D4"]
    )
    fig_grade.update_layout(
        paper_bgcolor=PINK_BG,
        plot_bgcolor=PINK_BG
    )
    st.plotly_chart(fig_grade, use_container_width=True)

    # =========================
    # PERFORMANCE LEVEL
    # =========================
    st.write("**4. Performance Level Distribution**")

    performance_counts = (
        filtered_df["grade"]
        .value_counts()
        .reset_index()
    )
    performance_counts.columns = ["Performance Level", "Count"]

    # =========================
    # FORCE COLOR FOR EACH CATEGORY ✅
    # =========================
    unique_levels = performance_counts["Performance Level"].unique()

    color_map = {
        level: PASTEL_COLORS[i % len(PASTEL_COLORS)]
        for i, level in enumerate(unique_levels)
    }

    fig_performance = px.pie(
        performance_counts,
        names="Performance Level",
        values="Count",
        title="Performance Level Distribution",
        color="Performance Level",
        color_discrete_map=color_map
    )

    fig_performance.update_layout(
        paper_bgcolor=PINK_BG,
        plot_bgcolor=PINK_BG
    )

    st.plotly_chart(fig_performance, use_container_width=True)


    # =========================
    # ATTENDANCE VS PERFORMANCE
    # =========================
    st.write("**5. Attendance vs Performance**")

    fig_attendance = px.scatter(
        filtered_df,
        x="absences",
        y="grade",
        title="Attendance vs Performance",
        color_discrete_sequence=["#CE93D8"]
    )
    fig_attendance.update_layout(
        paper_bgcolor=PINK_BG,
        plot_bgcolor=PINK_BG
    )
    st.plotly_chart(fig_attendance, use_container_width=True)

    # =========================
    # BEHAVIOR ANALYSIS
    # =========================
    st.write("**6. Behavior Analysis**")
    col1, col2 = st.columns(2)

    with col1:
        fig_studytime = px.box(
            filtered_df,
            x="studytime",
            y="grade",
            title="Study Time vs Performance",
            color_discrete_sequence=["#A5D6A7"]
        )
        fig_studytime.update_layout(
            paper_bgcolor=PINK_BG,
            plot_bgcolor=PINK_BG
        )
        st.plotly_chart(fig_studytime, use_container_width=True)

    with col2:
        fig_freetime = px.box(
            filtered_df,
            x="freetime",
            y="grade",
            title="Free Time vs Performance",
            color_discrete_sequence=["#FFCCBC"]
        )
        fig_freetime.update_layout(
            paper_bgcolor=PINK_BG,
            plot_bgcolor=PINK_BG
        )
        st.plotly_chart(fig_freetime, use_container_width=True)

    # =========================
    # SUPPORT & SOCIAL
    # =========================
    st.write("**7. Support & Social Analysis**")
    col1, col2, col3 = st.columns(3)

    with col1:
        fig_support = px.pie(
            filtered_df,
            names="school_support",
            title="School Support",
            hole=0.4,
            color_discrete_sequence=PASTEL_COLORS
        )
        fig_support.update_layout(
            paper_bgcolor=PINK_BG,
            plot_bgcolor=PINK_BG
        )
        st.plotly_chart(fig_support, use_container_width=True)

    with col2:
        fig_health = px.pie(
            filtered_df,
            names="health",
            title="Health Status",
            hole=0.4,
            color_discrete_sequence=PASTEL_COLORS
        )
        fig_health.update_layout(
            paper_bgcolor=PINK_BG,
            plot_bgcolor=PINK_BG
        )
        st.plotly_chart(fig_health, use_container_width=True)

    with col3:
        fig_travel = px.pie(
            filtered_df,
            names="traveltime",
            title="Travel Time",
            hole=0.4,
            color_discrete_sequence=PASTEL_COLORS
        )
        fig_travel.update_layout(
            paper_bgcolor=PINK_BG,
            plot_bgcolor=PINK_BG
        )
        st.plotly_chart(fig_travel, use_container_width=True)


    st.divider()
    st.write(
        "Dashboard ini memberikan wawasan mendalam tentang faktor-faktor yang "
        "memengaruhi performa akademik siswa. Gunakan filter di sidebar untuk "
        "menyesuaikan analisis."
    )
