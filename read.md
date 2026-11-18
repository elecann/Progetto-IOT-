# Simulatore relativo al Topic 5: Bitcoin Mining ed Energie Rinnovabili
Progetto di Cannata Elena e Idonea Marco
## 📌 Descrizione del Progetto

Questo progetto implementa un **simulatore software** basato sul modello presentato nell'articolo:

> *Holland, S., Mansur, E., Muller, N., & Yates, A. (2022). "Bitcoin and the electricity grid".*

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
  - **Tabella 1**: capacità ottimale (GW) ed emissioni (Mt CO₂) senza storage.
  - **Tabella 2**: statistiche sui prezzi e sulla varianza dei prezzi.
  - **Tabella 3**: capacità ottimale ed emissioni con storage.
  - **Tabella 4**: statistiche sui prezzi con storage.

Il simulatore si concentra sulla **Tabella 1** (scenari senza storage) e permette di replicare i risultati principali, con un'estensione parametrica per l'analisi di sensibilità.

---

## 🛠️ Requisiti

- **Python 3.8+**
- Librerie:
  ```bash
  pip install numpy pandas matplotlib
  ```

---

## 🚀 Come Eseguire il Simulatore

1. Clona o scarica il file `simulatore.py`.
2. Apri il terminale nella cartella del progetto.
3. Esegui:
   ```bash
   python simulatore.py
   ```
4. Il programma stamperà a schermo:
   - I risultati dei tre scenari (emissioni, prezzo medio, varianza).
   - Un confronto con i valori della Tabella 1 dell'articolo.
5. Verranno generati due file immagine:
   - `risultati_simulazione.png`: confronto emissioni e mix di generazione.
   - `sensibilita_domanda.png`: esperimento extra sulla sensibilità alla domanda dei miner.

---

## 📂 Struttura del Codice

| Componente | Descrizione |
| :--- | :--- |
| **Parametri** | Costi marginali, fattori di emissione e capacità presi dalle Tabelle A1, 1 e 3 dell'articolo. |
| **Profili Orari** | Generazione di 8760 ore di domanda, capacity factor eolici/solari e domanda dei miner. |
| **Motore di Simulazione** | Funzione `simula_anno()` che implementa il dispatch orario con vincoli (1)-(4), storage e Demand Response. |
| **Esecuzione Scenari** | Chiamata alla funzione per i tre scenari (Baseline, Bitcoin, Bitcoin+DR). |
| **Output** | Tabelle riassuntive, confronto con l'articolo e grafici. |
| **Esperimento Extra** | Analisi di sensibilità: variazione della domanda dei miner (0, 5, 10, 20, 30 GW) e impatto sulle emissioni. |

---

## 📊 Analisi Previste e Risultati Attesi

Il simulatore è progettato per condurre le seguenti analisi quantitative, in linea con la Sezione 5 dell'articolo.

### Analisi 1 — Confronto tra Scenari (Replica Tabella 1)

Vengono simulati tre scenari con le capacità di generazione e storage definite nell'articolo (Tabella 1 e 3):

| Scenario | Capacità Solare (GW) | Capacità Eolico (GW) | Capacità Gas CC (GW) | Capacità Gas Peaker (GW) | Storage (GWh) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Baseline | 48.68 | 34.24 | 27.47 | 5.62 | 32.54 |
| Bitcoin | 58.39 | 75.39 | 42.60 | 0.00 | 30.89 |
| Bitcoin + DR | 58.48 | 82.92 | 29.42 | 0.00 | 21.66 |

**Metriche calcolate per ciascuno scenario:**
- Emissioni totali annue di CO₂ (Mt).
- Prezzo medio dell'elettricità ($/MWh).
- Varianza giornaliera dei prezzi (misura di volatilità).
- Generazione media oraria per tecnologia (GW).

**Risultati attesi (confronto con l'articolo):**

| Scenario | Emissioni (Mt CO₂) — Articolo | Emissioni (Mt CO₂) — Simulatore |
| :--- | :---: | :---: |
| Baseline | 46.43 | ~40–50 |
| Bitcoin | 75.07 | ~60–80 |
| Bitcoin + DR | 48.67 | ~45–55 |

Le differenze sono dovute a:
- Profili orari semplificati (sinusoidali) invece che dati reali ERCOT.
- Prezzo marginale calcolato in modo semplificato (costo dell'ultima tecnologia utilizzata).
- Domanda dei miner assunta costante invece che derivata dalla curva di domanda stimata nella Sezione 3.

### Analisi 2 — Sensibilità alla Domanda dei Miner (Esperimento Extra)

Per mostrare che il software è **parametrico** e non solo una replica, viene eseguito un esperimento che varia la domanda media dei miner (0, 5, 10, 20, 30 GW) e misura l'impatto sulle emissioni totali.

**Risultato atteso:** relazione lineare tra domanda dei miner ed emissioni, con un coefficiente angolare che dipende dal mix di generazione marginale (prevalentemente Gas CC nello scenario Bitcoin).

Il grafico risultante (`sensibilita_domanda.png`) conferma la capacità del simulatore di condurre analisi what-if.

### Analisi 3 — Verifica della Demand Response

Viene confrontato lo scenario Bitcoin con e senza Demand Response per verificare l'affermazione dell'articolo secondo cui la DR **attenua quasi completamente** l'aumento delle emissioni.

**Risultato atteso:** riduzione delle emissioni di circa 25–30 Mt CO₂ quando la DR è attiva, grazie alla minore dipendenza dal Gas CC.

---

## 🧪 Validazione

La validazione del simulatore avviene su tre livelli:

1. **Validazione qualitativa**: i risultati rispettano le direzioni attese dall'articolo (Bitcoin aumenta le rinnovabili e le emissioni; la DR riduce le emissioni).
2. **Validazione quantitativa**: confronto con la Tabella 1 dell'articolo, con tolleranza del ±20% dovuta alle semplificazioni dichiarate.
3. **Validazione di sensibilità**: l'esperimento extra sulla domanda dei miner produce risultati monotoni e coerenti con la teoria (più domanda → più emissioni).

---

## 🔍 Limiti e Possibili Estensioni

### Limiti
- **Modello di prezzo semplificato**: non cattura la scarsità di capacità né i picchi estremi di prezzo.
- **Profili orari sintetici**: non utilizzano i dati reali ERCOT.
- **Domanda dei miner costante**: non implementa la curva di domanda della Sezione 3.
- **Nessuna rete di trasmissione**: il modello assume un singolo nodo (Texas isolato).

### Estensioni future
- Implementare l'**Equazione 7** (approccio bottom-up) per stimare la domanda dei miner in funzione del prezzo del Bitcoin.
- Aggiungere una **soglia di prezzo** per la Demand Response (es. i miner si spengono se il prezzo > 150 $/MWh).
- Utilizzare **dati reali ERCOT** per i capacity factor eolici e solari.
- Implementare il **modello di equilibrio endogeno completo** (Bellman Equation) per determinare le capacità ottimali.

---

## 📚 Riferimenti

- Holland, S., Mansur, E., Muller, N., & Yates, A. (2022). *Bitcoin and the electricity grid*.
- Cambridge Bitcoin Electricity Consumption Index (CBECI).
- U.S. Energy Information Administration (EIA) — Dati ERCOT.

---

## 👥 Autori

- **Cannata Elena**
- **Idonea Marco**

Progetto IOT — Bitcoin Mining ed Energie Rinnovabili.
```

---
