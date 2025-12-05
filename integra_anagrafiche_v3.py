#!/usr/bin/env python3
"""
Script integrazione v3 - Distinzione corretta dispositivi CDC/ODC
- Dispositivi CDC: DIAG001-DIAG005 (ECG, Holter, Spirometro, Ecografo, Monitor)
- Dispositivi ODC: DIAG006-DIAG014 (Defibrillatore, Radiologico, Emogas, POC, ecc.)
- Attrezzature: ATTR001-ATTR010 (comuni a CDC e ODC)
"""

import pandas as pd
import csv

def carica_cdc_dispositivi():
    """Carica dispositivi diagnostici CDC (DIAG001-DIAG005) da CDC_CE_1_claude.csv"""
    strutture = []
    dotazioni = []

    with open('CDC_CE_1_claude.csv', 'r', encoding='latin-1') as f:
        lines = f.readlines()

    # Trova header
    header_idx = None
    for i, line in enumerate(lines):
        if 'Zona;Denominazione' in line:
            header_idx = i
            break

    if header_idx is None:
        print("❌ Header non trovato in CDC file")
        return [], []

    # Parse dati
    for i in range(header_idx + 1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue

        values = line.split(';')
        if len(values) < 5:
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

        # SOLO dispositivi CDC: DIAG001-DIAG005

        # ECG (col 5) - DIAG001
        if len(values) > 5:
            stato = values[5].strip().upper()
            if 'PRESENTE' in stato or 'FINANZIATO' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG001',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in stato or 'NON RICHIESTO' not in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG001',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        # Holter (col 7) - DIAG002
        if len(values) > 7:
            stato = values[7].strip().upper()
            if 'PRESENTE' in stato or 'FINANZIATO' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG002',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG002',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        # Spirometro (col 8) - DIAG003
        if len(values) > 8:
            stato = values[8].strip().upper()
            if 'PRESENTE' in stato or 'FINANZIATO' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG003',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG003',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        # Ecografo (col 10) - DIAG004
        if len(values) > 10:
            stato = values[10].strip().upper()
            if 'PRESENTE' in stato or 'FINANZIATO' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG004',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG004',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        # Monitor (col 12) - DIAG005
        if len(values) > 12:
            stato = values[12].strip().upper()
            if 'PRESENTE' in stato or 'FINANZIATO' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG005',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG005',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

    return strutture, dotazioni


def carica_odc_dispositivi():
    """Carica dispositivi diagnostici ODC (DIAG006-DIAG014) da ODC_CE_1_claude.csv"""
    strutture = []
    dotazioni = []

    # Usa csv.reader per gestire correttamente le celle multi-riga
    with open('ODC_CE_1_claude.csv', 'r', encoding='latin-1') as f:
        # Salta le righe di intestazione iniziali
        for _ in range(10):
            next(f)

        reader = csv.reader(f, delimiter=';')

        for values in reader:
            if len(values) < 2:
                continue

            zona = values[0].strip() if len(values) > 0 else ''
            struttura_raw = values[1].strip() if len(values) > 1 else ''

            if not struttura_raw or not zona:
                continue

            # Salta l'header se presente
            if 'STRUTTURA' in struttura_raw.upper() and len(values) > 2 and 'POSTI LETTO' in str(values[2]).upper():
                continue

            # Pulisci il nome
            nome_pulito = struttura_raw.replace('\n', ' ').replace('  ', ' ')
            nome_pulito = nome_pulito.replace("OSPEDALE DI COMUNITA' DI ", '')
            nome_pulito = nome_pulito.replace("OSPEDALE DI COMUNITA' ", '')
            nome_pulito = nome_pulito.replace("OSPEDALE DI COMUNITA ", '')
            nome_pulito = nome_pulito.replace('CURE INTERMEDIE ', '')
            nome_pulito = nome_pulito.strip('"').strip()

            # Estrai solo il nome principale
            if any(ind in nome_pulito for ind in ['P.zza', 'Via', 'Viale', 'Piazza']):
                for ind in ['P.zza', 'Via', 'Viale', 'Piazza', 'Largo']:
                    if ind in nome_pulito:
                        nome_pulito = nome_pulito.split(ind)[0].strip()
                        break

            if '(' in nome_pulito and 'DETTA' not in nome_pulito.upper():
                nome_pulito = nome_pulito.split('(')[0].strip()

            # Estrai posti letto
            posti_letto = values[2].strip() if len(values) > 2 else ''

            # Determina PNRR
            pnrr = 'SI'  # Default per ODC
            if len(values) > 3:
                pnrr_col = values[3].strip().upper()
                if pnrr_col in ['NO', 'N']:
                    pnrr = 'NO'

            codice = f"ODC{len(strutture)+1:03d}"

            strutture.append({
                'Tipologia': 'OdC',
                'Codice': codice,
                'Nome_Struttura': f"OdC {nome_pulito}",
                'Zona': zona,
                'Classificazione': '',
                'Comune': nome_pulito.upper(),
                'Provincia': '',
                'Indirizzo': '',
                'CAP': '',
                'PNRR': pnrr,
                'Posti_Letto': posti_letto
            })

            # SOLO dispositivi ODC: DIAG006-DIAG014
            # Assegna tutti i dispositivi ODC a ogni struttura ODC
            dispositivi_odc = [
                ('DIAG006', 'Defibrillatore/DAE'),
                ('DIAG007', 'Apparecchio radiologico'),
                ('DIAG008', 'Emogasanalizzatore'),
                ('DIAG009', 'POC (Point of Care)'),
                ('DIAG010', 'Carrello emergenza'),
                ('DIAG011', 'ECG portatile'),
                ('DIAG012', 'Spirometro (ODC)'),
                ('DIAG013', 'Ecografo (ODC)'),
                ('DIAG014', 'Telemedicina (STANZA)')
            ]

            for cod_disp, desc_disp in dispositivi_odc:
                dotazioni.append({
                    'Codice_Struttura': codice,
                    'Codice_Dotazione': cod_disp,
                    'Quantita_Presente': 0,
                    'Quantita_Richiesta': 1,
                    'Note': 'Da acquistare'
                })

    return strutture, dotazioni


def carica_attrezzature_sanitarie(df_strutture):
    """Carica attrezzature sanitarie dai file tecnologie_*_dettaglio.csv - COMUNI a CDC e ODC"""
    dotazioni_attr = []

    # Carica CDC attrezzature
    try:
        df_cdc_attr = pd.read_csv('tecnologie_cdc_dettaglio.csv')

        # Mappa tecnologie a codici
        mapping = {
            'LETTINO VISITA ELETTRICO': 'ATTR001',
            'Lettino visita di tipo ginecologico (FAVERO)': 'ATTR002',
            'DAE+ ASPIRATORE PER CARRELLO EMERGENZA': 'ATTR004',
            'LAMPADA VISITA SU STATIVO': 'ATTR005',
            'FRIGORIFERO': 'ATTR006'
        }

        for _, row in df_cdc_attr.iterrows():
            tecnologia = row['Tecnologia']
            struttura_nome = row['Struttura']
            quantita = int(row['Quantita'])

            # Trova codice struttura - matching migliorato
            codice_strutt = None
            for _, strutt in df_strutture.iterrows():
                if strutt['Tipologia'] == 'CdC':
                    # Estrai parte comune del nome per matching
                    nome_struttura = strutt['Nome_Struttura'].replace('CdC ', '')
                    if nome_struttura in struttura_nome or struttura_nome in strutt['Nome_Struttura']:
                        codice_strutt = strutt['Codice']
                        break

            if codice_strutt and tecnologia in mapping:
                dotazioni_attr.append({
                    'Codice_Struttura': codice_strutt,
                    'Codice_Dotazione': mapping[tecnologia],
                    'Quantita_Presente': quantita,
                    'Quantita_Richiesta': quantita,
                    'Note': 'Presente (da file PNRR)'
                })

    except Exception as e:
        print(f"⚠️ Errore caricamento attrezzature CDC: {e}")

    # Carica ODC attrezzature
    try:
        df_odc_attr = pd.read_csv('tecnologie_odc_dettaglio.csv')

        mapping = {
            'Letto elettrico degenza (LINET)': 'ATTR003',
            'FRIGORIFERO': 'ATTR006',
            'DAE+ ASPIRATORE PER CARRELLO EMERGENZA': 'ATTR004',
            'Lavapadelle (ARJO)': 'ATTR007',
            'Vuotatoio (ARJO)': 'ATTR008',
            'Sollevatore (ARJO)': 'ATTR009'
        }

        for _, row in df_odc_attr.iterrows():
            tecnologia = row['Tecnologia']
            struttura_nome = row['Struttura']
            quantita = int(row['Quantita'])

            # Trova codice struttura - matching migliorato
            codice_strutt = None
            for _, strutt in df_strutture.iterrows():
                if strutt['Tipologia'] == 'OdC':
                    nome_struttura = strutt['Nome_Struttura'].replace('OdC ', '')
                    if nome_struttura in struttura_nome or struttura_nome in strutt['Nome_Struttura']:
                        codice_strutt = strutt['Codice']
                        break

            if codice_strutt and tecnologia in mapping:
                dotazioni_attr.append({
                    'Codice_Struttura': codice_strutt,
                    'Codice_Dotazione': mapping[tecnologia],
                    'Quantita_Presente': quantita,
                    'Quantita_Richiesta': quantita,
                    'Note': 'Presente (da file PNRR)'
                })

    except Exception as e:
        print(f"⚠️ Errore caricamento attrezzature ODC: {e}")

    return dotazioni_attr


def main():
    print("="*80)
    print("INTEGRAZIONE v3 - DISPOSITIVI CDC/ODC SEPARATI")
    print("="*80)
    print()

    # Carica CDC
    print("📋 Caricamento CDC (dispositivi DIAG001-DIAG005)...")
    strutture_cdc, dotazioni_cdc = carica_cdc_dispositivi()
    print(f"  ✅ {len(strutture_cdc)} CDC caricate")
    print(f"  ✅ {len(dotazioni_cdc)} configurazioni dispositivi CDC")
    print()

    # Carica ODC
    print("🏥 Caricamento ODC (dispositivi DIAG006-DIAG014)...")
    strutture_odc, dotazioni_odc = carica_odc_dispositivi()
    print(f"  ✅ {len(strutture_odc)} ODC caricate")
    print(f"  ✅ {len(dotazioni_odc)} configurazioni dispositivi ODC")
    print()

    # Combina strutture
    strutture_totali = strutture_cdc + strutture_odc
    df_strutture = pd.DataFrame(strutture_totali)

    # Carica attrezzature
    print("🛏️ Caricamento attrezzature sanitarie (ATTR001-ATTR010)...")
    dotazioni_attr = carica_attrezzature_sanitarie(df_strutture)
    print(f"  ✅ {len(dotazioni_attr)} configurazioni attrezzature sanitarie")
    print()

    # Combina dotazioni
    dotazioni_totali = dotazioni_cdc + dotazioni_odc + dotazioni_attr
    df_dotazioni = pd.DataFrame(dotazioni_totali)

    # Salva file
    print("💾 Salvataggio file integrati...")
    df_strutture.to_csv('strutture_sanitarie.csv', index=False)
    print(f"  ✅ strutture_sanitarie.csv ({len(df_strutture)} strutture)")

    df_dotazioni.to_csv('dotazioni_strutture_telemedicina.csv', index=False)
    print(f"  ✅ dotazioni_strutture_telemedicina.csv ({len(df_dotazioni)} configurazioni)")
    print()

    # Riepilogo
    print("="*80)
    print("RIEPILOGO INTEGRAZIONE")
    print("="*80)
    print(f"Totale Strutture: {len(df_strutture)}")
    print(f"  - CDC: {len(strutture_cdc)}")
    print(f"  - ODC: {len(strutture_odc)}")
    print()

    pnrr_si = len(df_strutture[df_strutture['PNRR'] == 'SI'])
    pnrr_no = len(df_strutture[df_strutture['PNRR'] == 'NO'])
    print(f"Strutture PNRR: {pnrr_si}")
    print(f"Strutture non PNRR: {pnrr_no}")
    print()

    print(f"Totale Configurazioni Dotazioni: {len(df_dotazioni)}")
    print(f"  - Dispositivi diagnostici CDC: {len(dotazioni_cdc)}")
    print(f"  - Dispositivi diagnostici ODC: {len(dotazioni_odc)}")
    print(f"  - Attrezzature sanitarie: {len(dotazioni_attr)}")
    print()

    # Distribuzione per codice
    print("📊 Distribuzione dotazioni per codice:")
    dist = df_dotazioni['Codice_Dotazione'].value_counts().sort_index()
    for cod, count in dist.items():
        print(f"  {cod}: {count} configurazioni")
    print()

    print("✅ Integrazione completata!")


if __name__ == "__main__":
    main()
