import streamlit as st
from stati import italia, spagna, francia, germania

st.set_page_config(page_title="Calcolo Stipendio Netto", page_icon="💰", layout="centered")
st.markdown("""
    <style>
        /* Nascondi tutto quello che Streamlit aggiunge */
        #MainMenu, footer, header {visibility: hidden !important;}
        
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="collapsedControl"],
        [data-testid="baseButton-headerNoPadding"] {
            display: none !important;
        }
        
        /* Forza rimozione sidebar toggle con selettore generico */
        section[data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
        
        /* Approccio nucleare: nascondi tutti i button nell'header */
        header button {display: none !important;}
        header {display: none !important;}
    </style>
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
