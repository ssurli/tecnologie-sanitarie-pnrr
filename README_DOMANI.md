# 🌅 Lavoro Preparato per Domani

**Data preparazione**: 11 Dicembre 2024 (sera)
**File Master ricevuto**: ELENCO PROGETTI CdC E OdC.xlsx - PNRR.csv

---

## 📊 Situazione Attuale

### Stato Repository
✅ **Clean** e aggiornato
✅ **Dotazioni ripristinate** a 316 (pre-integrazione Stima Arredi)
✅ **Dashboard funzionante** con dati corretti

### Anagrafica Strutture
- **File attuale**: `strutture_sanitarie.csv` (65 strutture: 53 CDC + 12 ODC)
- **File master**: `ELENCO PROGETTI CdC E OdC.xlsx - PNRR.csv` (33 strutture PNRR: 25 CDC + 8 ODC)

---

## ⚠️ PROBLEMA IDENTIFICATO

### Mismatch PNRR Critico

**14 CDC** hanno PNRR errato:
- Master dice: `VALIDATA = NO`
- Anagrafica attuale dice: `PNRR = SI`

Questo causa:
- ❌ Fabbisogni PNRR sovrastimati
- ❌ Report direzione con dati sbagliati
- ❌ Dashboard priorità errate

### Elenco 14 CDC da Correggere

1. CdC di PONTREMOLI
2. CdC TERMINETTO (Viareggio)
3. CdC di CAMAIORE
4. CdC PESCAGLIA
5. CdC COLLESALVETTI
6. CdC LIVORNO CENTRO
7. CdC CRESPINA LORENZANA
8. CdC VECCHIANO
9. CdC CASCINA
10. CdC MARINA DI PISA
11. CdC PISA VIA GARIBALDI
12. CdC PORTOFERRAIO
13. CdC SUVERETO
14. CdC CECINA

---

## 📁 File Creati Stanotte

### 1. Analisi e Report

| File | Descrizione |
|------|-------------|
| `analisi_confronto_anagrafiche.py` | Script analisi completa Master vs Attuale |
| `REPORT_CONFRONTO_ANAGRAFICHE.md` | Report dettagliato con tutti i finding |

### 2. Strumenti di Correzione

| File | Descrizione |
|------|-------------|
| `correggi_pnrr_da_master.py` | Script automatico per correggere PNRR |

**Cosa fa lo script**:
- ✅ Legge Master e Attuale
- ✅ Usa fuzzy matching per associare nomi simili
- ✅ Corregge solo campo PNRR (resto invariato)
- ✅ Crea backup automatico
- ✅ Genera report correzioni
- ✅ Chiede conferma prima di salvare
- ✅ NON tocca strutture non nel Master

---

## 🎯 Piano per Domani Mattina

### Step 1: Review (15 min)

```bash
# Leggi il report completo
cat REPORT_CONFRONTO_ANAGRAFICHE.md

# Esegui analisi per vedere situazione live
python analisi_confronto_anagrafiche.py
```

### Step 2: Decisione

**Opzione A - Correzione Automatica (CONSIGLIATA)**

Se sei d'accordo con i finding, procedi con la correzione automatica:

```bash
python correggi_pnrr_da_master.py
```

Lo script:
1. Mostra le 14 correzioni che farà
2. Chiede conferma
3. Crea backup
4. Genera `strutture_sanitarie_CORRETTE.csv`
5. Genera report dettagliato

**Opzione B - Verifica Manuale**

Se vuoi verificare prima con il team:
1. Usa il report per discutere le 14 strutture
2. Correggi manualmente `strutture_sanitarie.csv`
3. Rigenera dati

### Step 3: Applicazione (se OK)

```bash
# Verifica file corretto
head -20 strutture_sanitarie_CORRETTE.csv
tail -20 strutture_sanitarie_CORRETTE.csv

# Se tutto OK, applica
cp strutture_sanitarie_CORRETTE.csv strutture_sanitarie.csv

# Rigenera dati integrati
python integra_anagrafiche_v3.py

# Verifica dashboard
streamlit run dashboard_telemedicina.py
```

### Step 4: Commit

```bash
git add strutture_sanitarie.csv
git commit -m "fix: Corregge PNRR da file master ELENCO PROGETTI

Allinea 14 CDC da PNRR=SI a PNRR=NO secondo file master.
Fonte: ELENCO PROGETTI CdC E OdC.xlsx - PNRR.csv

Strutture corrette:
- CdC di PONTREMOLI
- CdC TERMINETTO
- CdC di CAMAIORE
- CdC PESCAGLIA
- CdC COLLESALVETTI
- CdC LIVORNO CENTRO
- CdC CRESPINA LORENZANA
- CdC VECCHIANO
- CdC CASCINA
- CdC MARINA DI PISA
- CdC PISA VIA GARIBALDI
- CdC PORTOFERRAIO
- CdC SUVERETO
- CdC CECINA"

git push
```

---

## 📊 Impatto Atteso

### Prima
- Strutture PNRR=SI: **37**
- Fabbisogno PNRR: €X (sovrastimato)

### Dopo
- Strutture PNRR=SI: **23** (-14, -37.8%)
- Fabbisogno PNRR: €Y (corretto)

---

## ✅ Note Importanti

1. **Strutture Extra**: Le 32 strutture nell'anagrafica che non sono nel Master vengono **mantenute** (sono strutture operative valide, non-PNRR)

2. **Solo PNRR Cambia**: Lo script modifica SOLO il campo PNRR, tutti gli altri campi restano invariati

3. **Backup Automatico**: Lo script crea backup automatico prima di qualsiasi modifica

4. **Fuzzy Matching**: Lo script usa matching intelligente per nomi simili:
   - "CdC di PONTREMOLI" ↔ "CdC Pontremoli"
   - "CdC SAN LEONARDO IN TREPONZIO" ↔ "CdC S. Leonardo In Treponzio"

5. **File Master è Autoritativo**: Il file ELENCO PROGETTI è la fonte ufficiale per PNRR validati

---

## 🔄 Dopo la Correzione PNRR

Una volta corretta l'anagrafica, potrai affrontare il tema delle **tecnologie aggiuntive** (file `tecnologie_*_dettaglio.csv` vs "Stima arredi PNRR").

---

## 🆘 Se Serve Aiuto

- **Report completo**: `REPORT_CONFRONTO_ANAGRAFICHE.md`
- **Script analisi**: `python analisi_confronto_anagrafiche.py`
- **Script correzione**: `python correggi_pnrr_da_master.py`

Tutti gli script sono **sicuri** (creano backup e chiedono conferma).

---

**Buon lavoro! 🚀**
