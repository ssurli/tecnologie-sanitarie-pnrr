#!/usr/bin/env python3
"""
Script completo per integrare:
1. Anagrafiche strutture da CDC_CE_1_claude.csv e ODC_CE_1_claude.csv
2. Dispositivi diagnostici da CDC_CE_1_claude.csv e ODC_CE_1_claude.csv
3. Attrezzature sanitarie da tecnologie_cdc_dettaglio.csv e tecnologie_odc_dettaglio.csv
"""

import pandas as pd
import csv

def carica_cdc_dispositivi():
    """Carica dispositivi diagnostici CDC da CDC_CE_1_claude.csv"""
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

        # Dispositivi diagnostici (indici colonne da CDC_CE_1)
        # ECG (col 5)
        if len(values) > 5:
            stato = values[5].strip().upper()
            if 'PRESENTE' in stato or 'FINANZIATO' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG001',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG001',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        # Holter (col 7)
        if len(values) > 7:
            stato = values[7].strip().upper()
            if 'PRESENTE' in stato or 'FINANZIATO' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG002',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG002',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        # Spirometro (col 8)
        if len(values) > 8:
            stato = values[8].strip().upper()
            if 'PRESENTE' in stato or 'FINANZIATO' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG003',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG003',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        # Ecografo (col 10)
        if len(values) > 10:
            stato = values[10].strip().upper()
            if 'PRESENTE' in stato or 'FINANZIATO' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG004',
                                'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})
            elif 'DA ACQUISTARE' in stato:
                dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG004',
                                'Quantita_Presente': 0, 'Quantita_Richiesta': 1, 'Note': 'Da acquistare'})

        # Monitor (col 12)
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
    """Carica dispositivi diagnostici ODC da ODC_CE_1_claude.csv"""
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
            if 'STRUTTURA' in struttura_raw.upper() and 'POSTI LETTO' in str(values[2]).upper():
                continue

            # Pulisci il nome
            nome_pulito = struttura_raw.replace('\n', ' ').replace('  ', ' ')
            nome_pulito = nome_pulito.replace("OSPEDALE DI COMUNITA' DI ", '')
            nome_pulito = nome_pulito.replace("OSPEDALE DI COMUNITA' ", '')
            nome_pulito = nome_pulito.replace("OSPEDALE DI COMUNITA ", '')
            nome_pulito = nome_pulito.replace('CURE INTERMEDIE ', '')

            # Rimuovi virgolette
            nome_pulito = nome_pulito.strip('"').strip()

            # Estrai solo il nome principale rimuovendo indirizzo
            # Se contiene indirizzo (Via, P.zza, etc.) prendi solo la prima parte
            if any(ind in nome_pulito for ind in ['P.zza', 'Via', 'Viale', 'Piazza']):
                # Prendi tutto prima dell'indirizzo
                for ind in ['P.zza', 'Via', 'Viale', 'Piazza', 'Largo']:
                    if ind in nome_pulito:
                        nome_pulito = nome_pulito.split(ind)[0].strip()
                        break

            # Se contiene località tra parentesi, estrai
            if '(' in nome_pulito:
                # Es: "MASSA P.zza 4 Novembre (MS)" -> "MASSA"
                # Ma mantieni es: "LE PIANE (DETTA VILLETTA)"
                if not 'DETTA' in nome_pulito.upper():
                    nome_pulito = nome_pulito.split('(')[0].strip()

            posti_letto = values[2].strip() if len(values) > 2 else ''
            pnrr = values[4].strip().upper() if len(values) > 4 else ''

            codice = f"ODC{len(strutture)+1:03d}"

            strutture.append({
                'Tipologia': 'OdC',
                'Codice': codice,
                'Nome_Struttura': f"OdC {nome_pulito}",
                'Zona': zona,
                'Classificazione': '',
                'Comune': nome_pulito.split('-')[0].split('(')[0].strip(),
                'Provincia': '',
                'Indirizzo': '',
                'CAP': '',
                'PNRR': 'SI' if pnrr in ['X', 'PNRR', 'SI'] else 'NO',
                'Posti_Letto': posti_letto
            })

            # Dispositivi diagnostici ODC
            # apparecchio radiologico (col 6)
            if len(values) > 6:
                stato = values[6].strip().upper()
                if 'PRESENTE' in stato:
                    dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG007',
                                    'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

            # ECOGRAFO (col 7)
            if len(values) > 7:
                stato = values[7].strip().upper()
                if 'PRESENTE' in stato:
                    dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG004',
                                    'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

            # carrello emergenza (col 9)
            if len(values) > 9:
                stato = values[9].strip().upper()
                if 'PRESENTE' in stato:
                    dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG010',
                                    'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

            # defibrillatore (col 10)
            if len(values) > 10:
                stato = values[10].strip().upper()
                if 'PRESENTE' in stato:
                    dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG006',
                                    'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

            # SPIROMETRO (col 11)
            if len(values) > 11:
                stato = values[11].strip().upper()
                if 'PRESENTE' in stato:
                    dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG003',
                                    'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

            # emogasanalizzatore (col 13)
            if len(values) > 13:
                stato = values[13].strip().upper()
                if 'PRESENTE' in stato:
                    dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG008',
                                    'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

            # POC (col 14)
            if len(values) > 14:
                stato = values[14].strip().upper()
                if 'PRESENTE' in stato:
                    dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG009',
                                    'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

            # ECG portatile (col 15)
            if len(values) > 15:
                stato = values[15].strip().upper()
                if 'PRESENTE' in stato:
                    dotazioni.append({'Codice_Struttura': codice, 'Codice_Dotazione': 'DIAG001',
                                    'Quantita_Presente': 1, 'Quantita_Richiesta': 1, 'Note': 'Presente'})

    return strutture, dotazioni

