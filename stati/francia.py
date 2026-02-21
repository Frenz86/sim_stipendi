import streamlit as st

# --- Costanti 2024 ---

# PASS: Plafond Annuel de la Sécurité Sociale
PASS = 46_368.0

# Assiette CSG/CRDS = 98.25% del lordo
ASSIETTE_CSG = 0.9825

# CSG/CRDS (applicati sull'assiette)
CSG_DEDUCTIBLE    = 0.0680   # 6.80% — deducibile dall'IR
CSG_NON_DEDUCTIBLE = 0.0240  # 2.40% — non deducibile
CRDS              = 0.0050   # 0.50% — non deducibile

# Tranche 1: porzione di salario fino a 1×PASS
SECU_VIEIL_PLAF   = 0.0690   # Retraite sécu plafonnée
SECU_VIEIL_DEPLAF = 0.0040   # Retraite sécu déplafonnée (su tutto il lordo)
AGIRC_T1          = 0.0315   # AGIRC-ARRCO T1
CEG_T1            = 0.0086   # Contribution d'Équilibre Général T1

# Tranche 2: porzione tra 1×PASS e 8×PASS
AGIRC_T2 = 0.0864   # AGIRC-ARRCO T2
CEG_T2   = 0.0108   # CEG T2
CET      = 0.0014   # Contribution d'Équilibre Technique

# Charges patronales 2024 (media settore privato, semplificate)
PAT_MALADIE      = 0.1300
PAT_VIEIL_PLAF   = 0.0855
PAT_VIEIL_DEPLAF = 0.0202
PAT_FAMILLE      = 0.0525
PAT_AT_MP        = 0.0200   # variabile per settore, usiamo media
PAT_CHOMAGE      = 0.0405
PAT_AGS          = 0.0015
PAT_AGIRC_T1     = 0.0472
PAT_CEG_T1       = 0.0129
PAT_FORMATION    = 0.0100
PAT_TOTAL = (
    PAT_MALADIE + PAT_VIEIL_PLAF + PAT_VIEIL_DEPLAF + PAT_FAMILLE +
    PAT_AT_MP + PAT_CHOMAGE + PAT_AGS + PAT_AGIRC_T1 + PAT_CEG_T1 + PAT_FORMATION
)  # ~42%

# Barème IR 2024
BAREME_IR = [
    (11_294,       0.00),
    (28_797,       0.11),
    (82_341,       0.30),
    (177_106,      0.41),
    (float("inf"), 0.45),
]

# Abattement forfaitaire pour frais professionnels
ABATTEMENT_RATE = 0.10
ABATTEMENT_MIN  = 495.0
ABATTEMENT_MAX  = 14_171.0

# Décote 2024 (riduzione IR per redditi bassi)
DECOTE_CELIBATAIRE = 1_840.0
DECOTE_COUPLE      = 3_045.0
DECOTE_RATE        = 0.75

# Plafonnement du quotient familial 2024
PLAFOND_DEMI_PART = 1_759.0  # max riduzione IR per demi-part supplementare


# --- Funzioni di calcolo ---

def _applique_bareme(base: float) -> float:
    """Applica il barème IR progressivo a base (reddito per 1 part)."""
    imposta = 0.0
    precedente = 0.0
    for limite, aliquota in BAREME_IR:
        scaglione = min(base, limite) - precedente
        if scaglione <= 0:
            break
        imposta += scaglione * aliquota
        precedente = limite
    return imposta


def cotisations_salariales(brut: float) -> dict:
    """
    Calcola le cotisations salariales con distinzione T1/T2 e CSG/CRDS.
    Restituisce dict con ogni componente e i totali deducibile/non-deducibile.
    """
    t1 = min(brut, PASS)        # porzione T1
    t2 = max(brut - PASS, 0.0)  # porzione T2
    assiette = brut * ASSIETTE_CSG

    # Tranche 1
    secu_plaf  = t1 * SECU_VIEIL_PLAF
    secu_deplaf = brut * SECU_VIEIL_DEPLAF  # su tutto il lordo
    agirc_t1   = t1 * AGIRC_T1
    ceg_t1_val = t1 * CEG_T1

    # Tranche 2 (se applicabile)
    agirc_t2   = t2 * AGIRC_T2
    ceg_t2_val = t2 * CEG_T2
    cet_val    = t2 * CET

    # CSG / CRDS (su assiette)
    csg_ded     = assiette * CSG_DEDUCTIBLE
    csg_non_ded = assiette * CSG_NON_DEDUCTIBLE
    crds_val    = assiette * CRDS

    # Totali
    cotis_deductibili = secu_plaf + secu_deplaf + agirc_t1 + ceg_t1_val + agirc_t2 + ceg_t2_val + cet_val + csg_ded
    cotis_non_ded     = csg_non_ded + crds_val
    total             = cotis_deductibili + cotis_non_ded

    return {
        "secu_plaf":    secu_plaf,
        "secu_deplaf":  secu_deplaf,
        "agirc_t1":     agirc_t1,
        "ceg_t1":       ceg_t1_val,
        "agirc_t2":     agirc_t2,
        "ceg_t2":       ceg_t2_val,
        "cet":          cet_val,
        "csg_ded":      csg_ded,
        "csg_non_ded":  csg_non_ded,
        "crds":         crds_val,
        "deductibili":  cotis_deductibili,
        "non_deductibili": cotis_non_ded,
        "total":        total,
        "sopra_pass":   t2 > 0,
    }


