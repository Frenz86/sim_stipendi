import streamlit as st
from stati import italia, spagna, francia, germania

# 1. QUESTA È LA SOLUZIONE "ULTIMATUM"
# Va messa subito dopo gli import
st.markdown(
    """
    <style>
    /* Nasconde il footer originale */
    footer {visibility: hidden !important; display: none !important;}

    /* Crea un blocco fisso che segue lo zoom e copre l'angolo destro */
    .stApp > header + section::after {
        content: "";
        position: fixed;
        bottom: 0;
        right: 0;
        width: 250px; /* Molto largo per coprire anche con lo zoom */
        height: 60px;  /* Più alto del badge */
        background-color: #ffffff; /* <--- USA #0e1117 SE IL TEMA È SCURO */
        z-index: 999999999;
        pointer-events: none;
        display: block !important;
    }

    /* Colpiamo duramente il badge con tutti i selettori conosciuti */
    [data-testid="stViewerBadge"], 
    ._container_gzau3_1, 
    ._viewerBadge_nim44_23,
    a[href*="streamlit.io/cloud"] {
        display: none !important;
        opacity: 0 !important;
        visibility: hidden !important;
        pointer-events: none !important;
        transform: scale(0) !important; /* Lo rimpicciolisce a zero */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def fmt(v: float) -> str:
    return f"€ {int(round(v))}"

def main():
    st.title("Calcolo Stipendio Netto")
    st.warning("I risultati sono approssimati: la simulazione si basa su aliquote medie e stime.")
    
    # Gestione immagine sicura
    try:
        st.image("aa.jpg")
    except:
        pass

    nazione = st.selectbox("Paese", ["Italia 🇮🇹", "Spagna 🇪🇸", "Francia 🇫🇷", "Germania 🇩🇪"])

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