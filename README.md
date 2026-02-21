# Simulatore Stipendio Netto Italia

![Anteprima](aa.jpg)

Calcolatore interattivo per stimare il **netto in busta paga** a partire da RAL o costo aziendale, basato sulle aliquote IRPEF 2024.

**[Apri l'app](https://simstipendi.streamlit.app/)**

---

## Funzionalità

- Calcolo del netto annuo e mensile da **RAL** o **costo aziendale**
- Supporto per **13a e 14a mensilità**
- **Addizionale regionale** per tutte le regioni italiane
- **Addizionale comunale** personalizzabile
- Detrazioni per **coniuge** e **figli a carico**
- **Trattamento integrativo** (ex bonus Renzi)
- Dettaglio completo di ogni voce: INPS, IRPEF, detrazioni, addizionali
- Calcolo accantonamento **TFR**

## Calcoli inclusi

| Voce | Dettaglio |
|---|---|
| Contributi INPS dipendente | 9,19% della RAL |
| Contributi INPS azienda | ~30% della RAL |
| IRPEF | 3 scaglioni 2024: 23% / 35% / 43% |
| Detrazioni lavoro dipendente | Art. 13 TUIR |
| Detrazione coniuge a carico | Art. 12 TUIR |
| Detrazione figli > 21 anni | 950€ per figlio |
| Trattamento integrativo | Max 1.200€/anno |
| TFR | RAL / 13,5 |

## Avvio in locale

```bash
pip install streamlit
streamlit run app.py
```

## Note

I calcoli sono stime basate sulle aliquote standard 2024. Situazioni particolari (partita IVA, regimi agevolati, pensioni, ecc.) non sono coperte.
