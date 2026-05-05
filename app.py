import streamlit as st
from stati import italia, spagna, francia, germania

st.set_page_config(page_title="Calcolo Stipendio Netto", page_icon="💰", layout="centered")

import os, streamlit as _st

# Patch dell'index.html di Streamlit (equivalente al sed del Dockerfile)
_index = os.path.join(os.path.dirname(_st.__file__), "static", "index.html")
with open(_index, "r") as f:
    _html = f.read()

_css = '<style>a[href="https://streamlit.io/cloud"]{display:none!important;}[data-testid="stToolbar"]{display:none!important;}[data-testid="stStatusWidget"]{display:none!important;}footer{visibility:hidden!important;}header{visibility:hidden!important;}</style>'

if _css not in _html:
    with open(_index, "w") as f:
        f.write(_html.replace("</head>", _css + "</head>"))

# --- il tuo codice normale da qui ---
from stati import italia, spagna, francia, germania

st.set_page_config(...)


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
