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
📊 Risultati Attesi
I risultati del simulatore non saranno identici a quelli dell'articolo, poiché il modello originale utilizza un equilibrio endogeno complesso (Bellman Equation con algoritmo a due passi) e dati reali del Texas (ERCOT). Tuttavia, i risultati dovrebbero essere nello stesso ordine di grandezza:

Scenario	Emissioni (Mt CO₂) — Articolo	Emissioni (Mt CO₂) — Simulatore
Baseline	46.43	~40–50
Bitcoin	75.07	~60–80
Bitcoin + DR	48.67	~45–55
Le differenze sono dovute a:

Profili orari semplificati (sinusoidali) invece che dati reali ERCOT.

Prezzo marginale calcolato in modo semplificato (costo dell'ultima tecnologia utilizzata).

Domanda dei miner assunta costante invece che derivata dalla curva di domanda stimata nella Sezione 3.

🧪 Esperimento Extra: Sensibilità alla Domanda dei Miner
Per mostrare che il software è parametrico e non solo una replica, è stato aggiunto un esperimento che varia la domanda media dei miner (0, 5, 10, 20, 30 GW) e misura l'impatto sulle emissioni totali. Il risultato è mostrato nel grafico sensibilita_domanda.png e conferma la relazione lineare tra domanda dei miner ed emissioni.

🔍 Limiti e Possibili Estensioni
Limiti
Modello di prezzo semplificato: non cattura la scarsità di capacità né i picchi estremi di prezzo.

Profili orari sintetici: non utilizzano i dati reali ERCOT.

Domanda dei miner costante: non implementa la curva di domanda della Sezione 3.

Nessuna rete di trasmissione: il modello assume un singolo nodo (Texas isolato).

Estensioni future
Implementare l'Equazione 7 (approccio bottom-up) per stimare la domanda dei miner in funzione del prezzo del Bitcoin.

Aggiungere una soglia di prezzo per la Demand Response (es. i miner si spengono se il prezzo > 150 $/MWh).

Utilizzare dati reali ERCOT per i capacity factor eolici e solari.

Implementare il modello di equilibrio endogeno completo (Bellman Equation) per determinare le capacità ottimali.

📚 Riferimenti
Holland, S., Mansur, E., Muller, N., & Yates, A. (2022). Bitcoin and the electricity grid. (Articolo di riferimento).

Cambridge Bitcoin Electricity Consumption Index (CBECI).

U.S. Energy Information Administration (EIA) — Dati ERCOT.

👥 Autori
Cannata Elena

Idonea Marco

Progetto IOT — Bitcoin Mining ed Energie Rinnovabili.
