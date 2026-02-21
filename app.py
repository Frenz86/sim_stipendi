import streamlit as st
from stati import italia, spagna

st.set_page_config(page_title="Calcolo Stipendio Netto", page_icon="💰", layout="centered")


def fmt(v: float) -> str:
    return f"€ {int(round(v))}"


def main():
    st.title("Calcolo Stipendio Netto")
    st.image("aa.jpg")

    nazione = st.selectbox("Paese / País", ["Italia 🇮🇹", "Spagna 🇪🇸"])

    if nazione == "Italia 🇮🇹":
        italia.render_ui(fmt)
    else:
        spagna.render_ui(fmt)


if __name__ == "__main__":
    main()
