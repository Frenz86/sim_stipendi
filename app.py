import streamlit as st
from stati import italia, spagna, francia, germania

st.set_page_config(page_title="Calcolo Stipendio Netto", page_icon="💰", layout="centered")
hide_streamlit_style = """
    <style>
        /* Nasconde il footer con il logo Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Nasconde il pulsante Fork e la toolbar in alto a destra */
        .stToolbar {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        
        /* Nasconde il bottone "Manage app" in basso a destra */
        .viewerBadge_container__r5tak {display: none !important;}
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.set_page_config(
    page_title="La tua app",
    initial_sidebar_state="hidden"  # o "hidden" nelle versioni più recenti
)


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
