Progetto di Cannata Elena e Idonea Marco

# Simulatore Topic 5: Bitcoin Mining ed Energie Rinnovabili

## 📌 Descrizione del Progetto

Questo progetto implementa un **simulatore software** basato sul modello presentato nell'articolo:

> *"Bitcoin and the electricity grid"* (HMY 2022) — Sezione 5: Simulazione e Risultati.

L'obiettivo è **quantificare l'impatto del Bitcoin mining** sulla capacità di generazione rinnovabile, sulle emissioni di CO₂ e sulla gestione della rete elettrica, confrontando tre scenari:
1. **Baseline**: senza domanda elettrica da Bitcoin.
2. **Bitcoin**: con domanda elettrica da Bitcoin.
3. **Bitcoin + Demand Response (DR)**: i miner spengono la loro domanda quando c'è deficit di rinnovabili.

Il simulatore riproduce la logica del modello di equilibrio di lungo periodo descritto nelle Equazioni (1)-(6) dell'articolo, implementando un **dispatch orario su 8760 ore** con:
- 4 tecnologie di generazione: Solare, Eolico, Gas Combined Cycle (CC), Gas Peaker.
- Storage (batteria) opzionale.
- Incertezza nei capacity factor delle rinnovabili.
- Meccanismo di Demand Response per i miner.

---

## 🎯 Parte Quantitativa dell'Articolo Individuata

La consegna richiede di individuare la parte dell'articolo in cui vengono effettuate **valutazioni quantitative**. Nel nostro caso, corrisponde a:

- **Sezione 4 (Simulation)**: descrizione degli esperimenti e dei parametri di input.
- **Sezione 5 (Results)**: risultati quantitativi riportati nelle **Tabelle 1, 2, 3 e 4**.
  - Tabella 1: capacità ottimale (GW) ed emissioni (Mt CO₂) senza storage.
  - Tabella 2: statistiche sui prezzi e sulla varianza dei prezzi.
  - Tabella 3: capacità ottimale ed emissioni con storage.
  - Tabella 4: statistiche sui prezzi con storage.

Il simulatore si concentra sulla **Tabella 1** (scenari senza storage) e permette di replicare i risultati principali.

---

## 🛠️ Requisiti

- **Python 3.8+**
- Librerie:
  ```bash
  pip install numpy pandas matplotlib
