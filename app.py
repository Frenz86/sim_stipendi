import streamlit as st

st.set_page_config(page_title="Calcolo Stipendio Italia", page_icon="💰", layout="centered")

# --- Costanti ---
ALIQUOTA_INPS_DIPENDENTE = 0.0919
ALIQUOTA_INPS_AZIENDA = 0.30  # ~30% contributi carico azienda (stima media)

# Scaglioni IRPEF 2024 (riforma a 3 aliquote)
SCAGLIONI_IRPEF = [
    (28_000, 0.23),
    (50_000, 0.35),
    (float("inf"), 0.43),
]

# Addizionale regionale IRPEF 2024 (aliquota media/principale per regione)
ADDIZIONALE_REGIONALE = {
    "Abruzzo": 0.0173,
    "Basilicata": 0.0123,
    "Calabria": 0.0203,
    "Campania": 0.0203,
    "Emilia-Romagna": 0.0133,
    "Friuli-Venezia Giulia": 0.0070,
    "Lazio": 0.0173,
    "Liguria": 0.0123,
    "Lombardia": 0.0123,
    "Marche": 0.0173,
    "Molise": 0.0203,
    "Piemonte": 0.0162,
    "Puglia": 0.0123,
    "Sardegna": 0.0123,
    "Sicilia": 0.0123,
    "Toscana": 0.0142,
    "Trentino-Alto Adige": 0.0123,
    "Umbria": 0.0123,
    "Valle d'Aosta": 0.0070,
    "Veneto": 0.0123,
}


# --- Funzioni di calcolo ---

def calcola_irpef_lorda(imponibile: float) -> float:
    """Calcola l'IRPEF lorda sugli scaglioni."""
    imposta = 0.0
    precedente = 0.0
    for limite, aliquota in SCAGLIONI_IRPEF:
        scaglione = min(imponibile, limite) - precedente
        if scaglione <= 0:
            break
        imposta += scaglione * aliquota
        precedente = limite
    return imposta


def detrazioni_lavoro_dipendente(reddito: float) -> float:
    """Detrazioni per lavoro dipendente (art. 13 TUIR, aggiornato 2024)."""
    if reddito <= 15_000:
        return max(1_955, 690)
    elif reddito <= 28_000:
        return 1_910 + 1_190 * (28_000 - reddito) / 13_000
    elif reddito <= 50_000:
        return 1_910 * (50_000 - reddito) / 22_000
    return 0.0


def detrazione_coniuge(reddito: float) -> float:
    """Detrazione per coniuge a carico (art. 12 TUIR, semplificata 2024)."""
    if reddito <= 15_000:
        return 800.0
    elif reddito <= 40_000:
        return 690.0
    elif reddito <= 80_000:
        return 690.0 * (80_000 - reddito) / 40_000
    return 0.0


def detrazione_figli(reddito: float, n_figli: int) -> float:
    """Detrazione per figli > 21 anni a carico (950 per figlio, ridotta sul reddito)."""
    if n_figli == 0:
        return 0.0
    det_per_figlio = max(0.0, 950.0 * (95_000 - reddito) / 95_000)
    return det_per_figlio * n_figli


def trattamento_integrativo(reddito: float, irpef_lorda: float, det_lavoro: float) -> float:
    """Trattamento integrativo (ex bonus Renzi) 2024: max 1.200 annui."""
    if irpef_lorda <= det_lavoro:
        return 0.0
    if reddito <= 15_000:
        return 1_200.0
    elif reddito <= 28_000:
        return max(0.0, 1_200.0 * (28_000 - reddito) / 13_000)
    return 0.0


def ral_da_costo_aziendale(costo: float) -> float:
    """Stima la RAL partendo dal costo aziendale."""
    return costo / (1 + ALIQUOTA_INPS_AZIENDA)


