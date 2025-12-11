#!/usr/bin/env python3
"""
Confronto tra file MASTER (ELENCO PROGETTI) e anagrafica attuale (strutture_sanitarie.csv)
"""

import pandas as pd
import difflib

# Leggi file master
df_master = pd.read_csv('ELENCO PROGETTI CdC E OdC.xlsx - PNRR.csv')

# Leggi anagrafica attuale
df_attuale = pd.read_csv('strutture_sanitarie.csv')

print("="*80)
print("ANALISI CONFRONTO ANAGRAFICHE")
print("="*80)

# Separa CDC e ODC nel master
cdc_mask = df_master['DENOMINAZIONE'].str.contains('CdC', na=False, case=False)
odc_mask = df_master['DENOMINAZIONE'].str.contains('OdC', na=False, case=False)

df_master_cdc = df_master[cdc_mask].copy()
df_master_odc = df_master[odc_mask].copy()

# Separa CDC e ODC nell'attuale
df_attuale_cdc = df_attuale[df_attuale['Tipologia'] == 'CdC'].copy()
df_attuale_odc = df_attuale[df_attuale['Tipologia'] == 'OdC'].copy()

print(f"\n📊 NUMEROSITÀ")
print(f"{'':30} {'Master':>10} {'Attuale':>10} {'Delta':>10}")
print("-"*60)
print(f"{'CDC':30} {len(df_master_cdc):10} {len(df_attuale_cdc):10} {len(df_attuale_cdc)-len(df_master_cdc):+10}")
print(f"{'ODC':30} {len(df_master_odc):10} {len(df_attuale_odc):10} {len(df_attuale_odc)-len(df_master_odc):+10}")
print(f"{'TOTALE':30} {len(df_master_cdc)+len(df_master_odc):10} {len(df_attuale):10} {len(df_attuale)-(len(df_master_cdc)+len(df_master_odc)):+10}")

# Normalizza nomi per confronto
def normalizza_nome(nome):
    """Normalizza nome per confronto: minuscolo, rimuove spazi extra, rimuove 'di'/'DI'"""
    if pd.isna(nome):
        return ""
    nome = str(nome).lower().strip()
    nome = ' '.join(nome.split())  # rimuove spazi multipli
    nome = nome.replace(' di ', ' ').replace('cdc ', 'cdc').replace('odc ', 'odc')
    return nome

# Crea dizionari normalizzati
master_cdc_nomi = {normalizza_nome(row['DENOMINAZIONE']): row['DENOMINAZIONE']
                   for _, row in df_master_cdc.iterrows()}
master_odc_nomi = {normalizza_nome(row['DENOMINAZIONE']): row['DENOMINAZIONE']
                   for _, row in df_master_odc.iterrows()}

attuale_cdc_nomi = {normalizza_nome(row['Nome_Struttura']): row['Nome_Struttura']
                    for _, row in df_attuale_cdc.iterrows()}
attuale_odc_nomi = {normalizza_nome(row['Nome_Struttura']): row['Nome_Struttura']
                    for _, row in df_attuale_odc.iterrows()}

print(f"\n📋 CDC - STRUTTURE NEL MASTER MA NON IN ATTUALE:")
print("-"*80)
for nome_norm, nome_orig in master_cdc_nomi.items():
    if nome_norm not in attuale_cdc_nomi:
        # Cerca match simili
        matches = difflib.get_close_matches(nome_norm, attuale_cdc_nomi.keys(), n=1, cutoff=0.6)
        if matches:
            print(f"⚠️  {nome_orig}")
            print(f"    Possibile match: {attuale_cdc_nomi[matches[0]]}")
        else:
            print(f"❌ {nome_orig} - MANCANTE")

print(f"\n📋 CDC - STRUTTURE IN ATTUALE MA NON NEL MASTER:")
print("-"*80)
conta_extra = 0
for nome_norm, nome_orig in attuale_cdc_nomi.items():
    if nome_norm not in master_cdc_nomi:
        # Cerca match simili
        matches = difflib.get_close_matches(nome_norm, master_cdc_nomi.keys(), n=1, cutoff=0.6)
        if not matches:
            conta_extra += 1
            if conta_extra <= 10:  # Mostra solo primi 10
                print(f"  {nome_orig}")

if conta_extra > 10:
    print(f"  ... e altri {conta_extra - 10}")
print(f"\nTotale CDC extra in attuale: {conta_extra}")

print(f"\n📋 ODC - CONFRONTO:")
print("-"*80)
print(f"Master ODC: {len(df_master_odc)}")
for _, row in df_master_odc.iterrows():
    nome = row['DENOMINAZIONE']
    print(f"  - {nome}")

print(f"\nAttuale ODC: {len(df_attuale_odc)}")
for _, row in df_attuale_odc.iterrows():
    nome = row['Nome_Struttura']
    pnrr = row['PNRR']
    print(f"  - {nome} [PNRR: {pnrr}]")

# Analisi PNRR
print(f"\n📊 ANALISI PNRR - CDC:")
print("-"*80)

# Per ogni CDC nel master, trova corrispondenza in attuale e confronta PNRR
match_pnrr = 0
mismatch_pnrr = 0
not_found = 0

for _, row_master in df_master_cdc.iterrows():
    nome_master = normalizza_nome(row_master['DENOMINAZIONE'])
    pnrr_master = row_master['VALIDATA']

    # Cerca in attuale
    found = False
    for _, row_attuale in df_attuale_cdc.iterrows():
        nome_attuale = normalizza_nome(row_attuale['Nome_Struttura'])
        if nome_master in nome_attuale or nome_attuale in nome_master:
            found = True
            pnrr_attuale = row_attuale['PNRR']

            # Confronta PNRR
            if pnrr_master == pnrr_attuale:
                match_pnrr += 1
            else:
                mismatch_pnrr += 1
                print(f"⚠️  {row_master['DENOMINAZIONE']}")
                print(f"    Master: PNRR={pnrr_master} | Attuale: PNRR={pnrr_attuale}")
            break

    if not found:
        not_found += 1

print(f"\nRiepilogo PNRR:")
print(f"  Match: {match_pnrr}")
print(f"  Mismatch: {mismatch_pnrr}")
print(f"  Non trovati: {not_found}")

print("\n" + "="*80)
print("RACCOMANDAZIONI")
print("="*80)
print("""
1. Il file MASTER contiene 25 CDC + 8 ODC (progetti PNRR)
2. L'anagrafica attuale ha 53 CDC + 12 ODC (include strutture non-PNRR)

AZIONI SUGGERITE:
a) Usare il MASTER per aggiornare solo i campi PNRR delle strutture presenti
b) Mantenere le strutture extra in attuale (sono strutture non-PNRR valide)
c) Verificare i mismatch PNRR e correggere nell'anagrafica attuale
d) Verificare nomi strutture con lievi differenze
""")
