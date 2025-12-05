# Dashboard Telemedicina
## Sistema di Gestione Dotazioni Tecnologiche - USL Toscana Nord Ovest

## 📋 Descrizione

Sistema integrato per la gestione e visualizzazione delle dotazioni tecnologiche per la telemedicina nelle strutture sanitarie (Case di Comunità e Ospedali di Comunità) PNRR e non PNRR della USL Toscana Nord Ovest.

### Funzionalità Principali

- **Anagrafica Strutture**: Gestione completa delle strutture sanitarie con informazioni geografiche
- **Catalogo Dotazioni**: Database delle dotazioni tecnologiche suddivise in:
  - **Dispositivi Diagnostici**: ECG, Holter, Spirometro, Ecografo, Monitor multiparametrico
  - **Attrezzature Sanitarie**: Lettini, Letti, DAE, Lampade, Frigofarmaco, Lavapadelle, Vuotatori, Sollevatori
- **Fabbisogno Complessivo**: Calcolo automatico delle dotazioni necessarie con costi unitari e totali
- **Dashboard Interattiva**: Visualizzazione dati con grafici e tabelle

## 📁 Struttura File

### File CSV (Database)

```
strutture_sanitarie.csv              # Anagrafica completa strutture (CDC/ODC)
dotazioni_telemedicina_catalogo.csv  # Catalogo dotazioni con costi unitari
dotazioni_strutture_telemedicina.csv # Dotazioni per struttura (presente/richiesto)
```

### Script

```
dashboard_telemedicina.py            # Dashboard Streamlit interattiva
analisi_tecnologie_sanitarie.py     # Script analisi tecnologie PNRR (esistente)
```

## 🚀 Installazione e Avvio

### 1. Installare le dipendenze

```bash
pip install -r requirements.txt
```

### 2. Avviare la dashboard

```bash
streamlit run dashboard_telemedicina.py
```

La dashboard si aprirà automaticamente nel browser predefinito all'indirizzo `http://localhost:8501`

## 📊 Utilizzo Dashboard

### Pagina 1: Riepilogo Generale

Visualizza:
- KPI principali (numero strutture, fabbisogno totale)
- Distribuzione costi per categoria (Dispositivi vs Attrezzature)
- Top 10 dotazioni per fabbisogno

### Pagina 2: Elenco Strutture

Permette di:
- Filtrare strutture per tipologia (CDC/ODC)
- Filtrare per provincia
- Filtrare per appartenenza PNRR (SI/NO)
- Visualizzare fabbisogno per struttura

### Pagina 3: Dettaglio Dotazioni Struttura

Visualizza per ogni struttura:
- Informazioni anagrafiche complete
- Dotazioni presenti vs richieste
- Quantità da acquistare
- Costi per categoria
- Note operative

### Pagina 4: Fabbisogno Complessivo

Mostra:
- Riepilogo completo per dotazione
- Fabbisogno aggregato per struttura
- Top 10 strutture per investimento necessario
- Totale complessivo generale

## 📝 Struttura Dati CSV

### strutture_sanitarie.csv

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| Tipologia | CdC/OdC | Tipo struttura |
| Codice | String | Codice univoco struttura |
| Nome_Struttura | String | Nome completo |
| Comune | String | Comune |
| Provincia | String | Sigla provincia (MS/LU/PI/LI) |
| Indirizzo | String | Via e numero civico |
| CAP | String | Codice postale |
| PNRR | SI/NO | Appartenenza PNRR |

### dotazioni_telemedicina_catalogo.csv

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| Categoria | String | Dispositivi Diagnostici / Attrezzature Sanitarie |
| Codice | String | Codice univoco dotazione (DIAG/ATTR) |
| Descrizione | String | Nome completo dotazione |
| Costo_Unitario_EUR | Decimal | Costo per unità in € |

### dotazioni_strutture_telemedicina.csv

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| Codice_Struttura | String | Riferimento a strutture_sanitarie.csv |
| Codice_Dotazione | String | Riferimento a catalogo |
| Quantita_Presente | Integer | Quantità già disponibile |
| Quantita_Richiesta | Integer | Quantità necessaria totale |
| Note | String | Note operative (es. "Da acquistare", "Completo") |

## 🔧 Personalizzazione

### Aggiungere una Nuova Struttura

1. Apri `strutture_sanitarie.csv`
2. Aggiungi una nuova riga con tutti i campi compilati
3. Assegna un codice univoco (es. CDC018, ODC006)
4. Salva il file

### Aggiungere una Nuova Dotazione al Catalogo

