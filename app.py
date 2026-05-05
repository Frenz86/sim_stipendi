import streamlit as st
from stati import italia, spagna, francia, germania

#st.set_page_config(page_title="Calcolo Stipendio Netto", page_icon="💰", layout="centered")

import streamlit as st

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Questo mira specificamente al badge in basso a destra */
            div[data-testid="stStatusWidget"] {display: none !important;}
            .stAppDeployButton {display: none !important;}
            /* Selettore universale per il viewer badge di Streamlit Cloud */
            [data-testid="stViewerBadge"] {display: none !important;}
            /* Rimuove lo spazio bianco aggiunto dal badge */
            iframe[title="streamlitApp"] { margin-bottom: -2rem !important; }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


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
