import streamlit as st
from stati import italia, spagna, francia, germania

#st.set_page_config(page_title="Calcolo Stipendio Netto", page_icon="💰", layout="centered")

import streamlit as st
import streamlit.components.v1 as components

# 1. CSS di backup (per sicurezza)
st.markdown("""
    <style>
    [data-testid="stViewerBadge"], ._container_gzau3_1, footer {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. JAVASCRIPT (La soluzione definitiva per le ultime versioni)
components.html("""
<script>
    const hideBadge = () => {
        // Cerca il badge tramite il tag 'a' e la classe parziale
        const badges = window.parent.document.querySelectorAll('a[class*="viewerBadge"]');
        badges.forEach(badge => {
            badge.style.display = 'none';
            badge.style.visibility = 'hidden';
        });
        
        // Cerca il badge tramite l'attributo data-testid
        const testIdBadge = window.parent.document.querySelector('div[data-testid="stViewerBadge"]');
        if (testIdBadge) {
            testIdBadge.style.display = 'none';
        }
    };

    // Esegui subito e poi ogni 500ms per intercettare caricamenti ritardati
    hideBadge();
    setInterval(hideBadge, 500);
</script>
""", height=0)


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