def charges_patronales(brut: float) -> dict:
    """Calcola le charges patronales (semplificate, media settore privato)."""
    maladie  = brut * PAT_MALADIE
    vieil    = brut * (PAT_VIEIL_PLAF + PAT_VIEIL_DEPLAF)
    famille  = brut * PAT_FAMILLE
    at_mp    = brut * PAT_AT_MP
    chomage  = brut * PAT_CHOMAGE
    ags      = brut * PAT_AGS
    agirc    = brut * (PAT_AGIRC_T1 + PAT_CEG_T1)
    formation = brut * PAT_FORMATION
    total_pat = brut * PAT_TOTAL
    return {
        "maladie":   maladie,
        "vieil":     vieil,
        "famille":   famille,
        "at_mp":     at_mp,
        "chomage":   chomage,
        "ags":       ags,
        "agirc":     agirc,
        "formation": formation,
        "total":     total_pat,
        "cout_total": brut + total_pat,
    }


def nb_parts(situation: str, n_enfants: int) -> float:
    """Calcola il nombre de parts fiscales (quotient familial)."""
    if situation == "Couple (marié·e / pacsé·e)":
        parts = 2.0
    elif situation == "Parent isolé":
        parts = 1.5
    else:
        parts = 1.0
    for i in range(n_enfants):
        parts += 0.5 if i < 2 else 1.0
    return parts


def calcola_ir(revenu_net_imposable: float, situation: str, n_enfants: int) -> dict:
    """
    Calcola l'Impôt sur le Revenu con quotient familial, plafonnement e décote.
    """
    nombre_parts = nb_parts(situation, n_enfants)
    parts_ref = 2.0 if situation == "Couple (marié·e / pacsé·e)" else 1.0
    demi_parts_supp = (nombre_parts - parts_ref) * 2

    # IR con quotient familial
    ir_avec_famille = _applique_bareme(revenu_net_imposable / nombre_parts) * nombre_parts

    # IR di riferimento (senza figli)
    ir_reference = _applique_bareme(revenu_net_imposable / parts_ref) * parts_ref

    # Plafonnement du quotient familial
    if demi_parts_supp > 0:
        gain = ir_reference - ir_avec_famille
        plafond = PLAFOND_DEMI_PART * demi_parts_supp
        if gain > plafond:
            ir_apres_quotient = ir_reference - plafond
        else:
            ir_apres_quotient = ir_avec_famille
    else:
        ir_apres_quotient = ir_avec_famille

    # Décote
    limite_decote = DECOTE_COUPLE if situation == "Couple (marié·e / pacsé·e)" else DECOTE_CELIBATAIRE
    if ir_apres_quotient <= limite_decote:
        decote = max(0.0, limite_decote - DECOTE_RATE * ir_apres_quotient)
    else:
        decote = 0.0
    ir_net = max(ir_apres_quotient - decote, 0.0)

    return {
        "nombre_parts":       nombre_parts,
        "ir_brut":            ir_reference,
        "ir_apres_quotient":  ir_apres_quotient,
        "decote":             decote,
        "ir_net":             ir_net,
    }


