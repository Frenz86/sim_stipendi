import streamlit as st
from stati import italia, spagna, francia, germania

# Configurazione pagina (opzionale)
# st.set_page_config(page_title="Calcolo Stipendio Netto", page_icon="💰", layout="centered")

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

    # --- ULTIMISSIMA SPIAGGIA: IL "COPRI-BADGE" DINAMICO ---
    st.markdown(
        """
        <style>
        /* 1. CSS Universale: Colpisce ogni possibile tag A che porta a Streamlit */
        iframe[title="streamlitApp"] + div a, 
        a[href*="streamlit.io/cloud"], 
        [data-testid="stViewerBadge"],
        ._container_gzau3_1 {
            display: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            z-index: -1 !important;
        }

        /* 2. Il "Tappo": Crea un rettangolo fisso sopra l'area del badge */
        /* Usiamo un selettore che Streamlit non può bloccare facilmente */
        html body div.stApp::after {
            content: "";
            position: fixed;
            bottom: 0;
            right: 0;
            width: 150px; /* Copre la larghezza del badge */
            height: 50px;  /* Copre l'altezza del badge */
            background-color: #0e1117; /* <--- METTI QUI IL COLORE DEL TUO SFONDO */
            z-index: 999999;
            pointer-events: none;
        }
        
        /* Nasconde il footer classico */
        footer {display:none !important;}
        </style>
        """,
        unsafe_allow_html=True
    )