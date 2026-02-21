import streamlit as st

# --- Costanti Seguridad Social ---

# Cotizaciones empleado 2024
SS_CONTINGENCIAS  = 0.0470
SS_DESEMPLEO      = 0.0155
SS_FP             = 0.0010
SS_TOTAL_EMPLEADO = SS_CONTINGENCIAS + SS_DESEMPLEO + SS_FP  # 6.35%

# Cotizaciones empresa 2024 (stima media)
SS_CONTINGENCIAS_EMPRESA = 0.2360
SS_DESEMPLEO_EMPRESA     = 0.0555
SS_FOGASA                = 0.0020
SS_FP_EMPRESA            = 0.0060
SS_MEI                   = 0.0050  # Mecanismo de Equidad Intergeneracional
SS_TOTAL_EMPRESA         = (
    SS_CONTINGENCIAS_EMPRESA + SS_DESEMPLEO_EMPRESA +
    SS_FOGASA + SS_FP_EMPRESA + SS_MEI
)  # ~30.45%

# --- Scaglioni IRPF statali 2024 (escala general estatal) ---
# Fissi, uguali in tutta la Spagna
SCAGLIONI_IRPF_ESTADO = [
    (12_450,       0.0950),
    (20_200,       0.1200),
    (35_200,       0.1500),
    (60_000,       0.1850),
    (300_000,      0.2250),
    (float("inf"), 0.2450),
]

# --- Scaglioni IRPF autonomici 2024 (escala autonómica) ---
# None = usa scaglioni statali come approssimazione
SCAGLIONI_IRPF_AUTONOMICO = {
    "Andalucía": [
        (12_450,       0.0950),
        (20_200,       0.1200),
        (35_200,       0.1500),
        (60_000,       0.1850),
        (float("inf"), 0.2250),
    ],
    "Aragón": [
        (12_450,       0.1000),
        (20_200,       0.1200),
        (34_000,       0.1400),
        (50_000,       0.1800),
        (70_000,       0.2200),
        (float("inf"), 0.2400),
    ],
    "Asturias": [
        (12_450,       0.1000),
        (17_707,       0.1200),
        (33_007,       0.1400),
        (53_407,       0.1870),
        (70_000,       0.2150),
        (90_000,       0.2350),
        (175_000,      0.2400),
        (float("inf"), 0.2500),
    ],
    "Baleares": [
        (10_000,       0.0900),
        (18_000,       0.1150),
        (30_000,       0.1400),
        (48_000,       0.1750),
        (70_000,       0.2000),
        (float("inf"), 0.2350),
    ],
    "Canarias": [
        (12_450,       0.0900),
        (20_200,       0.1175),
        (35_200,       0.1400),
        (60_000,       0.1825),
        (float("inf"), 0.2250),
    ],
    "Cantabria": [
        (12_450,       0.0990),
        (20_200,       0.1200),
        (35_200,       0.1500),
        (60_000,       0.1850),
        (90_000,       0.2150),
        (float("inf"), 0.2350),
    ],
    "Castilla-La Mancha": [
        (12_450,       0.0950),
        (20_200,       0.1200),
        (35_200,       0.1500),
        (60_000,       0.1850),
        (float("inf"), 0.2250),
    ],
    "Castilla y León": [
        (12_450,       0.0950),
        (20_200,       0.1200),
        (35_200,       0.1500),
        (60_000,       0.1850),
        (float("inf"), 0.2250),
    ],
    "Cataluña": [
        (12_450,       0.1050),
        (17_707,       0.1200),
        (21_000,       0.1400),
        (33_007,       0.1500),
        (53_407,       0.1880),
        (90_000,       0.2150),
        (120_000,      0.2350),
        (175_000,      0.2450),
        (float("inf"), 0.2550),
    ],
    "Comunidad Valenciana": [
        (12_000,       0.1000),
        (17_707,       0.1150),
        (33_007,       0.1415),
        (53_407,       0.1850),
        (120_000,      0.2250),
        (175_000,      0.2350),
        (float("inf"), 0.2500),
    ],
    "Extremadura": [
        (12_450,       0.0800),
        (20_200,       0.1175),
        (35_200,       0.1500),
        (60_000,       0.1925),
        (120_000,      0.2175),
        (float("inf"), 0.2500),
    ],
    "Galicia": [
        (12_450,       0.0950),
        (20_200,       0.1200),
        (35_200,       0.1500),
        (60_000,       0.1850),
        (70_000,       0.2150),
        (float("inf"), 0.2350),
    ],
    "La Rioja": [
        (12_450,       0.0900),
        (20_200,       0.1200),
        (35_200,       0.1500),
        (60_000,       0.1850),
        (float("inf"), 0.2250),
    ],
    "Madrid": [
        (12_450,       0.0900),
        (17_707,       0.1125),
        (33_007,       0.1330),
        (53_407,       0.1790),
        (120_000,      0.2100),
        (175_000,      0.2250),
        (float("inf"), 0.2400),
    ],
    "Murcia": [
        (12_450,       0.0950),
        (20_200,       0.1200),
        (35_200,       0.1500),
        (60_000,       0.1850),
        (float("inf"), 0.2250),
    ],
    "Navarra (régimen foral, aprox.)": [
        (13_590,       0.1300),
        (32_500,       0.2400),
        (52_360,       0.3200),
        (float("inf"), 0.3700),
    ],
    "País Vasco (régimen foral, aprox.)": [
        (17_140,       0.2300),
        (33_900,       0.2800),
        (72_000,       0.3500),
        (float("inf"), 0.4500),
    ],
}

