# 🚀 Guida Rapida - Dashboard Telemedicina

## Avvio Rapido in 3 Passi

### 1️⃣ Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 2️⃣ Avvia la dashboard

```bash
streamlit run dashboard_telemedicina.py
```

### 3️⃣ Apri il browser

La dashboard si aprirà automaticamente su `http://localhost:8501`

---

## 📊 Cosa Puoi Fare

### Vista: Riepilogo Generale
- Vedi quante strutture hai (CDC/ODC)
- Visualizza il fabbisogno totale in €
- Guarda la distribuzione costi tra Dispositivi Diagnostici e Attrezzature

### Vista: Elenco Strutture
- Filtra per tipologia (CDC/ODC)
- Filtra per provincia (MS, LU, PI, LI)
- Vedi il fabbisogno per ogni struttura

### Vista: Dettaglio Dotazioni Struttura
- Seleziona una struttura
- Vedi cosa c'è e cosa manca
- Controlla i costi per categoria

### Vista: Fabbisogno Complessivo
- Vedi il totale per ogni tipo di dotazione
- Identifica le strutture con più fabbisogno
- Calcola il budget necessario

---

## 🔧 Personalizzazione Rapida

### Aggiungere una struttura

Apri `strutture_sanitarie.csv` e aggiungi:

```csv
CdC,CDC018,CdC Lucca,Lucca,LU,Via Nuova 1,55100,SI
```

### Configurare dotazioni per una struttura

Apri `dotazioni_strutture_telemedicina.csv` e aggiungi:

```csv
CDC018,DIAG001,0,1,Da acquistare
CDC018,ATTR001,0,2,Da acquistare
```

Dove:
- `CDC018` = codice struttura
- `DIAG001` = codice dotazione (vedi catalogo)
- `0` = quantità presente
- `1` = quantità richiesta
- `Da acquistare` = nota

### Aggiornare quando acquisti

Quando compri una dotazione, modifica:

```csv
CDC018,DIAG001,1,1,Completo
```

(Cambia `Quantita_Presente` da 0 a 1)

---

## 📋 Dotazioni Disponibili

### 🔬 Dispositivi Diagnostici

| Codice | Descrizione | Costo |
|--------|-------------|-------|
| DIAG001 | ECG | €3.000 |
| DIAG002 | Holter ECG 24h | €2.500 |
| DIAG003 | Spirometro | €1.800 |
| DIAG004 | Ecografo portatile | €15.000 |
| DIAG005 | Monitor multiparametrico | €4.500 |

### 🛏️ Attrezzature Sanitarie

| Codice | Descrizione | Costo |
|--------|-------------|-------|
| ATTR001 | Lettino visita elettrico | €848 |
| ATTR002 | Lettino ginecologico | €1.767 |
| ATTR003 | Letto degenza elettrico | €1.723 |
| ATTR004 | DAE con aspiratore | €1.500 |
| ATTR005 | Lampada visita | €1.200 |
| ATTR006 | Frigofarmaco | €3.000 |
| ATTR007 | Lavapadelle | €5.048 |
| ATTR008 | Vuotatorio | €1.868 |
| ATTR009 | Sollevatore/Sollevapazienti | €4.680 |

---

## 💡 Casi d'Uso Comuni

### Caso 1: "Devo pianificare gli acquisti per il 2025"

1. Vai su **Fabbisogno Complessivo**
2. Guarda il riepilogo per dotazione
3. Identifica le priorità
4. Esporta i dati (se necessario, prendi screenshot)

### Caso 2: "Una struttura ha bisogno di nuove dotazioni"

1. Vai su **Dettaglio Dotazioni Struttura**
2. Seleziona la struttura
3. Vedi cosa manca
4. Aggiorna il file CSV se necessario

### Caso 3: "Voglio un report per il Direttore"

1. Vai su **Riepilogo Generale**
2. Prendi note sui KPI principali
3. Vai su **Fabbisogno Complessivo**
4. Prendi screenshot del totale

### Caso 4: "Ho completato un acquisto"

1. Apri `dotazioni_strutture_telemedicina.csv`
2. Trova la riga della dotazione acquistata
3. Modifica `Quantita_Presente`
4. Cambia `Note` in "Completo"
5. Riavvia la dashboard per vedere i nuovi dati

---

## ⚠️ Risoluzione Problemi

### La dashboard non si avvia

```bash
# Controlla che Streamlit sia installato
streamlit --version

# Se non funziona, reinstalla
pip install --upgrade streamlit
```

### I dati non sono corretti

1. Verifica i file CSV
2. Controlla che i codici siano coerenti
3. Assicurati che i numeri usino il punto (non virgola) per i decimali

### Voglio resettare i dati

```bash
git checkout strutture_sanitarie.csv
git checkout dotazioni_strutture_telemedicina.csv
```

---

## 📞 Serve Aiuto?

Consulta la documentazione completa in `README_TELEMEDICINA.md`

---

**Buon lavoro! 🏥**