def carica_attrezzature_sanitarie(df_strutture):
    """Carica attrezzature sanitarie dai file tecnologie_*_dettaglio.csv"""
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

            # Trova codice struttura
            codice_strutt = None
            for _, strutt in df_strutture.iterrows():
                if strutt['Tipologia'] == 'CdC' and struttura_nome in strutt['Nome_Struttura']:
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
            'ECG': 'DIAG001',
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

            # Trova codice struttura
            codice_strutt = None
            for _, strutt in df_strutture.iterrows():
                if strutt['Tipologia'] == 'OdC' and any(parte in strutt['Nome_Struttura'] for parte in struttura_nome.split()):
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
    print("INTEGRAZIONE COMPLETA - DISPOSITIVI E ATTREZZATURE")
    print("="*80)

    # 1. Carica anagrafiche e dispositivi diagnostici
    print("\n📋 Caricamento CDC (dispositivi diagnostici)...")
    strutture_cdc, dotazioni_cdc_diag = carica_cdc_dispositivi()
    print(f"  ✅ {len(strutture_cdc)} CDC caricate")
    print(f"  ✅ {len(dotazioni_cdc_diag)} configurazioni dispositivi diagnostici")

    print("\n🏥 Caricamento ODC (dispositivi diagnostici)...")
    strutture_odc, dotazioni_odc_diag = carica_odc_dispositivi()
    print(f"  ✅ {len(strutture_odc)} ODC caricate")
    print(f"  ✅ {len(dotazioni_odc_diag)} configurazioni dispositivi diagnostici")

    # 2. Carica attrezzature sanitarie
    df_strutture = pd.DataFrame(strutture_cdc + strutture_odc)

    print("\n🛏️ Caricamento attrezzature sanitarie...")
    dotazioni_attr = carica_attrezzature_sanitarie(df_strutture)
    print(f"  ✅ {len(dotazioni_attr)} configurazioni attrezzature sanitarie")

    # 3. Combina tutto
    print("\n💾 Salvataggio file integrati...")

    df_strutture.to_csv('strutture_sanitarie_integrate.csv', index=False, encoding='utf-8')
    print(f"  ✅ strutture_sanitarie_integrate.csv ({len(df_strutture)} strutture)")

    dotazioni_complete = dotazioni_cdc_diag + dotazioni_odc_diag + dotazioni_attr
    df_dotazioni = pd.DataFrame(dotazioni_complete)
    df_dotazioni.to_csv('dotazioni_strutture_telemedicina_integrate.csv', index=False, encoding='utf-8')
    print(f"  ✅ dotazioni_strutture_telemedicina_integrate.csv ({len(df_dotazioni)} configurazioni)")

    # Statistiche
    print("\n" + "="*80)
    print("RIEPILOGO INTEGRAZIONE")
    print("="*80)
    print(f"Totale Strutture: {len(df_strutture)}")
    print(f"  - CDC: {len(strutture_cdc)}")
    print(f"  - ODC: {len(strutture_odc)}")
    print(f"\nStrutture PNRR: {len(df_strutture[df_strutture['PNRR'] == 'SI'])}")
    print(f"Strutture non PNRR: {len(df_strutture[df_strutture['PNRR'] == 'NO'])}")

    print(f"\nTotale Configurazioni Dotazioni: {len(df_dotazioni)}")
    print(f"  - Dispositivi diagnostici: {len(dotazioni_cdc_diag) + len(dotazioni_odc_diag)}")
    print(f"  - Attrezzature sanitarie: {len(dotazioni_attr)}")

    # Distribuzione per codice
    print("\n📊 Distribuzione dotazioni per codice:")
    dist = df_dotazioni['Codice_Dotazione'].value_counts().sort_index()
    for cod, count in dist.items():
        print(f"  {cod}: {count} configurazioni")

    print("\n✅ Integrazione completata!")

if __name__ == "__main__":
    main()