# --- Minimi personali e familiari ---
MINIMO_PERSONAL   = 5_550.0
MINIMO_HIJOS      = [2_400.0, 2_700.0, 4_000.0, 4_500.0]  # 1°, 2°, 3°, 4°+
REDUCCION_CONJUNTA = 3_400.0  # tributación conjunta (cónyuge no trabaja)

# --- Parametri riduzione rendimenti del lavoro ---
REDUCCION_MAX     = 5_565.0
REDUCCION_MIN     = 1_000.0
REDUCCION_UMBRAL1 = 13_115.0
REDUCCION_UMBRAL2 = 16_825.0


# --- Funzioni di calcolo ---

def _aplica_scaglioni(base: float, brackets: list) -> float:
    """Applica scaglioni progressivi a base. Restituisce l'imposta totale."""
    imposta = 0.0
    precedente = 0.0
    for limite, aliquota in brackets:
        scaglione = min(base, limite) - precedente
        if scaglione <= 0:
            break
        imposta += scaglione * aliquota
        precedente = limite
    return imposta


def ss_empleado(sba: float) -> dict:
    """Calcola le cotizaciones a la Seguridad Social del empleado."""
    contingencias = sba * SS_CONTINGENCIAS
    desempleo     = sba * SS_DESEMPLEO
    fp            = sba * SS_FP
    total         = contingencias + desempleo + fp
    return {
        "contingencias": contingencias,
        "desempleo":     desempleo,
        "fp":            fp,
        "total":         total,
    }


def calcola_coste_empresa(sba: float) -> dict:
    """Calcola il costo aziendale totale a partire dal SBA."""
    contingencias = sba * SS_CONTINGENCIAS_EMPRESA
    desempleo     = sba * SS_DESEMPLEO_EMPRESA
    fogasa        = sba * SS_FOGASA
    fp            = sba * SS_FP_EMPRESA
    mei           = sba * SS_MEI
    total_ss      = contingencias + desempleo + fogasa + fp + mei
    return {
        "contingencias_empresa": contingencias,
        "desempleo_empresa":     desempleo,
        "fogasa":                fogasa,
        "fp_empresa":            fp,
        "mei":                   mei,
        "total_ss_empresa":      total_ss,
        "coste_total":           sba + total_ss,
    }


def reduccion_trabajo(base_imponible: float) -> float:
    """Reducción por rendimientos del trabajo (art. 20 LIRPF 2024)."""
    if base_imponible <= REDUCCION_UMBRAL1:
        return REDUCCION_MAX
    elif base_imponible <= REDUCCION_UMBRAL2:
        exceso = base_imponible - REDUCCION_UMBRAL1
        return max(REDUCCION_MAX - 1.5 * exceso, 0.0)
    return REDUCCION_MIN


def minimo_personal_familiar(n_hijos: int, conjunta: bool) -> float:
    """Calcola il mínimo personal y familiar."""
    mpf = MINIMO_PERSONAL
    for i in range(n_hijos):
        mpf += MINIMO_HIJOS[min(i, 3)]
    if conjunta:
        mpf += REDUCCION_CONJUNTA
    return mpf