def calcola_netto_annuo(
    ral: float,
    aliquota_regionale: float = 0.0,
    aliquota_comunale: float = 0.0,
    coniuge_carico: bool = False,
    n_figli: int = 0,
) -> dict:
    """Dal RAL calcola il netto annuo con dettaglio completo."""
    inps_dipendente = ral * ALIQUOTA_INPS_DIPENDENTE
    imponibile_irpef = ral - inps_dipendente

    irpef_lorda = calcola_irpef_lorda(imponibile_irpef)

    det_lavoro = detrazioni_lavoro_dipendente(ral)
    det_coniuge = detrazione_coniuge(ral) if coniuge_carico else 0.0
    det_figli_val = detrazione_figli(ral, n_figli)
    detrazioni_totali = det_lavoro + det_coniuge + det_figli_val

    irpef_netta = max(irpef_lorda - detrazioni_totali, 0)

    bonus_integrativo = trattamento_integrativo(ral, irpef_lorda, det_lavoro)

    addizionale_regionale = imponibile_irpef * aliquota_regionale
    addizionale_comunale = imponibile_irpef * aliquota_comunale

    tfr_annuo = ral / 13.5

    netto_annuo = (
        ral
        - inps_dipendente
        - irpef_netta
        - addizionale_regionale
        - addizionale_comunale
        + bonus_integrativo
    )

    return {
        "ral": ral,
        "inps_dipendente": inps_dipendente,
        "imponibile_irpef": imponibile_irpef,
        "irpef_lorda": irpef_lorda,
        "det_lavoro": det_lavoro,
        "det_coniuge": det_coniuge,
        "det_figli": det_figli_val,
        "irpef_netta": irpef_netta,
        "bonus_integrativo": bonus_integrativo,
        "addizionale_regionale": addizionale_regionale,
        "aliquota_regionale": aliquota_regionale,
        "addizionale_comunale": addizionale_comunale,
        "tfr_annuo": tfr_annuo,
        "netto_annuo": netto_annuo,
    }


def fmt(valore: float) -> str:
    return f"€ {int(round(valore))}"