def calcola_netto_annuo(
    brut: float,
    situation: str,
    n_enfants: int = 0,
    num_mois: int = 12,
) -> dict:
    """Calcola il salaire net annuel con dettaglio completo."""
    cotis = cotisations_salariales(brut)

    revenu_brut_imposable = brut - cotis["deductibili"]
    abattement = max(ABATTEMENT_MIN, min(revenu_brut_imposable * ABATTEMENT_RATE, ABATTEMENT_MAX))
    revenu_net_imposable = max(revenu_brut_imposable - abattement, 0.0)

    ir = calcola_ir(revenu_net_imposable, situation, n_enfants)

    net_annuel = brut - cotis["total"] - ir["ir_net"]
    net_mensuel = net_annuel / num_mois

    return {
        "brut":                   brut,
        "secu_plaf":              cotis["secu_plaf"],
        "secu_deplaf":            cotis["secu_deplaf"],
        "agirc_t1":               cotis["agirc_t1"],
        "ceg_t1":                 cotis["ceg_t1"],
        "agirc_t2":               cotis["agirc_t2"],
        "ceg_t2":                 cotis["ceg_t2"],
        "cet":                    cotis["cet"],
        "csg_ded":                cotis["csg_ded"],
        "csg_non_ded":            cotis["csg_non_ded"],
        "crds":                   cotis["crds"],
        "cotis_total":            cotis["total"],
        "sopra_pass":             cotis["sopra_pass"],
        "revenu_brut_imposable":  revenu_brut_imposable,
        "abattement":             abattement,
        "revenu_net_imposable":   revenu_net_imposable,
        "nombre_parts":           ir["nombre_parts"],
        "ir_brut":                ir["ir_brut"],
        "ir_apres_quotient":      ir["ir_apres_quotient"],
        "decote":                 ir["decote"],
        "ir_net":                 ir["ir_net"],
        "net_annuel":             net_annuel,
        "net_mensuel":            net_mensuel,
        "num_mois":               num_mois,
        "situation":              situation,
        "n_enfants":              n_enfants,
    }


def brut_da_cout_totale(cout: float) -> float:
    """Stima il salaire brut a partire dal coût employeur totale."""
    return cout / (1 + PAT_TOTAL)


# --- UI ---