def irpf_sobre_base(base: float, comunidad: str) -> float:
    """Applica scaglioni statali + autonomici a base. Restituisce imposta totale."""
    brackets_auto = SCAGLIONI_IRPF_AUTONOMICO.get(comunidad)
    if brackets_auto is None:
        brackets_auto = SCAGLIONI_IRPF_ESTADO
    return _aplica_scaglioni(base, SCAGLIONI_IRPF_ESTADO) + _aplica_scaglioni(base, brackets_auto)


def calcola_netto_annuo(
    sba: float,
    comunidad: str,
    n_hijos: int = 0,
    conjunta: bool = False,
    num_pagas: int = 14,
) -> dict:
    """Calcola il salario neto anual con dettaglio completo."""
    ss = ss_empleado(sba)
    ss_total = ss["total"]

    base_imponible    = sba - ss_total
    red_trabajo       = reduccion_trabajo(base_imponible)
    rendimientos_netos = max(base_imponible - red_trabajo, 0.0)

    mpf = minimo_personal_familiar(n_hijos, conjunta)

    irpf_rn  = irpf_sobre_base(rendimientos_netos, comunidad)
    irpf_mpf = irpf_sobre_base(min(mpf, rendimientos_netos), comunidad)
    irpf_total = max(irpf_rn - irpf_mpf, 0.0)

    netto_annuo = sba - ss_total - irpf_total
    neto_paga   = netto_annuo / num_pagas

    return {
        "sba":               sba,
        "ss_contingencias":  ss["contingencias"],
        "ss_desempleo":      ss["desempleo"],
        "ss_fp":             ss["fp"],
        "ss_total":          ss_total,
        "base_imponible":    base_imponible,
        "red_trabajo":       red_trabajo,
        "rendimientos_netos": rendimientos_netos,
        "mpf":               mpf,
        "n_hijos":           n_hijos,
        "conjunta":          conjunta,
        "irpf_rn":           irpf_rn,
        "irpf_mpf":          irpf_mpf,
        "irpf_total":        irpf_total,
        "netto_annuo":       netto_annuo,
        "neto_paga":         neto_paga,
        "num_pagas":         num_pagas,
        "comunidad":         comunidad,
    }


def sba_da_coste_empresa(coste: float) -> float:
    """Calcola il SBA a partire dal costo aziendale."""
    return coste / (1 + SS_TOTAL_EMPRESA)


# --- UI ---

