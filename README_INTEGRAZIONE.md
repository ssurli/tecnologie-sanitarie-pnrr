# Integrazione Anagrafiche Reali - Dashboard Telemedicina

## ✅ Integrazione Completata

Il sistema dashboard telemedicina è stato integrato con i dati reali provenienti dai file:
- `CDC_CE_1_claude.csv` - Anagrafiche Case di Comunità
- `ODC_CE_1_claude.csv` - Anagrafiche Ospedali di Comunità
- `ELENCO PROGETTI CdC E OdC.xlsx - PNRR.csv` - Elenco progetti PNRR

## 📊 Statistiche Dati Integrati

### Strutture Sanitarie
- **Totale strutture**: 77
  - **Case di Comunità**: 53
  - **Ospedali di Comunità**: 24
- **Strutture PNRR**: 25
- **Strutture non PNRR**: 52
- **Zone distretto**: 26

### Dotazioni Tecnologiche
- **Configurazioni totali**: 230
- **Dispositivi diagnostici**:
  - ECG (Elettrocardiografo)
  - Holter cardiaco 24h
  - Spirometro
  - Ecografo portatile
  - Monitor multiparametrico

## 📁 Nuovi File Creati

### Script di Integrazione
- `integra_anagrafiche_v2.py` - Script per parsing e integrazione dati
  - Gestisce formato CSV complesso con note iniziali
  - Parsing manuale per massima affidabilità
  - Mapping automatico stato dotazioni (PRESENTE/FINANZIATO/DA ACQUISTARE/NON RICHIESTO)

### File Dati
- `strutture_sanitarie.csv` - Anagrafica completa 77 strutture (aggiornato con dati reali)
- `dotazioni_strutture_telemedicina.csv` - 230 configurazioni dotazioni (aggiornato)
- `strutture_sanitarie_integrate.csv` - Copia dati integrati
- `dotazioni_strutture_telemedicina_integrate.csv` - Copia dotazioni integrate

### File Backup
- `strutture_sanitarie_placeholder_backup.csv` - Backup dati esempio originali
- `dotazioni_strutture_telemedicina_placeholder_backup.csv` - Backup configurazioni esempio

## 🆕 Nuovi Campi Dashboard

La dashboard ora visualizza:

### Anagrafica Strutture
- **Zona Distretto** - Zona territoriale di appartenenza (Lunigiana, Apuane, Valle del Serchio, etc.)
- **Classificazione** - Hub/Spoke per CDC
- **Posti Letto** - Numero posti letto per ODC
- Tutti i campi esistenti (Tipologia, Nome, Comune, PNRR, etc.)

### Filtri Migliorati
- Filtro per **Zona Distretto** (26 zone disponibili)
- Filtro per **Classificazione** (Hub/Spoke)
- Filtri esistenti (Tipologia, PNRR)

## 🚀 Come Usare

### 1. Avviare la Dashboard

```bash
# Installare dipendenze (se non già fatto)
pip install -r requirements.txt

# Avviare dashboard
streamlit run dashboard_telemedicina.py
```

### 2. Navigare tra le Viste

La dashboard offre 4 viste:

#### 📊 Riepilogo Generale
- Totale 77 strutture (53 CDC + 24 ODC)
- Fabbisogno complessivo calcolato automaticamente
- Grafici distribuzione costi per categoria

#### 🏥 Elenco Strutture
- Tabella completa con nuovi campi (Zona, Classificazione)
- Filtri multipli per analisi mirate
- Fabbisogno per struttura

#### 🔍 Dettaglio Dotazioni Struttura
- Seleziona una delle 77 strutture
- Visualizza dotazioni presenti vs richieste
- Suddivisione per categoria (Dispositivi Diagnostici / Attrezzature Sanitarie)

#### 💰 Fabbisogno Complessivo
- Riepilogo aggregato per dotazione
- Top 10 strutture per fabbisogno
- Calcolo automatico quantità da acquistare

## 🔄 Rieseguire Integrazione

Se i file sorgente vengono aggiornati, rieseguire:

```bash
python3 integra_anagrafiche_v2.py
```

Questo rigenerà:
- `strutture_sanitarie_integrate.csv`
- `dotazioni_strutture_telemedicina_integrate.csv`

Poi sostituire i file principali:

```bash
cp strutture_sanitarie_integrate.csv strutture_sanitarie.csv
cp dotazioni_strutture_telemedicina_integrate.csv dotazioni_strutture_telemedicina.csv
```

## 📝 Mapping Stato Dotazioni

