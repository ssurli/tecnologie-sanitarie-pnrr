#!/usr/bin/env python3
"""
Importa tecnologie dai fogli PULITI cdc_tecnologie e odc_tecnologie
(senza interferenze degli arredi)

NOTA: I prezzi NON vengono usati da questi file, ma dal catalogo ufficiale
      dotazioni_telemedicina_catalogo.csv durante l'integrazione
"""

import pandas as pd
import numpy as np

def pulisci_valore_euro(valore):
    """Converte valori Euro in float (formato europeo: 1.000,00)"""
    if pd.isna(valore) or valore == '':
        return 0.0

    # Rimuovi €, spazi
    valore_str = str(valore).replace('€', '').replace(' ', '').strip()

    try:
        # Formato europeo: 1.000,00 → rimuovi punto (migliaia), sostituisci , con .
        if ',' in valore_str:
            valore_str = valore_str.replace('.', '').replace(',', '.')
        # Altrimenti potrebbe essere già in formato corretto
        return float(valore_str)
    except:
        return 0.0

def estrai_tecnologie_cdc():
    """Estrae tecnologie dal foglio CDC pulito"""
    print("\n📥 Importazione CDC...")

    df = pd.read_csv('Stima arredi PNRR.xlsx - cdc_tecnologie.csv', header=None)

    # Riga 1 (indice 0) contiene i nomi delle strutture
    strutture_row = df.iloc[0]
    strutture = []
    for col_idx in range(2, len(strutture_row)):  # Salta prime 2 colonne
        nome = strutture_row[col_idx]
        if pd.notna(nome) and str(nome).strip() and 'CdC' in str(nome):
            strutture.append((col_idx, str(nome).strip()))

    print(f"  ✅ Trovate {len(strutture)} strutture CDC")

    # Estrai tecnologie (righe 2+)
    tecnologie = []

    for row_idx in range(1, len(df)):  # Salta riga header
        nome_tech = df.iloc[row_idx, 0]
        costo_unitario = df.iloc[row_idx, 1]

        if pd.isna(nome_tech) or str(nome_tech).strip() == '':
            continue

        nome_tech_str = str(nome_tech).strip()
        costo = pulisci_valore_euro(costo_unitario)

        # Estrai quantità per ogni struttura
        for col_idx, nome_struttura in strutture:
            quantita_val = df.iloc[row_idx, col_idx]

            if pd.notna(quantita_val) and str(quantita_val).strip():
                try:
                    qta = float(str(quantita_val).replace(',', '.'))
                    if qta > 0:
                        tecnologie.append({
                            'Struttura': nome_struttura,
                            'Tipologia': 'CdC',
                            'Attrezzatura': nome_tech_str,
                            'Costo_Unitario': costo,
                            'Quantita': qta,
                            'Totale': costo * qta
                        })
                except:
                    pass

    print(f"  ✅ Estratte {len(tecnologie)} voci tecnologie CDC")
    return tecnologie

def estrai_tecnologie_odc():
    """Estrae tecnologie dal foglio ODC pulito"""
    print("\n📥 Importazione ODC...")

    df = pd.read_csv('Stima arredi PNRR.xlsx - odc_tecnologie.csv', header=None)

    # Riga 1 (indice 0) contiene i nomi delle strutture
    strutture_row = df.iloc[0]
    strutture = []
    for col_idx in range(2, len(strutture_row)):  # Salta prime 2 colonne
        nome = strutture_row[col_idx]
        if pd.notna(nome) and str(nome).strip() and 'OdC' in str(nome):
            strutture.append((col_idx, str(nome).strip()))

    print(f"  ✅ Trovate {len(strutture)} strutture ODC")

    # Estrai tecnologie (righe 2+)
    tecnologie = []

    for row_idx in range(1, len(df)):  # Salta riga header
        nome_tech = df.iloc[row_idx, 0]
        costo_unitario = df.iloc[row_idx, 1]

        if pd.isna(nome_tech) or str(nome_tech).strip() == '':
            continue

        nome_tech_str = str(nome_tech).strip()
        costo = pulisci_valore_euro(costo_unitario)

        # Estrai quantità per ogni struttura
        for col_idx, nome_struttura in strutture:
            quantita_val = df.iloc[row_idx, col_idx]

            if pd.notna(quantita_val) and str(quantita_val).strip():
                try:
                    qta = float(str(quantita_val).replace(',', '.'))
                    if qta > 0:
                        tecnologie.append({
                            'Struttura': nome_struttura,
                            'Tipologia': 'OdC',
                            'Attrezzatura': nome_tech_str,
                            'Costo_Unitario': costo,
                            'Quantita': qta,
                            'Totale': costo * qta
                        })
                except:
                    pass

    print(f"  ✅ Estratte {len(tecnologie)} voci tecnologie ODC")
    return tecnologie

def main():
    print("="*70)
    print("IMPORTAZIONE TECNOLOGIE DA FOGLI PULITI")
    print("="*70)

    # Estrai da entrambi i fogli
    tecnologie_cdc = estrai_tecnologie_cdc()
    tecnologie_odc = estrai_tecnologie_odc()

    # Combina
    tutte_tecnologie = tecnologie_cdc + tecnologie_odc

    if not tutte_tecnologie:
        print("\n❌ Nessuna tecnologia estratta!")
        return

    # Crea DataFrame
    df_tech = pd.DataFrame(tutte_tecnologie)

    # Salva
    output_file = 'tecnologie_arredi_pnrr.csv'
    df_tech.to_csv(output_file, index=False)

    print("\n" + "="*70)
    print("✅ IMPORTAZIONE COMPLETATA")
    print("="*70)
    print(f"📊 Totale voci: {len(df_tech)}")
    print(f"🏥 Strutture: {df_tech['Struttura'].nunique()}")
    print(f"   - CDC: {len(df_tech[df_tech['Tipologia']=='CdC']['Struttura'].unique())}")
    print(f"   - ODC: {len(df_tech[df_tech['Tipologia']=='OdC']['Struttura'].unique())}")
    print(f"🔧 Attrezzature: {df_tech['Attrezzatura'].nunique()}")
    print(f"💰 Totale costi (indicativi): €{df_tech['Totale'].sum():,.2f}")
    print(f"\n⚠️  I prezzi mostrati sono dal file, ma durante l'integrazione")
    print(f"    verranno usati i prezzi UFFICIALI da dotazioni_telemedicina_catalogo.csv")
    print(f"\n💾 File salvato: {output_file}")

    # Riepilogo per attrezzatura
    print(f"\n📦 Riepilogo per attrezzatura:")
    riepilogo = df_tech.groupby('Attrezzatura').agg({
        'Quantita': 'sum',
        'Totale': 'sum'
    }).sort_values('Totale', ascending=False)

    for attrezzatura, row in riepilogo.iterrows():
        print(f"  • {attrezzatura:45s} | Qta: {row['Quantita']:3.0f} | €{row['Totale']:,.2f}")

if __name__ == "__main__":
    main()