def render_ui(fmt):
    st.caption("Simulación basada en el IRPF 2024 y cotizaciones a la Seguridad Social")

    modalidad = st.selectbox(
        "¿Qué quieres calcular?",
        ["Salario Bruto Anual (SBA)", "Coste Empresa", "Calculador Completo"],
    )

    # Comunidad Autónoma
    comunidades = sorted(SCAGLIONI_IRPF_AUTONOMICO.keys())
    comunidad = st.selectbox(
        "Comunidad Autónoma de residencia",
        comunidades,
        index=comunidades.index("Madrid"),
    )

    # Situación familiar
    st.subheader("Situación familiar")
    col_a, col_b = st.columns(2)
    with col_a:
        conjunta = st.checkbox(
            "Tributación conjunta",
            help="Selecciona si tu cónyuge no trabaja o tiene ingresos muy bajos. "
                 "Añade 3.400 € al mínimo personal y familiar.",
        )
    with col_b:
        n_hijos = st.number_input(
            "Hijos a cargo",
            min_value=0, max_value=6, value=0, step=1,
            help="Número de hijos dependientes. Cada hijo reduce la base imponible del IRPF.",
        )

    num_pagas = st.radio("Número de pagas", [12, 14], horizontal=True,
                         help="14 pagas = 12 mensuales + paga extra de verano y Navidad.")

    sba = 0.0

    if modalidad == "Salario Bruto Anual (SBA)":
        sba = st.number_input("Salario Bruto Anual (€)", min_value=0.0, value=30_000.0, step=500.0)

    elif modalidad == "Coste Empresa":
        coste_input = st.number_input("Coste empresa anual (€)", min_value=0.0, value=40_000.0, step=500.0)
        sba = sba_da_coste_empresa(coste_input)
        st.info(f"SBA estimado del coste empresa: **{fmt(sba)}**")

    elif modalidad == "Calculador Completo":
        sba = st.number_input("Salario Bruto Anual (€)", min_value=0.0, value=30_000.0, step=500.0)

    if st.button("Calcular", type="primary", use_container_width=True):
        if sba <= 0:
            st.warning("Introduce un importe válido mayor de cero.")
        else:
            r = calcola_netto_annuo(
                sba,
                comunidad=comunidad,
                n_hijos=int(n_hijos),
                conjunta=conjunta,
                num_pagas=num_pagas,
            )
            coste_emp = calcola_coste_empresa(sba)

            st.divider()
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Neto anual",                        fmt(r["netto_annuo"]))
            col2.metric(f"Neto por paga ({num_pagas} pagas)", fmt(r["neto_paga"]))
            col3.metric("Salario Bruto Anual",               fmt(r["sba"]))
            col4.metric("Coste empresa",                     fmt(coste_emp["coste_total"]))

            st.divider()
            st.subheader("Desglose del cálculo IRPF")

            voci    = []
            importi = []

            voci.append("Salario Bruto Anual (SBA)")
            importi.append(fmt(r["sba"]))

            voci.append(f"SS empleado - Contingencias comunes ({SS_CONTINGENCIAS*100:.2f}%)")
            importi.append(f"- {fmt(r['ss_contingencias'])}")

            voci.append(f"SS empleado - Desempleo ({SS_DESEMPLEO*100:.2f}%)")
            importi.append(f"- {fmt(r['ss_desempleo'])}")

            voci.append(f"SS empleado - Formación Profesional ({SS_FP*100:.2f}%)")
            importi.append(f"- {fmt(r['ss_fp'])}")

            voci.append(f"**Total SS empleado ({SS_TOTAL_EMPLEADO*100:.2f}%)**")
            importi.append(f"- {fmt(r['ss_total'])}")

            voci.append("Base imponible (SBA − SS empleado)")
            importi.append(fmt(r["base_imponible"]))

            voci.append("Reducción por rendimientos del trabajo")
            importi.append(f"- {fmt(r['red_trabajo'])}")

            voci.append("Rendimientos netos del trabajo")
            importi.append(fmt(r["rendimientos_netos"]))

            mpf_desc = "Personal 5.550 €"
            if r["n_hijos"] > 0:
                mpf_desc += f" + hijos ({r['n_hijos']})"
            if r["conjunta"]:
                mpf_desc += " + conjunta 3.400 €"
            voci.append(f"Mínimo personal y familiar  [{mpf_desc}]")
            importi.append(fmt(r["mpf"]))

            voci.append("IRPF sobre rendimientos netos (estado + CCAA)")
            importi.append(fmt(r["irpf_rn"]))

            voci.append("Deducción por mínimo personal y familiar")
            importi.append(f"- {fmt(r['irpf_mpf'])}")

            voci.append(f"**IRPF total — {comunidad}**")
            importi.append(f"- {fmt(r['irpf_total'])}")

            voci.append("**Salario Neto Anual**")
            importi.append(fmt(r["netto_annuo"]))

            voci.append(f"**Neto por paga ({num_pagas} pagas)**")
            importi.append(fmt(r["neto_paga"]))

            st.table({"Concepto": voci, "Importe": importi})

            if num_pagas == 14:
                st.caption(
                    "Con 14 pagas, las 2 pagas extra (verano y Navidad) ya están incluidas "
                    "en el bruto y en el neto anual. No existe el TFR italiano: "
                    "las pagas extra se cobran en el mismo año fiscal."
                )

            # Dettaglio coste empresa (sempre visibile)
            st.subheader("Desglose coste empresa")
            st.table({
                "Concepto": [
                    "Salario Bruto Anual (SBA)",
                    f"SS empresa - Contingencias comunes ({SS_CONTINGENCIAS_EMPRESA*100:.2f}%)",
                    f"SS empresa - Desempleo ({SS_DESEMPLEO_EMPRESA*100:.2f}%)",
                    f"SS empresa - FOGASA ({SS_FOGASA*100:.2f}%)",
                    f"SS empresa - Formación Profesional ({SS_FP_EMPRESA*100:.2f}%)",
                    f"SS empresa - MEI ({SS_MEI*100:.2f}%)",
                    f"**Total SS empresa ({SS_TOTAL_EMPRESA*100:.2f}%)**",
                    "**Coste empresa total**",
                ],
                "Importe": [
                    fmt(r["sba"]),
                    fmt(coste_emp["contingencias_empresa"]),
                    fmt(coste_emp["desempleo_empresa"]),
                    fmt(coste_emp["fogasa"]),
                    fmt(coste_emp["fp_empresa"]),
                    fmt(coste_emp["mei"]),
                    fmt(coste_emp["total_ss_empresa"]),
                    fmt(coste_emp["coste_total"]),
                ],
            })
