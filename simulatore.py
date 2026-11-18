import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# PARAMETRI DELL'ARTICOLO (Tabelle A1 e Sezione 4)
# ============================================================

# Costi marginali ($/MWh) e fattori di emissione (t CO2/MWh)
TECNOLOGIE = {
    'Gas_Peaker': {'costo': 44.13, 'emissioni': 0.526},
    'Gas_CC':     {'costo': 26.68, 'emissioni': 0.338},
    'Eolico':     {'costo': 0.0,   'emissioni': 0.0},
    'Solare':     {'costo': 0.0,   'emissioni': 0.0}
}

# Capacità in GW (dalla Tabella 1 dell'articolo - caso senza storage)
CAPACITA = {
    'Baseline':        {'Solare': 48.68, 'Eolico': 34.24, 'Gas_CC': 27.47, 'Gas_Peaker': 5.62},
    'Bitcoin':         {'Solare': 58.39, 'Eolico': 75.39, 'Gas_CC': 42.60, 'Gas_Peaker': 0.00},
    'Bitcoin_DR':      {'Solare': 58.48, 'Eolico': 82.92, 'Gas_CC': 29.42, 'Gas_Peaker': 0.00}
}

# Capacità di storage in GWh (Tabella 3)
STORAGE = {
    'Baseline':   32.54,
    'Bitcoin':    30.89,
    'Bitcoin_DR': 21.66
}

# ============================================================
# GENERAZIONE DEI PROFILI ORARI (8760 ore)
# ============================================================

np.random.seed(42)  # Per riproducibilità
ore_anno = 8760
ore_giorno = np.arange(24)

# --- Domanda tradizionale (GW) ---
# Curva sinusoidale: picco alle 17:00, minimo alle 5:00
domanda_base = 30 + 10 * np.sin(2 * np.pi * (ore_giorno - 8) / 24)
domanda_base = np.tile(domanda_base, 365)
# Variazione stagionale (estate più alta)
domanda_base *= (1 + 0.2 * np.sin(2 * np.pi * np.arange(ore_anno) / 8760))
domanda_base = np.clip(domanda_base, 15, 60)

# --- Capacity factor Eolico ---
# Più forte di notte, con incertezza
eolico_cf = 0.35 + 0.15 * np.sin(2 * np.pi * (ore_giorno - 0) / 24)
eolico_cf = np.tile(eolico_cf, 365)
eolico_cf += np.random.normal(0, 0.1, ore_anno)
eolico_cf = np.clip(eolico_cf, 0, 1)

# --- Capacity factor Solare ---
# Picco a mezzogiorno, zero di notte
solare_cf = np.maximum(0, np.sin(2 * np.pi * (ore_giorno - 6) / 24)) * 0.8
solare_cf = np.tile(solare_cf, 365)
solare_cf += np.random.normal(0, 0.05, ore_anno)
solare_cf = np.clip(solare_cf, 0, 1)

# --- Domanda dei miner (GW) ---
# L'articolo stima ~10 GW di domanda media globale assegnata al Texas
DOMANDA_MINER_MEDIA = 10.0  # GW
domanda_miner = np.full(ore_anno, DOMANDA_MINER_MEDIA)
domanda_miner += np.random.normal(0, 0.5, ore_anno)
domanda_miner = np.maximum(0, domanda_miner)

# ============================================================
# MOTORE DI SIMULAZIONE (Dispatch orario)
# ============================================================

def simula_anno(capacita, storage_capacita, domanda_miner, dr_attiva=False):
    """
    Simula un anno di dispatch orario.
    Restituisce: emissioni (Mt), prezzo medio, varianza prezzo, generazione per tecnologia.
    """
    generazione = {tech: np.zeros(ore_anno) for tech in TECNOLOGIE}
    prezzi = np.zeros(ore_anno)
    emissioni_totali = 0.0
    soc = 0.0  # State of Charge della batteria (GWh)
    efficienza = 0.9  # Efficienza di round-trip

    for t in range(ore_anno):
        # 1. Domanda totale
        domanda_tot = domanda_base[t] + domanda_miner[t]

        # 2. Generazione rinnovabile disponibile
        gen_solare = capacita['Solare'] * solare_cf[t]
        gen_eolico = capacita['Eolico'] * eolico_cf[t]
        gen_rinnovabile = gen_solare + gen_eolico

        # 3. Bilanciamento
        surplus = gen_rinnovabile - domanda_tot

        if surplus > 0:
            # Carica batteria (se c'è)
            if storage_capacita > 0:
                carica = min(surplus, storage_capacita - soc, storage_capacita * 0.1)
                soc += carica
                surplus -= carica
            # Il resto è curtailed (sprecato)
            # Ripartisci proporzionalmente la generazione rinnovabile
            if gen_rinnovabile > 0:
                gen_solare_eff = gen_solare * (domanda_tot / gen_rinnovabile)
                gen_eolico_eff = gen_eolico * (domanda_tot / gen_rinnovabile)
            else:
                gen_solare_eff = gen_eolico_eff = 0
            deficit = 0
        else:
            gen_solare_eff = gen_solare
            gen_eolico_eff = gen_eolico
            deficit = -surplus

            # Scarica batteria
            if storage_capacita > 0 and soc > 0:
                scarica = min(deficit, soc, storage_capacita * 0.1)
                soc -= scarica
                deficit -= scarica

            # Demand Response: riduci la domanda dei miner
            if dr_attiva and deficit > 0:
                riduzione = min(deficit, domanda_miner[t])
                domanda_miner[t] -= riduzione
                domanda_tot -= riduzione
                deficit -= riduzione

        # 4. Generazione fossile per coprire il deficit
        gen_gas_cc = 0.0
        gen_gas_peaker = 0.0

        if deficit > 0:
            gen_gas_cc = min(deficit, capacita['Gas_CC'])
            deficit -= gen_gas_cc
            if deficit > 0:
                gen_gas_peaker = min(deficit, capacita['Gas_Peaker'])
                deficit -= gen_gas_peaker

        # 5. Emissioni
        emissioni_t = (gen_gas_cc * TECNOLOGIE['Gas_CC']['emissioni'] +
                       gen_gas_peaker * TECNOLOGIE['Gas_Peaker']['emissioni'])
        emissioni_totali += emissioni_t

        # 6. Prezzo marginale (semplificato)
        if gen_gas_peaker > 0:
            prezzi[t] = TECNOLOGIE['Gas_Peaker']['costo']
        elif gen_gas_cc > 0:
            prezzi[t] = TECNOLOGIE['Gas_CC']['costo']
        else:
            prezzi[t] = 0.0

        # Salva generazione
        generazione['Solare'][t] = gen_solare_eff
        generazione['Eolico'][t] = gen_eolico_eff
        generazione['Gas_CC'][t] = gen_gas_cc
        generazione['Gas_Peaker'][t] = gen_gas_peaker

    # Statistiche
    prezzo_medio = np.mean(prezzi)
    prezzi_giornalieri = prezzi.reshape(365, 24)
    varianza_giornaliera = np.mean(np.var(prezzi_giornalieri, axis=1))

    return {
        'emissioni': emissioni_totali / 1e6,  # Mt CO2
        'prezzo_medio': prezzo_medio,
        'varianza_prezzo': varianza_giornaliera,
        'generazione': generazione
    }

