import streamlit as st
from stati import italia, spagna, francia, germania

#st.set_page_config(page_title="Calcolo Stipendio Netto", page_icon="💰", layout="centered")
import streamlit as st

# Iniezione aggressiva via st.html (disponibile nelle ultime versioni)
st.html(
    """
    <style>
    /* Nasconde tutto ciò che ha classi legate al badge o al footer */
    div[class*="viewerBadge"], 
    a[class*="viewerBadge"], 
    div[class*="styles_viewerBadge"],
    div[data-testid="stViewerBadge"],
    footer {
        display: none !important;
        height: 0 !important;
        width: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
        visibility: hidden !important;
    }

    /* Rimuove forzatamente lo spazio vuoto in fondo alla pagina */
    .main .block-container {
        padding-bottom: 0 !important;
    }

    /* Se il badge è dentro un iframe o un elemento fixed, questo lo colpisce */
    iframe[src*="streamlit.io"] {
        display: none !important;
    }
    </style>
    """
)

st.markdown(
    """
    <div style="position: fixed; bottom: 0; right: 0; width: 150px; height: 50px; background: white; z-index: 999999;">
    </div>
    """,
    unsafe_allow_html=True
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
