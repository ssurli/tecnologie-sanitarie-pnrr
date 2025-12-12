#!/usr/bin/env python3
"""
Script per integrare tecnologie da "Stima arredi PNRR" nelle dotazioni esistenti
NON modifica l'anagrafica strutture, solo aggiunge/aggiorna dotazioni

IMPORTANTE: Per le dotazioni già esistenti, SOSTITUISCE la quantità con il valore
PNRR definitivo (non somma). Il file Stima Arredi PNRR è la fonte definitiva.
"""

import pandas as pd

# Mappatura nomi strutture Stima Arredi → Nomi registro
MAPPATURA_STRUTTURE = {
    # ODC
    'OdC Campo Marte': 'OdC CAMPO DI MARTE Lucca',
    'OdC Cecina': 'OdC OSPEDALE DI COMUNITA CECINA Cecina',
    'OdC Piombino': 'OdC OSPEDALE DI COMUNITA PIOMBINO Piombino',
    'OdC Livorno': 'OdC PADIGLIONE 5 Livorno',
    'OdC Viareggio': 'OdC TABARRACCI',
    # CDC
    'CdC Carrara': 'CdC Carrara centro',
    'CdC Viareggio (terminetto)': 'CdC Terminetto',
    'CdC Pisa': 'CdC Pisa Via Garibaldi',
    'CdC Marina Pisa': 'CdC Marina di Pisa',
    'CdC Crespina': 'CdC Crespina Lorenzana',
    'CdC San Giuliano': 'CdC San Giuliano Terme',
}

# Mappatura nomi attrezzature Stima Arredi → Codici Catalogo
MAPPATURA_ATTREZZATURE = {
    'Letto elettrico degenza (LINET)': 'ATTR003',  # Letto degenza elettrico ✓
    'ECG': 'DIAG001',  # ECG (con trasmissione tracciati)
    'LAMPADA VISITA SU STATIVO': 'ATTR005',  # Lampada visita ✓
    'FRIGORIFERO': 'ATTR006',  # Frigofarmaco
    'DAE+ ASPIRATORE PER CARRELLO EMERGENZA': 'ATTR004',  # DAE con aspiratore ✓
    'Lavapadelle (ARJO)': 'ATTR007',  # Lavapadelle ✓
    'Vuotatoio (ARJO)': 'ATTR008',  # Vuotatorio ✓
    'Sollevatore (ARJO)': 'ATTR009',  # Sollevatore ✓
    'LETTINO VISITA ELETTRICO': 'ATTR001',  # Lettino visita elettrico
    'Lettino visita di tipo ginecologico (FAVERO)': 'ATTR002',  # Lettino ginecologico ✓
    'ECOGRAFO': 'DIAG004',  # Ecografo portatile
    'spirometro da mettere in rete': 'DIAG003',  # Spirometro
}

def carica_dati_esistenti():
    """Carica dati esistenti"""
    print("📥 Caricamento dati esistenti...")

    df_strutture = pd.read_csv('strutture_sanitarie.csv')
    df_catalogo = pd.read_csv('dotazioni_telemedicina_catalogo.csv')
    df_dotazioni = pd.read_csv('dotazioni_strutture_telemedicina.csv')

    print(f"  ✅ Strutture: {len(df_strutture)}")
    print(f"  ✅ Catalogo: {len(df_catalogo)}")
    print(f"  ✅ Dotazioni esistenti: {len(df_dotazioni)}")

    return df_strutture, df_catalogo, df_dotazioni

def carica_tecnologie_arredi():
    """Carica tecnologie estratte da Stima Arredi"""
    print("\n📥 Caricamento tecnologie da Stima Arredi...")

    df_tech = pd.read_csv('tecnologie_arredi_pnrr.csv')
    print(f"  ✅ Tecnologie: {len(df_tech)}")

    return df_tech

def mappa_strutture(df_tech, df_strutture):
    """Mappa nomi strutture a codici"""
    print("\n🔄 Mappatura strutture...")

    # Crea dizionario Nome → Codice
    mapping = {}
    for _, row in df_strutture.iterrows():
        nome = row['Nome_Struttura'].strip()
        codice = row['Codice'].strip()
        mapping[nome] = codice

    # Mappa le strutture
    strutture_non_trovate = []
    for nome in df_tech['Struttura'].unique():
        if nome not in mapping:
            strutture_non_trovate.append(nome)

    if strutture_non_trovate:
        print(f"  ⚠️  Strutture non trovate: {len(strutture_non_trovate)}")
        for nome in strutture_non_trovate[:5]:
            print(f"    - {nome}")
    else:
        print(f"  ✅ Tutte le {len(df_tech['Struttura'].unique())} strutture mappate")

    return mapping

def mappa_attrezzature(df_tech):
    """Mappa attrezzature a codici catalogo"""
    print("\n🔄 Mappatura attrezzature...")

    attrezzature_non_mappate = []
    for attr in df_tech['Attrezzatura'].unique():
        if attr not in MAPPATURA_ATTREZZATURE:
            attrezzature_non_mappate.append(attr)

    if attrezzature_non_mappate:
        print(f"  ⚠️  Attrezzature non mappate: {len(attrezzature_non_mappate)}")
        for attr in attrezzature_non_mappate:
            print(f"    - {attr}")
    else:
        print(f"  ✅ Tutte le {len(df_tech['Attrezzatura'].unique())} attrezzature mappate")

    return attrezzature_non_mappate

