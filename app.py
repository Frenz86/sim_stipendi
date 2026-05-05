import streamlit as st
from stati import italia, spagna, francia, germania

#st.set_page_config(page_title="Calcolo Stipendio Netto", page_icon="💰", layout="centered")

import streamlit as st

# Usa st.html invece di st.markdown per una gestione più pulita del DOM
st.html("""
    <style>
    /* 1. Nasconde il badge "Hosted with Streamlit" in basso a destra */
    div[data-testid="stStatusWidget"], 
    ._container_gzau3_1, 
    ._viewerBadge_nim44_23, 
    [data-testid="stViewerBadge"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* 2. Nasconde il pulsante "Deploy" in alto a destra */
    .stAppDeployButton {
        display: none !important;
    }

    /* 3. Nasconde il menu hamburger e il footer standard */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 4. Forza l'app a occupare tutto lo spazio eliminando il margine del badge */
    #root > div:nth-child(1) > div > div > div > div > section > div {
        padding-bottom: 0 !important;
    }
    </style>
""")


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
