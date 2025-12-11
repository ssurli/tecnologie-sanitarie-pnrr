# 🔄 Guida Aggiornamento Dati Dashboard

## 📋 Tipi di File e Script

| Tipo File | Contenuto | Script | Frequenza |
|-----------|-----------|--------|-----------|
| **CDC_CE_*.xlsx** | Anagrafiche strutture CDC | `aggiorna_dati.py` (preview)<br/>+ integrazione manuale | Ad hoc |
| **ODC_CE_*.xlsx** | Anagrafiche strutture ODC | `aggiorna_dati.py` (preview)<br/>+ integrazione manuale | Ad hoc |
| **Stima arredi PNRR.xlsx** | Tecnologie da sezione finale | `importa_arredi_pnrr.py`<br/>+ `integra_tecnologie_arredi.py` | Periodico |

**⚠️ NOTA**: Per "Stima arredi PNRR" vengono estratte **SOLO le tecnologie** (righe in fondo), NON gli arredi.

## 📥 Processo di Aggiornamento Generale

### 1. **Ricevi nuovi file**
Quando ti arrivano file aggiornati (es. `CDC_CE_1.xlsx`, `Stima arredi PNRR.xlsx`):

### 2. **Backup automatico**
```bash
# Lo script crea automaticamente un backup in backup_YYYYMMDD_HHMMSS/
python aggiorna_dati.py CDC_CE_1.xlsx
```

### 3. **Verifica dati**
Lo script mostra:
- ✅ Numero di righe e colonne
- ✅ Colonne presenti
- ✅ Validazione dati
- ⚠️ Eventuali warning

### 4. **Aggiornamento manuale CSV**
Se i dati sono OK, aggiorna manualmente i CSV:

#### Per strutture:
```bash
# Copia i dati nel formato corretto
# Esempio: se il file ha nuove strutture
# Aggiungi le righe a strutture_sanitarie.csv
```

#### Per dotazioni:
```bash
# Aggiorna dotazioni_strutture_telemedicina.csv
# Oppure usa integra_anagrafiche_v3.py
```

### 5. **Rigenera dati integrati**
```bash
python integra_anagrafiche_v3.py
```

### 6. **Verifica dashboard**
```bash
streamlit run dashboard_telemedicina.py
```
Controlla che i nuovi dati siano visibili correttamente.

### 7. **Commit e push**
```bash
git add .
git commit -m "feat: Aggiorna dati strutture da CDC_CE_1 del $(date +%Y-%m-%d)"
git push
```

---

## 🎯 Scenari Comuni

### Scenario 1: Nuove strutture CDC/ODC
```bash
# 1. Scarica file da Drive
# 2. Importa
python aggiorna_dati.py CDC_CE_nuove_strutture.xlsx

# 3. Verifica e copia manualmente i dati in strutture_sanitarie.csv
# 4. Rigenera
python integra_anagrafiche_v3.py

# 5. Testa
streamlit run dashboard_telemedicina.py
```

### Scenario 2: Aggiornamento listino prezzi
```bash
# 1. Modifica dotazioni_telemedicina_catalogo.csv
#    Aggiorna i prezzi mantenendo il formato:
#    Categoria,Codice,Descrizione,Costo_Unitario_EUR,IVA_Percentuale,Applicabile_A

# 2. Rigenera dati
python integra_anagrafiche_v3.py

# 3. Rigenera report HTML
python genera_report_html.py

# 4. Commit
git add . && git commit -m "feat: Aggiorna listino prezzi" && git push
```

### Scenario 3: Nuove dotazioni per strutture esistenti
```bash
# 1. Modifica dotazioni_strutture_telemedicina.csv
#    Aggiungi righe con formato:
#    Codice_Struttura,Codice_Dotazione,Quantita_Richiesta,Quantita_Presente,Stato_Finanziamento

# 2. Rigenera
python integra_anagrafiche_v3.py

# 3. Commit
git add . && git commit -m "feat: Aggiunge dotazioni per [strutture]" && git push
```

---

## 📊 File da Drive - Procedure Specifiche

### Tipo 1: File CDC_CE_*.xlsx (Anagrafiche CDC)

**Contenuto**: Strutture Case di Comunità con dotazioni
**Frequenza**: Ad hoc quando ci sono nuove strutture/modifiche