def integra_dotazioni(df_tech, df_strutture, df_catalogo, df_dotazioni_esistenti):
    """Integra le nuove dotazioni con quelle esistenti"""
    print("\n🔄 Integrazione dotazioni...")

    # Mapping strutture (con normalizzazione nomi)
    mapping_strutture = {}
    for _, row in df_strutture.iterrows():
        mapping_strutture[row['Nome_Struttura'].strip()] = row['Codice'].strip()

    # Aggiungi anche le varianti dal file Arredi
    for nome_arredi, nome_registro in MAPPATURA_STRUTTURE.items():
        if nome_registro in mapping_strutture:
            mapping_strutture[nome_arredi] = mapping_strutture[nome_registro]

    nuove_righe = []
    aggiornamenti = 0
    aggiunte = 0

    for _, row in df_tech.iterrows():
        nome_struttura = row['Struttura']
        attrezzatura = row['Attrezzatura']
        quantita = row['Quantita']

        # Mappa struttura
        if nome_struttura not in mapping_strutture:
            continue
        codice_struttura = mapping_strutture[nome_struttura]

        # Mappa attrezzatura
        if attrezzatura not in MAPPATURA_ATTREZZATURE:
            continue
        codice_dotazione = MAPPATURA_ATTREZZATURE[attrezzatura]

        # Verifica se esiste già
        esistente = df_dotazioni_esistenti[
            (df_dotazioni_esistenti['Codice_Struttura'] == codice_struttura) &
            (df_dotazioni_esistenti['Codice_Dotazione'] == codice_dotazione)
        ]

        if len(esistente) > 0:
            # Aggiorna quantità (sostituisce con valore PNRR definitivo)
            idx = esistente.index[0]
            df_dotazioni_esistenti.loc[idx, 'Quantita_Richiesta'] = quantita
            df_dotazioni_esistenti.loc[idx, 'Note'] = 'Da Stima Arredi PNRR'
            aggiornamenti += 1
        else:
            # Aggiungi nuova riga
            nuove_righe.append({
                'Codice_Struttura': codice_struttura,
                'Codice_Dotazione': codice_dotazione,
                'Quantita_Presente': 0,
                'Quantita_Richiesta': quantita,
                'Stato_Finanziamento': 'DA_ACQUISTARE',
                'Note': 'Da Stima Arredi PNRR'
            })
            aggiunte += 1

    # Aggiungi nuove righe
    if nuove_righe:
        df_nuove = pd.DataFrame(nuove_righe)
        df_dotazioni_finale = pd.concat([df_dotazioni_esistenti, df_nuove], ignore_index=True)
    else:
        df_dotazioni_finale = df_dotazioni_esistenti

    print(f"  ✅ Aggiornamenti: {aggiornamenti}")
    print(f"  ✅ Nuove aggiunte: {aggiunte}")
    print(f"  ✅ Totale dotazioni: {len(df_dotazioni_finale)}")

    return df_dotazioni_finale

def main():
    print("=" * 80)
    print("INTEGRAZIONE TECNOLOGIE DA STIMA ARREDI PNRR")
    print("=" * 80)

    # Carica dati
    df_strutture, df_catalogo, df_dotazioni = carica_dati_esistenti()
    df_tech = carica_tecnologie_arredi()

    # Mappa
    mappa_strutture(df_tech, df_strutture)
    mappa_attrezzature(df_tech)

    # Integra
    df_dotazioni_aggiornate = integra_dotazioni(df_tech, df_strutture, df_catalogo, df_dotazioni)

    # Salva backup
    print("\n💾 Backup file originale...")
    df_dotazioni.to_csv('dotazioni_strutture_telemedicina.csv.bak', index=False)
    print("  ✅ dotazioni_strutture_telemedicina.csv.bak")

    # Salva aggiornato
    print("\n💾 Salvataggio dotazioni aggiornate...")
    df_dotazioni_aggiornate.to_csv('dotazioni_strutture_telemedicina_INTEGRATO.csv', index=False)
    print("  ✅ dotazioni_strutture_telemedicina_INTEGRATO.csv")

    print("\n" + "=" * 80)
    print("✅ INTEGRAZIONE COMPLETATA")
    print("=" * 80)
    print("\n⚠️  IMPORTANTE:")
    print("  1. Verifica il file dotazioni_strutture_telemedicina_INTEGRATO.csv")
    print("  2. Se OK, rinomina:")
    print("     cp dotazioni_strutture_telemedicina_INTEGRATO.csv dotazioni_strutture_telemedicina.csv")
    print("  3. ⚠️  NON eseguire integra_anagrafiche_v3.py dopo questa integrazione!")
    print("     (quello script rigenera i file sovrascrivendo i dati PNRR)")

if __name__ == "__main__":
    main()
