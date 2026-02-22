import streamlit as st

# --- Costanti 2024 ---

# Beitragsbemessungsgrenzen (soglie massime contributive)
BBG_RV_ALV = 90_600.0   # Rentenversicherung e Arbeitslosenversicherung (Ovest 2024)
BBG_KV_PV  = 62_100.0   # Krankenversicherung e Pflegeversicherung 2024

# Contributi dipendente (Arbeitnehmer)
RV_AN             = 0.0930   # Rentenversicherung
KV_AN_BASE        = 0.0730   # Krankenversicherung (quota fissa)
KV_ZUSATZ_HALF    = 0.0085   # metà Zusatzbeitrag medio 2024 (1.70% / 2)
PV_AN_BASE        = 0.0170   # Pflegeversicherung (con almeno 1 figlio)
PV_AN_KINDERLOS   = 0.0060   # sovrapprezzo senza figli (≥ 23 anni)
ALV_AN            = 0.0130   # Arbeitslosenversicherung

# Contributi datore (Arbeitgeber)
RV_AG             = 0.0930
KV_AG             = KV_AN_BASE + KV_ZUSATZ_HALF   # 8.15%
PV_AG             = 0.0170
ALV_AG            = 0.0130
UV_AG             = 0.0130   # Unfallversicherung (media settore privato)
INSOLVENZ_AG      = 0.0006   # Insolvenzgeldumlage

AG_EXTRA_TOTAL = RV_AG + KV_AG + PV_AG + ALV_AG + UV_AG + INSOLVENZ_AG

# Lohnsteuer 2024 — zone del polinomio ufficiale BMF
GRZ_1 = 11_604.0    # Grundfreibetrag (Klasse I / II / IV)
GRZ_ZONE1_MAX = 17_005.0
GRZ_ZONE2_MAX = 66_760.0
GRZ_ZONE3_MAX = 277_825.0

# Deduzioni forfettarie
WERBUNGSKOSTEN     = 1_230.0   # tutte le Steuerklassen
SONDERAUSGABEN_STD = 36.0      # Klasse I / II / IV
SONDERAUSGABEN_KL3 = 72.0      # Klasse III

# Alleinerzieher-Entlastungsbetrag (Klasse II)
ALLEINERZIEHER_BASIS  = 4_260.0
ALLEINERZIEHER_ZUSATZ =   240.0   # per ogni figlio oltre il primo

# Solidaritätszuschlag 2024
SOLI_FREIGRENZE        = 17_543.0   # soglia annua Lohnsteuer (raddoppia per Kl. III)
SOLI_MILDERUNGS_FAKTOR = 0.119      # fattore della zona di attenuazione
SOLI_RATE              = 0.0550     # aliquota piena

# Kirchensteuer
BUNDESLAENDER_KIRCHE_8 = {"Bayern", "Baden-Württemberg"}
KIRCHENSTEUER_RATE_8   = 0.080
KIRCHENSTEUER_RATE_9   = 0.090

BUNDESLAENDER = sorted([
    "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen",
    "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen",
    "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen",
    "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen",
])

# Kindergeld 2024
KINDERGELD_PRO_KIND_MONAT = 250.0   # € / Mese / Kind (tutti i figli)


# --- Funzioni di calcolo ---

def _pv_rate_an(n_kinder: int) -> float:
    """Aliquota Pflegeversicherung dipendente in base al numero di figli."""
    if n_kinder == 0:
        return PV_AN_BASE + PV_AN_KINDERLOS          # 2.30% senza figli
    if n_kinder == 1:
        return PV_AN_BASE                            # 1.70%
    # Dal 2° al 5° figlio: riduzione di 0.25% per figlio aggiuntivo
    reduktion = min(n_kinder - 1, 4) * 0.0025
    return PV_AN_BASE - reduktion                    # min 0.70%


def berechne_sv_an(brutto: float, n_kinder: int = 0) -> dict:
    """Calcola i contributi sociali annui del dipendente."""
    pv_rate = _pv_rate_an(n_kinder)
    rv  = min(brutto, BBG_RV_ALV) * RV_AN
    kv  = min(brutto, BBG_KV_PV)  * (KV_AN_BASE + KV_ZUSATZ_HALF)
    pv  = min(brutto, BBG_KV_PV)  * pv_rate
    alv = min(brutto, BBG_RV_ALV) * ALV_AN
    return {
        "rv": rv, "kv": kv, "pv": pv, "alv": alv,
        "pv_rate": pv_rate,
        "total": rv + kv + pv + alv,
    }


