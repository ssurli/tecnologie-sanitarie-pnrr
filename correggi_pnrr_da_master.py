#!/usr/bin/env python3
"""
Script per correggere i valori PNRR nell'anagrafica usando il file MASTER
ELENCO PROGETTI CdC E OdC come fonte autoritativa.
"""

import pandas as pd
import difflib
from datetime import datetime

def normalizza_nome(nome):
    """Normalizza nome per confronto"""
    if pd.isna(nome):
        return ""
    nome = str(nome).lower().strip()
    nome = ' '.join(nome.split())
    nome = nome.replace(' di ', ' ').replace('cdc ', 'cdc').replace('odc ', 'odc')
    return nome

def trova_match(nome_cerca, lista_nomi_dict, threshold=0.7):
    """Trova match migliore tra nomi normalizzati"""
    nome_norm = normalizza_nome(nome_cerca)

    # Cerca match esatto
    if nome_norm in lista_nomi_dict:
        return lista_nomi_dict[nome_norm], 1.0

    # Cerca match fuzzy
    matches = difflib.get_close_matches(nome_norm, lista_nomi_dict.keys(), n=1, cutoff=threshold)
    if matches:
        score = difflib.SequenceMatcher(None, nome_norm, matches[0]).ratio()
        return lista_nomi_dict[matches[0]], score

    return None, 0.0

def main():
    print("="*80)
    print("CORREZIONE PNRR DA FILE MASTER")
    print("="*80)

    # Leggi file master
    print("\n📥 Lettura file MASTER...")
    df_master = pd.read_csv('ELENCO PROGETTI CdC E OdC.xlsx - PNRR.csv')

    # Separa CDC e ODC
    cdc_mask = df_master['DENOMINAZIONE'].str.contains('CdC', na=False, case=False)
    df_master_cdc = df_master[cdc_mask].copy()

    print(f"   ✅ {len(df_master_cdc)} CDC nel Master")

    # Crea dizionario normalizzato: nome_norm → (nome_orig, PNRR)
    master_dict = {}
    for _, row in df_master_cdc.iterrows():
        nome_norm = normalizza_nome(row['DENOMINAZIONE'])
        master_dict[nome_norm] = {
            'nome': row['DENOMINAZIONE'],
            'pnrr': row['VALIDATA']
        }

    # Leggi anagrafica attuale
    print("\n📥 Lettura anagrafica attuale...")
    df_attuale = pd.read_csv('strutture_sanitarie.csv')
    df_attuale_cdc = df_attuale[df_attuale['Tipologia'] == 'CdC'].copy()

    print(f"   ✅ {len(df_attuale_cdc)} CDC nell'anagrafica")

    # Backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f'strutture_sanitarie.csv.backup_{timestamp}'
    df_attuale.to_csv(backup_file, index=False)
    print(f"   💾 Backup creato: {backup_file}")

    # Processa correzioni
    print("\n🔄 Analisi correzioni...")
    print("-"*80)

    correzioni = []
    non_trovati = []
    gia_corretti = 0

    for idx, row in df_attuale_cdc.iterrows():
        nome_struttura = row['Nome_Struttura']
        pnrr_attuale = row['PNRR']

        # Cerca nel master
        match_info, score = trova_match(nome_struttura, master_dict)

        if match_info:
            pnrr_master = match_info['pnrr']

            if pnrr_attuale != pnrr_master:
                correzioni.append({
                    'idx': idx,
                    'nome': nome_struttura,
                    'master_nome': match_info['nome'],
                    'prima': pnrr_attuale,
                    'dopo': pnrr_master,
                    'score': score
                })
                print(f"🔧 {nome_struttura}")
                print(f"   {pnrr_attuale} → {pnrr_master} (match: {score:.1%})")
            else:
                gia_corretti += 1
        else:
            # Non trovato nel master - mantieni com'è
            non_trovati.append(nome_struttura)

    print(f"\n📊 RIEPILOGO:")
    print(f"   Correzioni da applicare: {len(correzioni)}")
    print(f"   Già corretti: {gia_corretti}")
    print(f"   Non nel Master (mantenuti): {len(non_trovati)}")

    if len(correzioni) == 0:
        print("\n✅ Nessuna correzione necessaria!")
        return

    # Chiedi conferma
    print("\n⚠️  ATTENZIONE:")
    print(f"   Verranno modificati {len(correzioni)} record PNRR")
    print(f"   Le {len(non_trovati)} strutture non nel Master restano invariate")
    print()

    risposta = input("Procedere con le correzioni? (si/no): ").strip().lower()

    if risposta not in ['si', 'sì', 's', 'yes', 'y']:
        print("\n❌ Operazione annullata")
        return

    # Applica correzioni
    print("\n✍️  Applicazione correzioni...")
    df_corrette = df_attuale.copy()

    for correzione in correzioni:
        idx = correzione['idx']
        df_corrette.loc[idx, 'PNRR'] = correzione['dopo']

    # Salva file corretto
    output_file = 'strutture_sanitarie_CORRETTE.csv'
    df_corrette.to_csv(output_file, index=False)

    print(f"   ✅ File salvato: {output_file}")

    # Report dettagliato
    report_file = f'report_correzioni_pnrr_{timestamp}.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("REPORT CORREZIONI PNRR\n")
        f.write("="*80 + "\n\n")
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"File Master: ELENCO PROGETTI CdC E OdC.xlsx - PNRR.csv\n")
        f.write(f"File Attuale: strutture_sanitarie.csv\n\n")

        f.write(f"Correzioni applicate: {len(correzioni)}\n\n")

        f.write("DETTAGLIO CORREZIONI:\n")
        f.write("-"*80 + "\n")
        for c in correzioni:
            f.write(f"\n{c['nome']}\n")
            f.write(f"  Master: {c['master_nome']}\n")
            f.write(f"  PNRR: {c['prima']} → {c['dopo']}\n")
            f.write(f"  Match score: {c['score']:.1%}\n")

        f.write(f"\n\nSTRUTTURE NON NEL MASTER (mantenute invariate):\n")
        f.write("-"*80 + "\n")
        for nome in non_trovati:
            f.write(f"  - {nome}\n")

    print(f"   📄 Report salvato: {report_file}")

    print("\n" + "="*80)
    print("✅ CORREZIONE COMPLETATA")
    print("="*80)
    print("\nPROSSIMI PASSI:")
    print("1. Verifica il file: strutture_sanitarie_CORRETTE.csv")
    print("2. Se OK, applicalo:")
    print("   cp strutture_sanitarie_CORRETTE.csv strutture_sanitarie.csv")
    print("3. Rigenera dati:")
    print("   python integra_anagrafiche_v3.py")
    print("4. Commit:")
    print("   git add strutture_sanitarie.csv")
    print("   git commit -m 'fix: Corregge PNRR da file master'")
    print("   git push")

if __name__ == "__main__":
    main()