# ============================================================
# ESECUZIONE DEGLI SCENARI
# ============================================================

print("=" * 60)
print("SIMULAZIONE BITCOIN MINING E ENERGIE RINNOVABILI")
print("=" * 60)

# Scenario 1: Baseline (senza Bitcoin)
print("\n[1] Scenario BASELINE (senza Bitcoin)...")
res_baseline = simula_anno(CAPACITA['Baseline'], STORAGE['Baseline'], np.zeros(ore_anno), dr_attiva=False)

# Scenario 2: Con Bitcoin (senza DR)
print("[2] Scenario BITCOIN (senza Demand Response)...")
res_bitcoin = simula_anno(CAPACITA['Bitcoin'], STORAGE['Bitcoin'], domanda_miner.copy(), dr_attiva=False)

# Scenario 3: Con Bitcoin + Demand Response
print("[3] Scenario BITCOIN + DEMAND RESPONSE...")
res_bitcoin_dr = simula_anno(CAPACITA['Bitcoin_DR'], STORAGE['Bitcoin_DR'], domanda_miner.copy(), dr_attiva=True)

# ============================================================
# RISULTATI
# ============================================================

print("\n" + "=" * 60)
print("RISULTATI (confronto con Tabella 1 dell'articolo)")
print("=" * 60)

risultati = pd.DataFrame({
    'Scenario': ['Baseline', 'Bitcoin', 'Bitcoin+DR'],
    'Emissioni (Mt CO2)': [res_baseline['emissioni'], res_bitcoin['emissioni'], res_bitcoin_dr['emissioni']],
    'Prezzo Medio ($/MWh)': [res_baseline['prezzo_medio'], res_bitcoin['prezzo_medio'], res_bitcoin_dr['prezzo_medio']],
    'Varianza Prezzo': [res_baseline['varianza_prezzo'], res_bitcoin['varianza_prezzo'], res_bitcoin_dr['varianza_prezzo']]
})

print(risultati.to_string(index=False))

print("\n" + "=" * 60)
print("CONFRONTO CON L'ARTICOLO (Tabella 1)")
print("=" * 60)
print("Articolo - Baseline: 46.43 Mt CO2")
print("Articolo - Bitcoin:  75.07 Mt CO2")
print("Articolo - Bitcoin+DR: 48.67 Mt CO2")
print("\nI tuoi risultati dovrebbero essere nello stesso ordine di grandezza.")

# ============================================================
# GRAFICI
# ============================================================

# Grafico 1: Confronto emissioni
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].bar(risultati['Scenario'], risultati['Emissioni (Mt CO2)'], color=['green', 'red', 'blue'])
axes[0].set_ylabel('Emissioni (Mt CO2)')
axes[0].set_title('Emissioni Totali Annue')
axes[0].grid(axis='y', alpha=0.3)

# Grafico 2: Generazione media per tecnologia
tecnologie = ['Solare', 'Eolico', 'Gas_CC', 'Gas_Peaker']
x = np.arange(len(tecnologie))
width = 0.25

for i, (nome, res) in enumerate([('Baseline', res_baseline), ('Bitcoin', res_bitcoin), ('Bitcoin+DR', res_bitcoin_dr)]):
    medie = [np.mean(res['generazione'][t]) for t in tecnologie]
    axes[1].bar(x + i*width, medie, width, label=nome)

axes[1].set_xticks(x + width)
axes[1].set_xticklabels(tecnologie)
axes[1].set_ylabel('Generazione Media (GW)')
axes[1].set_title('Mix di Generazione per Scenario')
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('risultati_simulazione.png', dpi=150)
plt.show()

print("\nGrafico salvato come 'risultati_simulazione.png'")