def berechne_sv_ag(brutto: float) -> dict:
    """Calcola i contributi sociali annui del datore di lavoro."""
    rv  = min(brutto, BBG_RV_ALV) * RV_AG
    kv  = min(brutto, BBG_KV_PV)  * KV_AG
    pv  = min(brutto, BBG_KV_PV)  * PV_AG
    alv = min(brutto, BBG_RV_ALV) * ALV_AG
    uv  = brutto * UV_AG
    ins = brutto * INSOLVENZ_AG
    extra = rv + kv + pv + alv + uv + ins
    return {
        "rv": rv, "kv": kv, "pv": pv, "alv": alv, "uv": uv, "ins": ins,
        "extra": extra,
        "gesamtkosten": brutto + extra,
    }


def _lohnsteuer_formel(zve: float) -> float:
    """Applica il polinomio ufficiale BMF 2024 allo zvE (Zu versteuerndes Einkommen)."""
    if zve <= GRZ_1:
        return 0.0
    if zve <= GRZ_ZONE1_MAX:
        y = (zve - GRZ_1) / 10_000
        return (979.18 * y + 1_400) * y
    if zve <= GRZ_ZONE2_MAX:
        z = (zve - 17_004) / 10_000
        return (192.59 * z + 2_397) * z + 966.53
    if zve <= GRZ_ZONE3_MAX:
        return 0.42 * zve - 10_602.13
    return 0.45 * zve - 18_936.88


def berechne_lohnsteuer(
    brutto: float, steuerklasse: str, n_kinder: int, sv_an_total: float
) -> dict:
    """Calcola zvE e Lohnsteuer lorda annua."""
    sa = SONDERAUSGABEN_KL3 if steuerklasse == "III" else SONDERAUSGABEN_STD

    alleinerzieher = 0.0
    if steuerklasse == "II" and n_kinder > 0:
        alleinerzieher = ALLEINERZIEHER_BASIS + max(n_kinder - 1, 0) * ALLEINERZIEHER_ZUSATZ

    zve = max(brutto - sv_an_total - WERBUNGSKOSTEN - sa - alleinerzieher, 0.0)

    # Klasse III: formula applicata su metà zvE, poi raddoppiata
    if steuerklasse == "III":
        lohnsteuer = _lohnsteuer_formel(zve / 2) * 2
    else:
        lohnsteuer = _lohnsteuer_formel(zve)

    return {
        "zve": zve,
        "alleinerzieher": alleinerzieher,
        "lohnsteuer": lohnsteuer,
    }


def berechne_soli(lohnsteuer: float, steuerklasse: str) -> float:
    """Calcola il Solidaritätszuschlag 2024 con zona di attenuazione."""
    fz = SOLI_FREIGRENZE * (2 if steuerklasse == "III" else 1)
    if lohnsteuer <= fz:
        return 0.0
    soli_milderung = (lohnsteuer - fz) * SOLI_MILDERUNGS_FAKTOR
    return min(soli_milderung, lohnsteuer * SOLI_RATE)


def berechne_kirchensteuer(lohnsteuer: float, bundesland: str, mitglied: bool) -> float:
    """Calcola la Kirchensteuer (opzionale)."""
    if not mitglied:
        return 0.0
    rate = KIRCHENSTEUER_RATE_8 if bundesland in BUNDESLAENDER_KIRCHE_8 else KIRCHENSTEUER_RATE_9
    return lohnsteuer * rate


def calcola_netto_annuo(
    brutto: float,
    steuerklasse: str = "I",
    bundesland: str = "Nordrhein-Westfalen",
    n_kinder: int = 0,
    kirchenmitglied: bool = False,
) -> dict:
    """Calcola il netto annuo con dettaglio completo."""
    sv_an   = berechne_sv_an(brutto, n_kinder)
    lst     = berechne_lohnsteuer(brutto, steuerklasse, n_kinder, sv_an["total"])
    soli    = berechne_soli(lst["lohnsteuer"], steuerklasse)
    kirche  = berechne_kirchensteuer(lst["lohnsteuer"], bundesland, kirchenmitglied)

    netto = brutto - sv_an["total"] - lst["lohnsteuer"] - soli - kirche

    return {
        "brutto":          brutto,
        "sv_rv":           sv_an["rv"],
        "sv_kv":           sv_an["kv"],
        "sv_pv":           sv_an["pv"],
        "sv_alv":          sv_an["alv"],
        "sv_pv_rate":      sv_an["pv_rate"],
        "sv_total":        sv_an["total"],
        "zve":             lst["zve"],
        "alleinerzieher":  lst["alleinerzieher"],
        "lohnsteuer":      lst["lohnsteuer"],
        "soli":            soli,
        "kirche":          kirche,
        "kirchenmitglied": kirchenmitglied,
        "kindergeld":      n_kinder * KINDERGELD_PRO_KIND_MONAT * 12,
        "netto":           netto,
        "n_kinder":        n_kinder,
        "steuerklasse":    steuerklasse,
    }