Lo script di integrazione mappa automaticamente:

| Valore Originale | Quantità Presente | Quantità Richiesta | Note |
|------------------|-------------------|-------------------|------|
| PRESENTE | 1 | 1 | Presente |
| FINANZIATO | 1 | 1 | Presente |
| DA ACQUISTARE | 0 | 1 | Da acquistare |
| NON RICHIESTO | 0 | 0 | Non richiesto |

## 🎯 Esempi di Analisi

### Filtrare solo strutture PNRR
1. Vai su "Elenco Strutture"
2. In filtro PNRR seleziona solo "SI"
3. Visualizza le 25 strutture PNRR

### Analizzare una Zona specifica
1. Vai su "Elenco Strutture"
2. In filtro "Zona Distretto" seleziona es. "Lunigiana"
3. Vedi tutte le strutture della zona

### Identificare strutture con più fabbisogno
1. Vai su "Fabbisogno Complessivo"
2. Guarda il grafico "Top 10 Strutture"
3. Vedi la tabella completa ordinata per fabbisogno

### Pianificare acquisti per dispositivo
1. Vai su "Fabbisogno Complessivo"
2. Espandi categoria "Dispositivi Diagnostici"
3. Vedi quantità totale da acquistare e costo per ogni dispositivo

## ⚙️ Struttura Tecnica

### File CSV Principali

**strutture_sanitarie.csv**
```csv
Tipologia,Codice,Nome_Struttura,Zona,Classificazione,Comune,Provincia,Indirizzo,CAP,PNRR,Posti_Letto
CdC,CDC001,CdC Aulla,Lunigiana,Hub,Aulla,,Piazza Roma,,NO,
OdC,ODC001,OdC Massa,Apuane,,Massa,,,,SI,20
```

**dotazioni_strutture_telemedicina.csv**
```csv
Codice_Struttura,Codice_Dotazione,Quantita_Presente,Quantita_Richiesta,Note
CDC001,DIAG001,0,1,Da acquistare
CDC001,DIAG003,1,1,Presente
```

**dotazioni_telemedicina_catalogo.csv** (invariato)
```csv
Categoria,Codice,Descrizione,Costo_Unitario_EUR
Dispositivi Diagnostici,DIAG001,ECG,3000.00
```

## 🔍 Verifica Integrità Dati

Eseguire questo script per verificare:

```python
import pandas as pd

# Carica dati
df_strutt = pd.read_csv('strutture_sanitarie.csv')
df_dot = pd.read_csv('dotazioni_strutture_telemedicina.csv')
df_cat = pd.read_csv('dotazioni_telemedicina_catalogo.csv')

# Verifica coerenza codici
codici_strutture = set(df_strutt['Codice'])
codici_dotazioni = set(df_dot['Codice_Struttura'])
codici_catalogo = set(df_cat['Codice'])
codici_dot_usati = set(df_dot['Codice_Dotazione'])

print(f"Strutture: {len(codici_strutture)}")
print(f"Strutture con dotazioni: {len(codici_dotazioni)}")
print(f"Dotazioni nel catalogo: {len(codici_catalogo)}")
print(f"Dotazioni usate: {len(codici_dot_usati)}")

# Verifica codici orfani
orfani = codici_dotazioni - codici_strutture
if orfani:
    print(f"\n⚠️ Codici dotazioni senza struttura: {orfani}")
else:
    print("\n✅ Tutti i codici dotazioni hanno una struttura")

dot_orfane = codici_dot_usati - codici_catalogo
if dot_orfane:
    print(f"⚠️ Codici dotazione non in catalogo: {dot_orfane}")
else:
    print("✅ Tutte le dotazioni usate sono nel catalogo")
```

## 📞 Supporto

Per problemi o domande sull'integrazione:
1. Verificare che i file sorgente (CDC_CE_1_claude.csv, ODC_CE_1_claude.csv) non siano stati modificati
2. Rieseguire lo script di integrazione
3. Verificare i log di errore

## 🔄 Prossimi Sviluppi

- [ ] Completare Province e CAP mancanti
- [ ] Aggiungere coordinate GPS per mappa geografica
- [ ] Integrare dati da ELENCO PROGETTI per date fine lavori
- [ ] Export Excel report personalizzati
- [ ] Tracking ordini e consegne

---

**Integrazione completata**: Dicembre 2024
**Dati sorgente**: CDC_CE_1_claude.csv (53 CDC), ODC_CE_1_claude.csv (24 ODC)
**Sistema**: Dashboard Telemedicina - USL Toscana Nord Ovest