```bash
# 1. Scarica da Google Drive
# 2. Importa (opzionale, per vedere preview)
python aggiorna_dati.py CDC_CE_1.xlsx

# 3. Integra manualmente in strutture_sanitarie.csv e dotazioni_strutture_telemedicina.csv
# 4. Rigenera dati
python integra_anagrafiche_v3.py

# 5. Commit
git add . && git commit -m "feat: Aggiorna strutture CDC da CDC_CE" && git push
```

### Tipo 2: File ODC_CE_*.xlsx (Anagrafiche ODC)

**Contenuto**: Strutture Ospedali di Comunità con dotazioni
**Frequenza**: Ad hoc quando ci sono nuove strutture/modifiche

```bash
# Stesso procedimento dei file CDC_CE
python aggiorna_dati.py ODC_CE_1.xlsx
# ... seguito da integrazione manuale e rigenerazione
```

### Tipo 3: File "Stima arredi PNRR.xlsx" (Tecnologie)

**Contenuto**: Tecnologie/attrezzature da fogli OdC e CdC (NON arredi)
**Frequenza**: Periodico - file condiviso con aggiornamenti continui
**⚠️ IMPORTANTE**: Estrae SOLO tecnologie dalla sezione in fondo (ignora arredi)

**Workflow automatizzato**:

```bash
# 1. Scarica file aggiornato da Google Drive
# 2. Esporta i 2 fogli come CSV:
#    - "OdC" → Stima arredi PNRR.xlsx - OdC.csv
#    - "CdC" → Stima arredi PNRR.xlsx - CdC.csv

# 3. Estrai tecnologie dai CSV
python importa_arredi_pnrr.py

# Output:
# ✅ File creato: tecnologie_arredi_pnrr.csv
# 📊 Totale voci, strutture, attrezzature, costi

# 4. Integra nelle dotazioni esistenti
python integra_tecnologie_arredi.py

# Output:
# ✅ Aggiornamenti: X dotazioni esistenti
# ✅ Nuove aggiunte: Y configurazioni
# ✅ File creato: dotazioni_strutture_telemedicina_INTEGRATO.csv

# 5. VERIFICA il file integrato
head -20 dotazioni_strutture_telemedicina_INTEGRATO.csv
tail -20 dotazioni_strutture_telemedicina_INTEGRATO.csv

# 6. Se OK, applica l'integrazione
cp dotazioni_strutture_telemedicina_INTEGRATO.csv dotazioni_strutture_telemedicina.csv

# 7. Rigenera dati completi
python integra_anagrafiche_v3.py

# 8. Commit e push
git add dotazioni_strutture_telemedicina.csv tecnologie_arredi_pnrr.csv
git commit -m "feat: Aggiorna tecnologie da Stima Arredi PNRR del $(date +%Y-%m-%d)"
git push
```

**Mappatura automatica strutture**:
- OdC Viareggio → OdC TABARRACCI
- OdC Campo Marte → OdC CAMPO DI MARTE Lucca
- OdC Cecina → OdC OSPEDALE DI COMUNITA CECINA Cecina
- OdC Piombino → OdC OSPEDALE DI COMUNITA PIOMBINO Piombino
- OdC Livorno → OdC PADIGLIONE 5 Livorno
- (CDC: mappatura automatica per nome)

---

## ⚠️ Troubleshooting

### Errore: "Colonna mancante"
- Verifica che il file Excel abbia le colonne richieste
- Confronta con i CSV esistenti
- Rinomina le colonne se necessario

### Errore: "Validazione fallita"
- Controlla i valori PNRR (devono essere 'SI' o 'NO')
- Verifica i codici strutture
- Controlla i formati numerici

### Backup corrotto
```bash
# Ripristina dal backup
cp backup_YYYYMMDD_HHMMSS/*.csv .
```

---

## 📝 Checklist Post-Aggiornamento

- [ ] Dati aggiornati nei CSV
- [ ] `integra_anagrafiche_v3.py` eseguito con successo
- [ ] Dashboard testata localmente
- [ ] Report HTML generato
- [ ] Commit e push effettuati
- [ ] Streamlit Cloud aggiornato (verifica dopo 2 min)
- [ ] URL condiviso con colleghi (se necessario)

---

## 🆘 Supporto

Per problemi o dubbi:
1. Controlla i log dello script
2. Verifica il backup in `backup_*/`
3. Confronta i CSV vecchi/nuovi
4. Chiedi assistenza con screenshot dell'errore