def brutto_da_gesamtkosten(kosten: float) -> float:
    """Stima il Jahresbruttolohn a partire dai Gesamtkosten del datore."""
    return kosten / (1 + AG_EXTRA_TOTAL)


# --- UI ---

def render_ui(fmt):
    st.caption(
        "Simulation basierend auf Lohnsteuer 2024 (BMF-Formel), "
        "Sozialversicherungsbeiträge 2024 und Soli-Regelung nach § 3 SolZG"
    )

    modalitaet = st.selectbox(
        "Was möchten Sie berechnen?",
        ["Jahresbruttolohn", "Gesamtkosten Arbeitgeber", "Vollständiger Rechner"],
    )

    col_a, col_b = st.columns(2)
    with col_a:
        steuerklasse = st.selectbox(
            "Steuerklasse",
            ["I", "II", "III", "IV"],
            help=(
                "I: ledig / geschieden / verwitwet\n"
                "II: alleinerziehend\n"
                "III: verheiratet – Hauptverdiener\n"
                "IV: verheiratet – beide berufstätig"
            ),
        )
    with col_b:
        bundesland = st.selectbox(
            "Bundesland",
            BUNDESLAENDER,
            index=BUNDESLAENDER.index("Nordrhein-Westfalen"),
        )

    st.subheader("Familiensituation")
    col_c, col_d = st.columns(2)
    with col_c:
        n_kinder = st.number_input(
            "Anzahl Kinder",
            min_value=0, max_value=8, value=0, step=1,
            help=(
                "Beeinflusst den Pflegeversicherungsbeitrag (Kinderlosenzuschlag entfällt ab 1 Kind). "
                "Das Kindergeld (250 €/Kind/Monat) wird separat ausgewiesen."
            ),
        )
    with col_d:
        kirchenmitglied = st.checkbox(
            "Kirchenmitglied",
            help="Kirchensteuer: 8% in Bayern und Baden-Württemberg, 9% in allen anderen Bundesländern.",
        )

    brutto = 0.0

    if modalitaet == "Jahresbruttolohn":
        brutto = st.number_input("Jahresbruttolohn (€)", min_value=0.0, value=40_000.0, step=500.0)

    elif modalitaet == "Gesamtkosten Arbeitgeber":
        kosten_input = st.number_input(
            "Gesamtkosten Arbeitgeber (€/Jahr)", min_value=0.0, value=55_000.0, step=500.0
        )
        brutto = brutto_da_gesamtkosten(kosten_input)
        st.info(f"Geschätzter Jahresbruttolohn: **{fmt(brutto)}**")

    elif modalitaet == "Vollständiger Rechner":
        brutto = st.number_input("Jahresbruttolohn (€)", min_value=0.0, value=40_000.0, step=500.0)

    if st.button("Berechnen", type="primary", use_container_width=True):
        if brutto <= 0:
            st.warning("Bitte geben Sie einen gültigen Betrag größer als 0 ein.")
        else:
            r    = calcola_netto_annuo(
                brutto,
                steuerklasse=steuerklasse,
                bundesland=bundesland,
                n_kinder=int(n_kinder),
                kirchenmitglied=kirchenmitglied,
            )
            ag   = berechne_sv_ag(brutto)

            st.divider()
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Jahresnettolohn",   fmt(r["netto"]))
            col2.metric("Monatsnettolohn",   fmt(r["netto"] / 12))
            col3.metric("Jahresbruttolohn",  fmt(r["brutto"]))
            col4.metric("Gesamtkosten AG",   fmt(ag["gesamtkosten"]))

            st.divider()
            st.subheader("Steuer- und Abzugsübersicht")

            voci    = []
            importi = []

            voci.append("Jahresbruttolohn")
            importi.append(fmt(r["brutto"]))

            voci.append(f"Rentenversicherung AN ({RV_AN*100:.2f}%, bis {fmt(BBG_RV_ALV)})")
            importi.append(f"- {fmt(r['sv_rv'])}")

            voci.append(f"Krankenversicherung AN ({(KV_AN_BASE+KV_ZUSATZ_HALF)*100:.2f}%, bis {fmt(BBG_KV_PV)})")
            importi.append(f"- {fmt(r['sv_kv'])}")

            voci.append(f"Pflegeversicherung AN ({r['sv_pv_rate']*100:.2f}%, bis {fmt(BBG_KV_PV)})")
            importi.append(f"- {fmt(r['sv_pv'])}")

            voci.append(f"Arbeitslosenversicherung AN ({ALV_AN*100:.2f}%, bis {fmt(BBG_RV_ALV)})")
            importi.append(f"- {fmt(r['sv_alv'])}")

            voci.append("**Sozialversicherung gesamt (AN)**")
            importi.append(f"- {fmt(r['sv_total'])}")

            voci.append(f"Werbungskostenpauschale")
            importi.append(f"- {fmt(WERBUNGSKOSTEN)}")

            sa_val = SONDERAUSGABEN_KL3 if steuerklasse == "III" else SONDERAUSGABEN_STD
            voci.append("Sonderausgaben-Pauschbetrag")
            importi.append(f"- {fmt(sa_val)}")

            if r["alleinerzieher"] > 0:
                voci.append("Alleinerzieher-Entlastungsbetrag")
                importi.append(f"- {fmt(r['alleinerzieher'])}")

            voci.append("**Zu versteuerndes Einkommen (zvE)**")
            importi.append(fmt(r["zve"]))

            voci.append(f"**Lohnsteuer (Steuerklasse {r['steuerklasse']})**")
            importi.append(f"- {fmt(r['lohnsteuer'])}")

            if r["soli"] > 0:
                voci.append(f"Solidaritätszuschlag ({SOLI_RATE*100:.1f}% der Lohnsteuer)")
                importi.append(f"- {fmt(r['soli'])}")
            else:
                voci.append("Solidaritätszuschlag")
                importi.append("— (unter Freigrenze)")

            if r["kirchenmitglied"]:
                ks_rate = 8 if bundesland in BUNDESLAENDER_KIRCHE_8 else 9
                voci.append(f"Kirchensteuer ({ks_rate}% der Lohnsteuer) — {bundesland}")
                importi.append(f"- {fmt(r['kirche'])}")

            voci.append("**Jahresnettolohn**")
            importi.append(fmt(r["netto"]))

            voci.append("**Monatsnettolohn**")
            importi.append(fmt(r["netto"] / 12))

            if r["kindergeld"] > 0:
                voci.append(
                    f"Kindergeld ({int(n_kinder)} Kind{'er' if n_kinder > 1 else ''} "
                    f"× {int(KINDERGELD_PRO_KIND_MONAT)} €/Monat)"
                )
                importi.append(f"+ {fmt(r['kindergeld'])} (von der Familienkasse, separat)")

            st.table({"Posten": voci, "Betrag": importi})

            if r["kindergeld"] > 0:
                st.caption(
                    f"Das Kindergeld ({fmt(r['kindergeld'])}/Jahr) wird direkt von der Familienkasse "
                    "ausgezahlt und ist nicht im Nettolohn enthalten. Der Kinderfreibetrag wird im Rahmen "
                    "der jährlichen Einkommensteuererklärung geprüft, falls dieser günstiger ist."
                )

            # Arbeitgeberkosten
            st.subheader("Arbeitgeberkosten (Gesamtkostenübersicht)")
            st.table({
                "Posten": [
                    "Jahresbruttolohn",
                    f"Rentenversicherung AG ({RV_AG*100:.2f}%)",
                    f"Krankenversicherung AG ({KV_AG*100:.2f}%)",
                    f"Pflegeversicherung AG ({PV_AG*100:.2f}%)",
                    f"Arbeitslosenversicherung AG ({ALV_AG*100:.2f}%)",
                    f"Unfallversicherung (ca. {UV_AG*100:.2f}%, Durchschnitt)",
                    f"Insolvenzgeldumlage ({INSOLVENZ_AG*100:.2f}%)",
                    f"**Arbeitgeberanteil gesamt (ca. {AG_EXTRA_TOTAL*100:.1f}%)**",
                    "**Gesamtkosten Arbeitgeber**",
                ],
                "Betrag": [
                    fmt(r["brutto"]),
                    fmt(ag["rv"]),
                    fmt(ag["kv"]),
                    fmt(ag["pv"]),
                    fmt(ag["alv"]),
                    fmt(ag["uv"]),
                    fmt(ag["ins"]),
                    fmt(ag["extra"]),
                    fmt(ag["gesamtkosten"]),
                ],
            })

            st.caption(
                "⚠️ Vereinfachte Schätzung. Der Unfallversicherungsbeitrag variiert je nach "
                "Berufsgenossenschaft und Branche. Die Kirchensteuer ist optional. "
                "Der Pflegeversicherungsbeitrag gilt für Arbeitnehmer ≥ 23 Jahre."
            )