def render_ui(fmt):
    st.caption(
        "Simulation basée sur le barème IR 2024, cotisations sociales 2024 "
        "et le PASS 2024 (46 368 €)"
    )

    modalite = st.selectbox(
        "Que souhaitez-vous saisir ?",
        ["Salaire Brut Annuel", "Coût Employeur", "Calculateur Complet"],
    )

    # Situation familiale
    st.subheader("Situation familiale")
    col_a, col_b = st.columns(2)
    with col_a:
        situation = st.selectbox(
            "Situation",
            ["Célibataire", "Couple (marié·e / pacsé·e)", "Parent isolé"],
            help="Détermine le nombre de parts fiscales pour le quotient familial.",
        )
    with col_b:
        n_enfants = st.number_input(
            "Enfants à charge",
            min_value=0, max_value=6, value=0, step=1,
            help="Chaque enfant ajoute 0,5 part (1re et 2e) ou 1 part (3e et suivants).",
        )

    num_mois = st.radio(
        "Nombre de mois",
        [12, 13],
        horizontal=True,
        help="13 mois si votre convention collective prévoit une prime de fin d'année.",
    )

    brut = 0.0

    if modalite == "Salaire Brut Annuel":
        brut = st.number_input("Salaire Brut Annuel (€)", min_value=0.0, value=35_000.0, step=500.0)

    elif modalite == "Coût Employeur":
        cout_input = st.number_input("Coût employeur annuel (€)", min_value=0.0, value=50_000.0, step=500.0)
        brut = brut_da_cout_totale(cout_input)
        st.info(f"Salaire brut estimé depuis le coût employeur : **{fmt(brut)}**")

    elif modalite == "Calculateur Complet":
        brut = st.number_input("Salaire Brut Annuel (€)", min_value=0.0, value=35_000.0, step=500.0)

    if st.button("Calculer", type="primary", use_container_width=True):
        if brut <= 0:
            st.warning("Veuillez saisir un montant valide supérieur à zéro.")
        else:
            r = calcola_netto_annuo(
                brut,
                situation=situation,
                n_enfants=int(n_enfants),
                num_mois=num_mois,
            )
            charges = charges_patronales(brut)

            st.divider()
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Net annuel",                          fmt(r["net_annuel"]))
            col2.metric(f"Net mensuel ({num_mois} mois)",     fmt(r["net_mensuel"]))
            col3.metric("Salaire brut",                        fmt(r["brut"]))
            col4.metric("Coût employeur",                      fmt(charges["cout_total"]))

            st.divider()
            st.subheader("Détail du calcul")

            voci    = []
            importi = []

            voci.append("Salaire brut annuel")
            importi.append(fmt(r["brut"]))

            voci.append(f"Retraite sécu plafonnée ({SECU_VIEIL_PLAF*100:.2f}%, jusqu'au PASS)")
            importi.append(f"- {fmt(r['secu_plaf'])}")

            voci.append(f"Retraite sécu déplafonnée ({SECU_VIEIL_DEPLAF*100:.2f}%)")
            importi.append(f"- {fmt(r['secu_deplaf'])}")

            voci.append(f"AGIRC-ARRCO T1 + CEG ({(AGIRC_T1+CEG_T1)*100:.2f}%, jusqu'au PASS)")
            importi.append(f"- {fmt(r['agirc_t1'] + r['ceg_t1'])}")

            if r["sopra_pass"]:
                voci.append(f"AGIRC-ARRCO T2 + CEG + CET ({(AGIRC_T2+CEG_T2+CET)*100:.2f}%, au-delà du PASS)")
                importi.append(f"- {fmt(r['agirc_t2'] + r['ceg_t2'] + r['cet'])}")

            voci.append(f"CSG déductible ({CSG_DEDUCTIBLE*100:.2f}% × 98,25%)")
            importi.append(f"- {fmt(r['csg_ded'])}")

            voci.append(f"CSG non déductible ({CSG_NON_DEDUCTIBLE*100:.2f}% × 98,25%)")
            importi.append(f"- {fmt(r['csg_non_ded'])}")

            voci.append(f"CRDS ({CRDS*100:.2f}% × 98,25%)")
            importi.append(f"- {fmt(r['crds'])}")

            voci.append("**Total cotisations salariales**")
            importi.append(f"- {fmt(r['cotis_total'])}")

            voci.append("Revenu brut imposable (brut − cotis. déductibles)")
            importi.append(fmt(r["revenu_brut_imposable"]))

            voci.append("Abattement forfaitaire 10% (frais professionnels)")
            importi.append(f"- {fmt(r['abattement'])}")

            voci.append("Revenu net imposable")
            importi.append(fmt(r["revenu_net_imposable"]))

            parts_detail = f"{r['nombre_parts']:.1f} part(s)"
            if n_enfants > 0:
                parts_detail += f" — {int(n_enfants)} enfant(s)"
            voci.append(f"Quotient familial  [{parts_detail}]")
            importi.append("")

            voci.append("IR brut (barème sans quotient familial)")
            importi.append(fmt(r["ir_brut"]))

            if r["ir_apres_quotient"] < r["ir_brut"]:
                gain = r["ir_brut"] - r["ir_apres_quotient"]
                voci.append("Réduction quotient familial")
                importi.append(f"- {fmt(gain)}")

            if r["decote"] > 0:
                voci.append("Décote")
                importi.append(f"- {fmt(r['decote'])}")

            voci.append("**IR net (prélèvement à la source)**")
            importi.append(f"- {fmt(r['ir_net'])}")

            voci.append("**Salaire Net Annuel**")
            importi.append(fmt(r["net_annuel"]))

            voci.append(f"**Net mensuel ({num_mois} mois)**")
            importi.append(fmt(r["net_mensuel"]))

            st.table({"Poste": voci, "Montant": importi})

            if num_mois == 13:
                st.caption(
                    "13 mois : la prime de fin d'année est incluse dans le brut et le net annuel. "
                    "Le net mensuel affiché correspond à 1/13 du net annuel."
                )

            # Charges patronales
            st.subheader("Charges patronales (coût employeur)")
            st.table({
                "Poste": [
                    "Salaire brut",
                    f"Maladie, mat., inval., décès ({PAT_MALADIE*100:.2f}%)",
                    f"Vieillesse ({(PAT_VIEIL_PLAF+PAT_VIEIL_DEPLAF)*100:.2f}%)",
                    f"Allocations familiales ({PAT_FAMILLE*100:.2f}%)",
                    f"Accidents du travail / MP ({PAT_AT_MP*100:.2f}%, moy.)",
                    f"Assurance chômage ({PAT_CHOMAGE*100:.2f}%)",
                    f"AGS ({PAT_AGS*100:.2f}%)",
                    f"AGIRC-ARRCO + CEG ({(PAT_AGIRC_T1+PAT_CEG_T1)*100:.2f}%)",
                    f"Formation professionnelle ({PAT_FORMATION*100:.2f}%)",
                    f"**Total charges patronales (~{PAT_TOTAL*100:.1f}%)**",
                    "**Coût employeur total**",
                ],
                "Montant": [
                    fmt(r["brut"]),
                    fmt(charges["maladie"]),
                    fmt(charges["vieil"]),
                    fmt(charges["famille"]),
                    fmt(charges["at_mp"]),
                    fmt(charges["chomage"]),
                    fmt(charges["ags"]),
                    fmt(charges["agirc"]),
                    fmt(charges["formation"]),
                    fmt(charges["total"]),
                    fmt(charges["cout_total"]),
                ],
            })

            st.caption(
                "⚠️ Charges patronales semplificate (media settore privato). "
                "AT/MP varia per settore; allocations familiales ridotta a 3,45% sotto 3,5×SMIC."
            )
