#!/usr/bin/env python3
"""
Script semplificato per integrare le anagrafiche reali delle strutture
"""

import pandas as pd
import csv

def carica_cdc():
    """Carica CDC manualmente per gestire il formato particolare"""
    strutture = []
    dotazioni = []

    with open('CDC_CE_1_claude.csv', 'r', encoding='latin-1') as f:
        lines = f.readlines()

    # Trova la riga dell'header (contiene "Zona;Denominazione")
    header_idx = None
    for i, line in enumerate(lines):
        if 'Zona;Denominazione' in line:
            header_idx = i
            break

    if header_idx is None:
        print("❌ Header non trovato in CDC file")
        return [], []

    # Parse header
    header = lines[header_idx].strip().split(';')

    # Parse dati
    for i in range(header_idx + 1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue

        values = line.split(';')
        if len(values) < 5:  # Righe troppo corte
            continue

        zona = values[0].strip() if len(values) > 0 else ''
        denominazione = values[1].strip() if len(values) > 1 else ''
        tipologia = values[2].strip() if len(values) > 2 else ''
        pnrr = values[3].strip().upper() if len(values) > 3 else ''
        indirizzo = values[4].strip() if len(values) > 4 else ''

        if not denominazione:
            continue

        codice = f"CDC{len(strutture)+1:03d}"

        strutture.append({
            'Tipologia': 'CdC',
            'Codice': codice,
            'Nome_Struttura': f"CdC {denominazione}",
            'Zona': zona,
            'Classificazione': tipologia if tipologia in ['Hub', 'Spoke'] else 'Spoke',
            'Comune': denominazione,
            'Provincia': '',
            'Indirizzo': indirizzo,
            'CAP': '',
            'PNRR': 'SI' if pnrr in ['PNRR', 'X', 'SI'] else 'NO'
        })

        # Dotazioni
        if len(values) > 5:
            # ECG
            ecg = values[5].strip().upper() if len(values) > 5 else ''
            if 'PRESENTE' in ecg or 'FINANZIATO' in ecg:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG001',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in ecg:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG001',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        if len(values) > 7:
            # Holter
            holter = values[7].strip().upper() if len(values) > 7 else ''
            if 'PRESENTE' in holter or 'FINANZIATO' in holter:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG002',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in holter:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG002',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        if len(values) > 8:
            # Spirometro
            spiro = values[8].strip().upper() if len(values) > 8 else ''
            if 'PRESENTE' in spiro or 'FINANZIATO' in spiro:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG003',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in spiro:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG003',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        if len(values) > 10:
            # Ecografo
            eco = values[10].strip().upper() if len(values) > 10 else ''
            if 'PRESENTE' in eco or 'FINANZIATO' in eco:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG004',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in eco:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG004',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        if len(values) > 12:
            # Monitor
            monitor = values[12].strip().upper() if len(values) > 12 else ''
            if 'PRESENTE' in monitor or 'FINANZIATO' in monitor:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG005',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in monitor:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG005',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

    return strutture, dotazioni

def carica_odc():
    """Carica ODC manualmente"""
    strutture = []
    dotazioni = []

    with open('ODC_CE_1_claude.csv', 'r', encoding='latin-1') as f:
        lines = f.readlines()

    # Trova header
    header_idx = None
    for i, line in enumerate(lines):
        if 'Zona;STRUTTURA' in line:
            header_idx = i
            break

    if header_idx is None:
        print("❌ Header non trovato in ODC file")
        return [], []

    # Parse dati
    for i in range(header_idx + 1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue

        values = line.split(';')
        if len(values) < 2:
            continue

        zona = values[0].strip() if len(values) > 0 else ''
        struttura_raw = values[1].strip() if len(values) > 1 else ''

        if not struttura_raw:
            continue

        # Pulisci nome struttura
        nome_pulito = struttura_raw.replace('\n', ' ').replace('  ', ' ')
        nome_pulito = nome_pulito.replace("OSPEDALE DI COMUNITA' DI ", '')
        nome_pulito = nome_pulito.replace('CURE INTERMEDIE ', '')
        nome_pulito = nome_pulito.split('\n')[0] if '\n' in nome_pulito else nome_pulito

        posti_letto = values[2].strip() if len(values) > 2 else ''
        pnrr = values[4].strip().upper() if len(values) > 4 else ''

        codice = f"ODC{len(strutture)+1:03d}"

        strutture.append({
            'Tipologia': 'OdC',
            'Codice': codice,
            'Nome_Struttura': f"OdC {nome_pulito}",
            'Zona': zona,
            'Classificazione': '',
            'Comune': nome_pulito.split('-')[0].strip() if '-' in nome_pulito else nome_pulito,
            'Provincia': '',
            'Indirizzo': '',
            'CAP': '',
            'PNRR': 'SI' if pnrr in ['X', 'PNRR', 'SI'] else 'NO',
            'Posti_Letto': posti_letto
        })

        # Dotazioni (colonne: 7=eco, 11=spiro, 15=ECG, 10=defibrillatore)
        if len(values) > 7:
            eco = values[7].strip().upper()
            if 'PRESENTE' in eco:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG004',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

        if len(values) > 11:
            spiro = values[11].strip().upper()
            if 'PRESENTE' in spiro:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG003',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

        if len(values) > 15:
            ecg = values[15].strip().upper()
            if 'PRESENTE' in ecg:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG001',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

        if len(values) > 10:
            dae = values[10].strip().upper()
            if 'PRESENTE' in dae:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'ATTR004',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

    return strutture, dotazioni

def main():
    print("="*80)
    print("INTEGRAZIONE ANAGRAFICHE REALI - DASHBOARD TELEMEDICINA")
    print("="*80)

    print("\n📋 Caricamento Case di Comunità...")
    strutture_cdc, dotazioni_cdc = carica_cdc()
    print(f"  ✅ {len(strutture_cdc)} Case di Comunità caricate")
    print(f"  ✅ {len(dotazioni_cdc)} configurazioni dotazioni create")

    print("\n🏥 Caricamento Ospedali di Comunità...")
    strutture_odc, dotazioni_odc = carica_odc()
    print(f"  ✅ {len(strutture_odc)} Ospedali di Comunità caricati")
    print(f"  ✅ {len(dotazioni_odc)} configurazioni dotazioni create")

    # Salva
    print("\n💾 Salvataggio file integrati...")

    df_strutture = pd.DataFrame(strutture_cdc + strutture_odc)
    df_strutture.to_csv('strutture_sanitarie_integrate.csv', index=False, encoding='utf-8')
    print(f"  ✅ Salvato: strutture_sanitarie_integrate.csv ({len(df_strutture)} strutture)")

    df_dotazioni = pd.DataFrame(dotazioni_cdc + dotazioni_odc)
    df_dotazioni.to_csv('dotazioni_strutture_telemedicina_integrate.csv', index=False, encoding='utf-8')
    print(f"  ✅ Salvato: dotazioni_strutture_telemedicina_integrate.csv ({len(df_dotazioni)} configurazioni)")

    # Statistiche
    print("\n" + "="*80)
    print("RIEPILOGO INTEGRAZIONE")
    print("="*80)
    print(f"Totale Strutture: {len(df_strutture)}")
    print(f"  - Case di Comunità: {len(strutture_cdc)}")
    print(f"  - Ospedali di Comunità: {len(strutture_odc)}")
    print(f"\nStrutture PNRR: {len(df_strutture[df_strutture['PNRR'] == 'SI'])}")
    print(f"Strutture non PNRR: {len(df_strutture[df_strutture['PNRR'] == 'NO'])}")
    print(f"\nTotale Configurazioni Dotazioni: {len(df_dotazioni)}")

    print("\n✅ Integrazione completata con successo!")

if __name__ == "__main__":
    main()
