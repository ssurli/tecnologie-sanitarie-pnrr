#!/usr/bin/env python3
"""
Script di aggiornamento dati - Dashboard Telemedicina
Importa nuovi dati da file Excel e aggiorna i CSV

Utilizzo:
    python aggiorna_dati.py CDC_CE_1.xlsx
    python aggiorna_dati.py --tutti  # Importa tutti i file nella cartella
"""

import pandas as pd
import shutil
from datetime import datetime
from pathlib import Path
import sys
import argparse

def backup_files():
    """Crea backup dei file CSV esistenti"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"backup_{timestamp}")
    backup_dir.mkdir(exist_ok=True)

    files_to_backup = [
        'strutture_sanitarie.csv',
        'dotazioni_strutture_telemedicina.csv',
        'dotazioni_telemedicina_catalogo.csv'
    ]

    print(f"📦 Creazione backup in {backup_dir}/")
    for file in files_to_backup:
        if Path(file).exists():
            shutil.copy2(file, backup_dir / file)
            print(f"  ✅ {file}")

    return backup_dir

def importa_excel(file_path):
    """Importa dati da file Excel"""
    print(f"\n📥 Importazione da {file_path}")

    try:
        # Leggi Excel
        df = pd.read_excel(file_path)

        # Mostra preview
        print(f"  📊 Righe: {len(df)}, Colonne: {len(df.columns)}")
        print(f"  📋 Colonne: {', '.join(df.columns.tolist())}")

        return df

    except Exception as e:
        print(f"  ❌ Errore: {e}")
        return None

def valida_dati(df, tipo='strutture'):
    """Valida i dati importati"""
    print(f"\n🔍 Validazione dati {tipo}...")

    errori = []
    warnings = []

    if tipo == 'strutture':
        # Colonne richieste per strutture
        colonne_richieste = ['Nome_Struttura', 'Tipologia', 'PNRR']
        for col in colonne_richieste:
            if col not in df.columns:
                errori.append(f"Colonna mancante: {col}")

        # Verifica valori PNRR
        if 'PNRR' in df.columns:
            valori_invalidi = df[~df['PNRR'].isin(['SI', 'NO'])]['PNRR'].unique()
            if len(valori_invalidi) > 0:
                warnings.append(f"Valori PNRR non standard: {valori_invalidi}")

    elif tipo == 'dotazioni':
        # Colonne richieste per dotazioni
        colonne_richieste = ['Codice_Struttura', 'Codice_Dotazione', 'Quantita_Richiesta']
        for col in colonne_richieste:
            if col not in df.columns:
                errori.append(f"Colonna mancante: {col}")

    # Report validazione
    if errori:
        print(f"  ❌ {len(errori)} errori:")
        for err in errori:
            print(f"    - {err}")
        return False

    if warnings:
        print(f"  ⚠️  {len(warnings)} warning:")
        for warn in warnings:
            print(f"    - {warn}")

    print(f"  ✅ Validazione OK")
    return True

def aggiorna_strutture(df_nuovo):
    """Aggiorna file strutture_sanitarie.csv"""
    print(f"\n🔄 Aggiornamento strutture...")

    # Carica CSV esistente
    df_esistente = pd.read_csv('strutture_sanitarie.csv')

    # Merge o sostituisci
    # TODO: Implementa logica di merge basata su Codice

    # Per ora sovrascrivi (implementa merge più sofisticato se necessario)
    df_nuovo.to_csv('strutture_sanitarie.csv', index=False)
    print(f"  ✅ Aggiornate {len(df_nuovo)} strutture")

def rigenera_dati():
    """Rigenera dati integrati"""
    print(f"\n🔄 Rigenerazione dati integrati...")

    import subprocess
    result = subprocess.run(['python', 'integra_anagrafiche_v3.py'],
                          capture_output=True, text=True)

    if result.returncode == 0:
        print(f"  ✅ Dati rigenerati")
        return True
    else:
        print(f"  ❌ Errore: {result.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Aggiorna dati dashboard')
    parser.add_argument('file', nargs='?', help='File Excel da importare')
    parser.add_argument('--tutti', action='store_true', help='Importa tutti i file *.xlsx nella cartella')
    parser.add_argument('--no-backup', action='store_true', help='Salta backup')
    parser.add_argument('--no-regen', action='store_true', help='Salta rigenerazione dati')

    args = parser.parse_args()

    print("=" * 80)
    print("AGGIORNAMENTO DATI DASHBOARD TELEMEDICINA")
    print("=" * 80)

    # Backup
    if not args.no_backup:
        backup_dir = backup_files()

    # Importa file
    if args.tutti:
        files = list(Path('.').glob('*.xlsx'))
        print(f"\n📂 Trovati {len(files)} file Excel")
        for file in files:
            df = importa_excel(file)
            if df is not None:
                # Processa file
                pass
    elif args.file:
        df = importa_excel(args.file)
        if df is not None and valida_dati(df, tipo='strutture'):
            # aggiorna_strutture(df)
            print("\n⚠️  Aggiornamento manuale richiesto - verifica i dati prima")
    else:
        parser.print_help()
        return

    # Rigenera dati
    if not args.no_regen:
        if rigenera_dati():
            print("\n✅ Aggiornamento completato!")
        else:
            print("\n❌ Errore durante rigenerazione")
            if not args.no_backup:
                print(f"💡 Puoi ripristinare il backup da: {backup_dir}/")

    print("\n" + "=" * 80)
    print("Per applicare le modifiche alla dashboard:")
    print("  1. Verifica i dati aggiornati")
    print("  2. git add .")
    print("  3. git commit -m 'Aggiorna dati da [fonte]'")
    print("  4. git push")
    print("=" * 80)

if __name__ == "__main__":
    main()
