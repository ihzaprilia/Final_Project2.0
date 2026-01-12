import streamlit as st

def contact_me():

    # =========================
    # CUSTOM CSS (PASTEL CONTACT PAGE)
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
    # CONTENT
    # =========================
    st.markdown("<div class='contact-card'>", unsafe_allow_html=True)

    st.markdown("## 📬 Contact Me")
    st.write(
        "Jika Anda memiliki pertanyaan atau ingin berdiskusi lebih lanjut, "
        "silakan hubungi saya melalui email atau media sosial berikut:"
    )

    st.markdown("📧 **Email:** ihzapr@gmail.com")
    st.markdown("🔗 **LinkedIn:** [linkedin.com/in/ihzaaprilia](https://www.linkedin.com/in/ihzaaprilia/)")
    st.markdown("🐱 **GitHub:** [github.com/ihzaaprilia](https://github.com/ihzaaprilia)")

    st.write(
        "Saya terbuka untuk kolaborasi dan diskusi seputar "
        "**data science dan machine learning**. "
        "Terima kasih telah mengunjungi aplikasi ini!"
    )

    st.markdown("</div>", unsafe_allow_html=True)