1. Apri `dotazioni_telemedicina_catalogo.csv`
2. Aggiungi la nuova dotazione con:
   - Categoria appropriata
   - Codice univoco (DIAG### o ATTR###)
   - Descrizione
   - Costo unitario
3. Salva il file

### Configurare Dotazioni per una Struttura

1. Apri `dotazioni_strutture_telemedicina.csv`
2. Aggiungi righe per ogni dotazione necessaria:
   - Codice_Struttura: riferimento alla struttura
   - Codice_Dotazione: riferimento al catalogo
   - Quantita_Presente: dotazioni già presenti
   - Quantita_Richiesta: dotazioni totali necessarie
   - Note: stato o osservazioni
3. Salva il file

Il sistema calcolerà automaticamente:
- Quantità da acquistare = Richiesta - Presente
- Costo totale = Quantità da acquistare × Costo unitario

## 📈 Esempi di Utilizzo

### Scenario 1: Verificare il Fabbisogno di una Struttura

1. Avvia la dashboard: `streamlit run dashboard_telemedicina.py`
2. Vai su "Dettaglio Dotazioni Struttura"
3. Seleziona la struttura dal menu a tendina
4. Visualizza le dotazioni presenti/richieste e il costo totale

### Scenario 2: Pianificare gli Acquisti

1. Vai su "Fabbisogno Complessivo"
2. Espandi le categorie per vedere il riepilogo per dotazione
3. Ordina per costo totale per prioritizzare gli acquisti
4. Esporta i dati (funzionalità in arrivo)

### Scenario 3: Analisi per Provincia

1. Vai su "Elenco Strutture"
2. Filtra per provincia specifica (es. solo "PI")
3. Visualizza il fabbisogno aggregato per quella provincia

## 🔄 Integrazione con Progetto PNRR Esistente

Questo sistema si integra con il progetto PNRR esistente:

- **Script esistente** (`analisi_tecnologie_sanitarie.py`): Analisi dotazioni PNRR già acquistate/pianificate
- **Nuovo sistema** (`dashboard_telemedicina.py`): Gestione dotazioni telemedicina e fabbisogno futuro

Le strutture sono le stesse (CDC e ODC PNRR) con l'aggiunta di strutture non PNRR.

### Workflow Completo

```bash
# 1. Analizzare dotazioni PNRR esistenti
python3 analisi_tecnologie_sanitarie.py

# 2. Pianificare dotazioni telemedicina
streamlit run dashboard_telemedicina.py
```

## 💡 Best Practices

### Gestione Dati

- ✅ Mantenere backup dei file CSV prima di modifiche importanti
- ✅ Usare codici univoci per strutture e dotazioni
- ✅ Verificare i costi unitari prima di inserirli
- ✅ Aggiornare le note per tracciare lo stato delle dotazioni

### Aggiornamento Stato Dotazioni

Quando una dotazione viene acquistata:

1. Aggiorna `Quantita_Presente` in `dotazioni_strutture_telemedicina.csv`
2. Modifica la `Note` da "Da acquistare" a "Completo" o "Parziale"
3. Il sistema ricalcolerà automaticamente il fabbisogno residuo

## 📊 Metriche Principali

### KPI Disponibili nella Dashboard

- **Numero Strutture**: Totale, CDC, ODC
- **Fabbisogno Totale**: Costo complessivo degli acquisti necessari
- **Distribuzione per Categoria**: % Dispositivi vs Attrezzature
- **Top Strutture**: Classifiche per investimento necessario
- **Dotazioni Critiche**: Più richieste e più costose

## 🔍 Troubleshooting

### Errore "File not found"

```bash
# Verifica di essere nella directory corretta
cd /path/to/tecnologie-sanitarie-pnrr
ls *.csv
```

### Dati non visualizzati correttamente

1. Verifica formato CSV (separatore: virgola)
2. Controlla encoding file (UTF-8)
3. Verifica coerenza codici tra file (Codice_Struttura, Codice_Dotazione)

### Dashboard non si avvia

```bash
# Reinstalla dipendenze
pip install --upgrade -r requirements.txt

# Verifica versione Streamlit
streamlit --version
```

## 📞 Supporto

Per assistenza tecnica o modifiche al sistema, contattare:
- RUP della struttura di riferimento
- Team ICT USL Toscana Nord Ovest

## 📝 Note Tecniche

- **Encoding**: UTF-8
- **Separatore CSV**: Virgola (,)
- **Formato Numeri**: Decimale con punto (1234.56)
- **Browser supportati**: Chrome, Firefox, Safari, Edge (versioni recenti)

## 🔐 Sicurezza e Privacy

- I dati sono gestiti localmente
- Nessun dato sensibile viene trasmesso in rete
- Backup consigliato dei file CSV su sistemi aziendali

## 📅 Changelog

### Versione 1.0 (Dicembre 2024)

- ✅ Sistema completo dotazioni telemedicina
- ✅ Dashboard interattiva con 4 viste
- ✅ Calcolo automatico fabbisogno
- ✅ 22 strutture configurate (17 CDC + 5 ODC)
- ✅ 14 dotazioni nel catalogo
- ✅ Grafici interattivi con Plotly

### Sviluppi Futuri

- 🔄 Export Excel report fabbisogno
- 🔄 Mappa geografica strutture con GPS
- 🔄 Gestione fornitori e preventivi
- 🔄 Tracking ordini e consegne
- 🔄 Integrazione con sistema gestione magazzino

---

**Progetto**: PNRR - Missione 6 Salute - Telemedicina
**Ultimo aggiornamento**: Dicembre 2024
**USL**: Toscana Nord Ovest