# --- UI ---
def main():
    st.title("Calcolo Stipendio Netto")
    st.image("aa.jpg")
    st.caption("Simulazione basata su aliquote IRPEF 2024 (3 scaglioni) e contributi INPS standard")

    modalita = st.selectbox(
        "Cosa vuoi inserire?",
        ["RAL (Retribuzione Annua Lorda)", "Costo Aziendale", "Calcolatore completo"],
    )

    # Regione
    regione = st.selectbox(
        "Regione di residenza",
        sorted(ADDIZIONALE_REGIONALE.keys()),
        index=sorted(ADDIZIONALE_REGIONALE.keys()).index("Lombardia"),
    )
    aliquota_regionale = ADDIZIONALE_REGIONALE[regione]
    st.caption(f"Addizionale regionale {regione}: {aliquota_regionale * 100:.2f}%")

    # Addizionale comunale
    aliquota_comunale = st.number_input(
        "Addizionale comunale IRPEF (%)",
        min_value=0.0, max_value=0.8, value=0.5, step=0.05,
        help="Varia da 0% a 0,8% in base al comune. Controlla sul sito del tuo comune.",
    ) / 100

    # Carichi familiari
    st.subheader("Carichi familiari")
    col_a, col_b = st.columns(2)
    with col_a:
        coniuge_carico = st.checkbox("Coniuge a carico")
    with col_b:
        n_figli = st.number_input(
            "Figli > 21 anni a carico",
            min_value=0, max_value=10, value=0, step=1,
            help="Figli sotto i 21 anni sono coperti dall'Assegno Unico (non detraibile da IRPEF).",
        )

    mostra_tfr = st.checkbox("Mostra accantonamento TFR", value=True)

    mensilita = 13
    ral = 0.0

    if modalita == "RAL (Retribuzione Annua Lorda)":
        ral = st.number_input("Inserisci la RAL lorda annua (€)", min_value=0.0, value=30_000.0, step=500.0)
        mensilita = st.radio("Numero di mensilità", [13, 14], horizontal=True)

    elif modalita == "Costo Aziendale":
        costo = st.number_input("Inserisci il costo aziendale annuo (€)", min_value=0.0, value=40_000.0, step=500.0)
        mensilita = st.radio("Numero di mensilità", [13, 14], horizontal=True)
        ral = ral_da_costo_aziendale(costo)
        st.info(f"RAL stimata dal costo aziendale: **{fmt(ral)}**")

    elif modalita == "Calcolatore completo":
        ral = st.number_input("Inserisci la RAL lorda annua (€)", min_value=0.0, value=30_000.0, step=500.0)
        mensilita = st.radio("Numero di mensilità", [13, 14], horizontal=True)

    if st.button("Calcola", type="primary", use_container_width=True):
        if ral <= 0:
            st.warning("Inserisci un importo valido maggiore di zero.")
        else:
            r = calcola_netto_annuo(
                ral,
                aliquota_regionale=aliquota_regionale,
                aliquota_comunale=aliquota_comunale,
                coniuge_carico=coniuge_carico,
                n_figli=int(n_figli),
            )
            netto_mensile = r["netto_annuo"] / mensilita
            costo_aziendale = ral * (1 + ALIQUOTA_INPS_AZIENDA)

            st.divider()
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Netto annuo", fmt(r["netto_annuo"]))
            col2.metric(f"Netto mensile ({mensilita} men.)", fmt(netto_mensile))
            col3.metric("RAL", fmt(r["ral"]))
            col4.metric("Costo aziendale", fmt(costo_aziendale))

            st.divider()
            st.subheader("Dettaglio calcolo")

            voci = ["RAL (lordo annuo)"]
            importi = [fmt(r["ral"])]

            voci.append("Contributi INPS dipendente (9,19%)")
            importi.append(f"- {fmt(r['inps_dipendente'])}")

            voci.append("Imponibile IRPEF")
            importi.append(fmt(r["imponibile_irpef"]))

            voci.append("IRPEF lorda")
            importi.append(fmt(r["irpef_lorda"]))

            voci.append("Detrazione lavoro dipendente")
            importi.append(f"- {fmt(r['det_lavoro'])}")

            if coniuge_carico:
                voci.append("Detrazione coniuge a carico")
                importi.append(f"- {fmt(r['det_coniuge'])}")

            if n_figli > 0:
                voci.append(f"Detrazione figli > 21 anni ({int(n_figli)})")
                importi.append(f"- {fmt(r['det_figli'])}")

            voci.append("IRPEF netta")
            importi.append(fmt(r["irpef_netta"]))

            if r["bonus_integrativo"] > 0:
                voci.append("Trattamento integrativo (ex bonus Renzi)")
                importi.append(f"+ {fmt(r['bonus_integrativo'])}")

            voci.append(f"Addizionale regionale {regione} ({r['aliquota_regionale'] * 100:.2f}%)")
            importi.append(f"- {fmt(r['addizionale_regionale'])}")

            voci.append(f"Addizionale comunale ({aliquota_comunale * 100:.2f}%)")
            importi.append(f"- {fmt(r['addizionale_comunale'])}")

            voci.append("**Netto annuo**")
            importi.append(fmt(r["netto_annuo"]))

            voci.append(f"**Netto mensile ({mensilita} mensilità)**")
            importi.append(fmt(netto_mensile))

            st.table({"Voce": voci, "Importo": importi})

            if mostra_tfr:
                st.subheader("TFR (Trattamento di Fine Rapporto)")
                st.table({
                    "Voce": ["Accantonamento TFR annuo (RAL / 13,5)", "TFR mensile"],
                    "Importo": [fmt(r["tfr_annuo"]), fmt(r["tfr_annuo"] / 12)],
                })
                st.caption(
                    "Il TFR non entra nel netto mensile: "
                    "viene erogato alla cessazione del rapporto o come anticipo."
                )

            if modalita == "Costo Aziendale":
                costo_val = ral * (1 + ALIQUOTA_INPS_AZIENDA)
                inps_azienda = costo_val - ral
                st.subheader("Dettaglio costo aziendale")
                st.table({
                    "Voce": ["RAL", "Contributi INPS azienda (~30%)", "Costo aziendale totale"],
                    "Importo": [fmt(ral), fmt(inps_azienda), fmt(costo_val)],
                })


if __name__ == "__main__":
    main()
