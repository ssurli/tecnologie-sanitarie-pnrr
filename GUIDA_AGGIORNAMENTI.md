# 🔄 Guida Aggiornamento Dati Dashboard

## 📥 Processo di Aggiornamento

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

## 📊 File da Drive - Procedura

### File: "Stima arredi PNRR.xlsx"

**Opzione A - Download manuale:**
1. Scarica da Google Drive
2. Salva in `/home/user/tecnologie-sanitarie-pnrr/`
3. Esegui: `python aggiorna_dati.py "Stima arredi PNRR.xlsx"`

**Opzione B - Link pubblico:**
1. Drive → File → Condividi → "Chiunque abbia il link"
2. Copia link
3. Esegui:
```bash
# Converti link in formato download diretto
# Da: https://drive.google.com/file/d/FILE_ID/view
# A: https://drive.google.com/uc?export=download&id=FILE_ID

wget "https://drive.google.com/uc?export=download&id=FILE_ID" -O "Stima_arredi_PNRR.xlsx"
python aggiorna_dati.py Stima_arredi_PNRR.xlsx
```

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
