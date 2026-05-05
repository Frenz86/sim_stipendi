import streamlit as st
from stati import italia, spagna, francia, germania

st.set_page_config(page_title="Calcolo Stipendio Netto", page_icon="💰", layout="centered")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        [data-testid="stToolbar"] {display: none !important;}
    </style>

    <script>
        const observer = new MutationObserver(() => {
            // Badge Streamlit Cloud (corona rossa)
            const badge = document.querySelector('a[href="https://streamlit.io/cloud"]');
            if (badge) badge.style.display = 'none';

            // Icona verde (status widget)
            const status = document.querySelector('[data-testid="stStatusWidget"]');
            if (status) status.style.display = 'none';
        });

        observer.observe(document.body, { childList: true, subtree: true });
    </script>
""", unsafe_allow_html=True)


def fmt(v: float) -> str:
    return f"€ {int(round(v))}"


def main():
    st.title("Calcolo Stipendio Netto")
    st.warning("I risultati sono **approssimati**: la simulazione si basa su aliquote medie e stime. Non sostituisce una consulenza fiscale o del lavoro.")
    st.image("aa.jpg")

    nazione = st.selectbox("Paese / País / Pays / Land / Deutschland", ["Italia 🇮🇹", "Spagna 🇪🇸", "Francia 🇫🇷", "Germania 🇩🇪"])

    if nazione == "Italia 🇮🇹":
        italia.render_ui(fmt)
    elif nazione == "Spagna 🇪🇸":
        spagna.render_ui(fmt)
    elif nazione == "Francia 🇫🇷":
        francia.render_ui(fmt)
    else:
        germania.render_ui(fmt)


if __name__ == "__main__":
    main()
