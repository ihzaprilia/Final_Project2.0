import streamlit as st

def about_dataset():

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
    # HEADER
    # =========================
    st.markdown("## 📊 Tentang Dataset")
    st.markdown(
        "Informasi singkat mengenai dataset yang digunakan dalam analisis performa siswa."
    )

    st.divider()

    # =========================
    # CONTENT
    # =========================
    col1, col2 = st.columns([4, 6], gap="medium")

    with col1:
        link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUsQxcvA2BpIdeW22Go3vs0u2Hxtph-bAVvg&s"
        st.image(
            link,
            caption="Healthcare Student Performance Data",
            use_container_width=True
        )

    with col2:
        st.markdown(
            """
            <div style="
                background-color: #FADADD;
                padding: 24px;
                border-radius: 18px;
                box-shadow: 0 6px 16px rgba(0,0,0,0.08);
            ">
                <h4 style="margin-top: 0;">📌 Deskripsi Dataset</h4>
                <p style="line-height: 1.7;">
                    Dataset ini digunakan untuk menganalisis <b>performa akademik siswa</b>
                    serta faktor-faktor yang memengaruhinya, seperti karakteristik demografis,
                    lingkungan keluarga, dan perilaku belajar.
                </p>
                <p style="line-height: 1.7;">
                    Data ini memungkinkan analisis hubungan antara kebiasaan belajar, kehadiran,
                    serta dukungan fasilitas belajar terhadap capaian nilai siswa sehingga
                    membantu institusi pendidikan merancang strategi pembelajaran yang lebih efektif.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
