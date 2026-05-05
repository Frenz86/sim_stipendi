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

    # --- IL KILLER DEL BADGE PARTE DA QUI ---
    # Lo inseriamo alla fine così viene eseguito dopo che la UI è pronta
    st.components.v1.html("""
    <style>
        /* CSS estremo: nasconde il contenitore e il link */
        [data-testid="stViewerBadge"], 
        ._container_gzau3_1, 
        ._viewerBadge_nim44_23, 
        a[href*="streamlit.io/cloud"],
        footer {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
    </style>
    <script>
        // Funzione per rimuovere il badge dal DOM superiore (parent)
        function removeBadge() {
            const badge = window.parent.document.querySelector('div[data-testid="stViewerBadge"]') || 
                          window.parent.document.querySelector('._container_gzau3_1') ||
                          window.parent.document.querySelector('a[href*="streamlit.io/cloud"]');
            if (badge) {
                badge.style.display = 'none';
                badge.remove();
            }
        }
        // Esegui subito e poi monitora ogni 400ms
        removeBadge();
        setInterval(removeBadge, 400);
    </script>
    """, height=0)