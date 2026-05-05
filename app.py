import streamlit as st
from stati import italia, spagna, francia, germania

# 1. POSIZIONA QUESTO ALL'INIZIO (Sotto gli import)
st.markdown('''
    <style>
    /* Nasconde il footer e il badge se accessibili */
    footer {visibility: hidden !important;}
    [data-testid="stViewerBadge"] {display: none !important;}
    
    /* CREIAMO UN COPRI-BADGE "STILE PATCH" */
    /* Questo crea un rettangolo che sta SOPRA il badge di Streamlit */
    .stApp > header + section::after {
        content: "";
        position: fixed;
        bottom: 0;
        right: 0;
        width: 100vw; /* Copre tutta la larghezza per sicurezza */
        height: 50px;
        background-color: white; /* <--- CAMBIA IN #0e1117 SE USI IL TEMA SCURO */
        z-index: 9999999;
        pointer-events: none;
    }
    
    /* Riduciamo il margine inferiore per non lasciare buchi bianchi */
    .main .block-container {
        padding-bottom: 0 !important;
        margin-bottom: -50px !important;
    }
    </style>
''', unsafe_allow_html=True)

def fmt(v: float) -> str:
    return f"€ {int(round(v))}"

def main():
    st.title("Calcolo Stipendio Netto")
    st.warning("I risultati sono **approssimati**: la simulazione si basa su aliquote medie e stime.")
    
    # Prova a caricare l'immagine, gestendo l'errore se manca
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
