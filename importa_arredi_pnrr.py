#!/usr/bin/env python3
"""
Script per importare tecnologie da file "Stima arredi PNRR"
Estrae solo anagrafiche strutture e sezione "Tipologia Attrezzatura da acquistare"
"""

import pandas as pd
import numpy as np

def estrai_tecnologie_odc():
    """Estrae tecnologie da file ODC"""
    print("📥 Importazione ODC...")

    df = pd.read_csv('Stima arredi PNRR.xlsx - OdC.csv', header=None)

    # Trova riga con nomi strutture (riga 2, indice 2)
    strutture_row = df.iloc[2]
    strutture = []
    indici_colonne = []

    for idx, val in enumerate(strutture_row):
        if 'OdC' in str(val):
            nome_pulito = str(val).strip().replace('OdC ', 'OdC ')
            strutture.append(nome_pulito)
            # Trova indice colonna numero (nr.)
            indici_colonne.append(idx + 2)  # Colonna "nr." dopo il nome

    print(f"  ✅ Trovate {len(strutture)} strutture ODC")

    # Trova inizio sezione tecnologie (cerca "Tipologia Attrezzatura")
    inizio_tecnologie = None
    for idx, row in df.iterrows():
        if 'Tipologia Attrezzatura' in str(row[1]):
            inizio_tecnologie = idx + 2  # Header è riga successiva, dati dopo ancora
            break

    if inizio_tecnologie is None:
        print("  ❌ Sezione tecnologie non trovata")
        return None

    print(f"  📍 Sezione tecnologie inizia a riga {inizio_tecnologie}")

    # Estrai dati tecnologie
    tecnologie_data = []
    for idx in range(inizio_tecnologie, len(df)):
        row = df.iloc[idx]

        # Salta righe vuote
        if pd.isna(row[1]) or str(row[1]).strip() == '':
            continue

        locale = str(row[0]).strip() if not pd.isna(row[0]) else ''
        attrezzatura = str(row[1]).strip()
        costo_str = str(row[2]).strip()

        # Estrai costo (rimuovi €, virgole, converti)
        try:
            costo = float(costo_str.replace('€', '').replace('.', '').replace(',', '.').strip())
        except:
            costo = 0.0

        # Per ogni struttura, estrai quantità
        for i, struttura in enumerate(strutture):
            col_idx = indici_colonne[i]
            if col_idx < len(row):
                qta_str = str(row[col_idx]).strip()
                try:
                    qta = int(qta_str) if qta_str and qta_str != 'nan' else 0
                except:
                    qta = 0

                if qta > 0:  # Solo se c'è una quantità
                    tecnologie_data.append({
                        'Struttura': struttura,
                        'Tipologia': 'OdC',
                        'Locale': locale,
                        'Attrezzatura': attrezzatura,
                        'Costo_Unitario': costo,
                        'Quantita': qta,
                        'Totale': costo * qta
                    })

    print(f"  ✅ Estratte {len(tecnologie_data)} voci tecnologie ODC")
    return pd.DataFrame(tecnologie_data)

def estrai_tecnologie_cdc():
    """Estrae tecnologie da file CDC"""
    print("\n📥 Importazione CDC...")

    df = pd.read_csv('Stima arredi PNRR.xlsx - CdC.csv', header=None)

    # Trova riga con nomi strutture (simile a ODC)
    strutture = []
    indici_colonne = []

    # Cerca nelle prime righe
    for idx in range(10):
        row = df.iloc[idx]
        for col_idx, val in enumerate(row):
            if 'CdC' in str(val) or 'Cdc' in str(val):
                nome = str(val).strip()
                if nome not in strutture and len(nome) < 50 and nome != 'CdC':
                    strutture.append(nome)
                    indici_colonne.append(col_idx + 2)  # Colonna nr.

    print(f"  ✅ Trovate {len(strutture)} strutture CDC")

    # Trova sezione tecnologie
    inizio_tecnologie = None
    for idx, row in df.iterrows():
        if 'Tipologia Attrezzatura' in str(row[1]):
            inizio_tecnologie = idx + 2
            break

    if inizio_tecnologie is None:
        print("  ❌ Sezione tecnologie non trovata")
        return None

    print(f"  📍 Sezione tecnologie inizia a riga {inizio_tecnologie}")

    # Estrai dati (stesso metodo di ODC)
    tecnologie_data = []
    for idx in range(inizio_tecnologie, len(df)):
        row = df.iloc[idx]

        if pd.isna(row[1]) or str(row[1]).strip() == '':
            continue

        locale = str(row[0]).strip() if not pd.isna(row[0]) else ''
        attrezzatura = str(row[1]).strip()
        costo_str = str(row[2]).strip()

        try:
            costo = float(costo_str.replace('€', '').replace('.', '').replace(',', '.').strip())
        except:
            costo = 0.0

        for i, struttura in enumerate(strutture):
            if i < len(indici_colonne):
                col_idx = indici_colonne[i]
                if col_idx < len(row):
                    qta_str = str(row[col_idx]).strip()
                    try:
                        qta = int(qta_str) if qta_str and qta_str != 'nan' else 0
                    except:
                        qta = 0

                    if qta > 0:
                        tecnologie_data.append({
                            'Struttura': struttura,
                            'Tipologia': 'CdC',
                            'Locale': locale,
                            'Attrezzatura': attrezzatura,
                            'Costo_Unitario': costo,
                            'Quantita': qta,
                            'Totale': costo * qta
                        })

    print(f"  ✅ Estratte {len(tecnologie_data)} voci tecnologie CDC")
    return pd.DataFrame(tecnologie_data)

def main():
    print("="*70)
    print("IMPORTAZIONE TECNOLOGIE DA STIMA ARREDI PNRR")
    print("="*70)

    # Estrai ODC
    df_odc = estrai_tecnologie_odc()

    # Estrai CDC
    df_cdc = estrai_tecnologie_cdc()

    # Combina
    if df_odc is not None and df_cdc is not None:
        df_tecnologie = pd.concat([df_odc, df_cdc], ignore_index=True)
    elif df_odc is not None:
        df_tecnologie = df_odc
    elif df_cdc is not None:
        df_tecnologie = df_cdc
    else:
        print("\n❌ Nessun dato estratto!")
        return

    # Salva
    output_file = 'tecnologie_arredi_pnrr.csv'
    df_tecnologie.to_csv(output_file, index=False)

    print("\n" + "="*70)
    print("✅ IMPORTAZIONE COMPLETATA")
    print("="*70)
    print(f"📊 Totale voci: {len(df_tecnologie)}")
    print(f"🏥 Strutture: {df_tecnologie['Struttura'].nunique()}")
    print(f"🔧 Attrezzature: {df_tecnologie['Attrezzatura'].nunique()}")
    print(f"💰 Totale costi: €{df_tecnologie['Totale'].sum():,.2f}")
    print(f"\n💾 File salvato: {output_file}")

    # Mostra riepilogo per attrezzatura
    print("\n📦 Riepilogo per attrezzatura:")
    riepilogo = df_tecnologie.groupby('Attrezzatura').agg({
        'Quantita': 'sum',
        'Totale': 'sum'
    }).sort_values('Totale', ascending=False)

    for idx, row in riepilogo.iterrows():
        print(f"  • {idx:40} | Qta: {row['Quantita']:3.0f} | €{row['Totale']:,.2f}")

if __name__ == "__main__":
    main()
