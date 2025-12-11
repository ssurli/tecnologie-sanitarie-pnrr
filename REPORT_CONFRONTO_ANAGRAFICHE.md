# 📊 Report Confronto Anagrafiche

**Data**: 11 Dicembre 2024
**File Master**: ELENCO PROGETTI CdC E OdC.xlsx - PNRR.csv
**File Attuale**: strutture_sanitarie.csv

---

## 🔍 Executive Summary

### Numerosità Strutture

| Tipologia | Master | Attuale | Delta |
|-----------|--------|---------|-------|
| **CDC** | 25 | 53 | **+28** |
| **ODC** | 8 | 12 | **+4** |
| **TOTALE** | 33 | 65 | **+32** |

### Interpretazione

- ✅ Il **Master** contiene solo le strutture dei **progetti PNRR validati/in corso**
- ✅ L'**Attuale** include anche strutture **non-PNRR** (aggiuntive, funzionanti)
- ⚠️ **14 CDC hanno PNRR mismatch** (Master=NO, Attuale=SI)

---

## ❌ PROBLEMA CRITICO: Mismatch PNRR

Le seguenti **14 CDC** sono marcate come **PNRR=SI** nell'anagrafica attuale,
ma nel Master risultano **VALIDATA=NO**:

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

### Impatto

Queste strutture vengono **erroneamente conteggiate** nei fabbisogni PNRR:
- Costi gonfiati per dotazioni PNRR
- Report direzione con dati errati
- Dashboard mostra priorità sbagliate

---

## ✅ SOLUZIONI

### Opzione A: Correzione Automatica (CONSIGLIATA)

Usare lo script `correggi_pnrr_da_master.py` che:
1. Legge il Master
2. Aggiorna solo i campi PNRR nell'anagrafica attuale
3. **NON tocca** strutture non presenti nel Master (restano come sono)
4. Crea backup automatico

```bash
python correggi_pnrr_da_master.py
```

### Opzione B: Verifica Manuale

Controllare una per una le 14 strutture con il team per confermare se:
- Sono effettivamente progetti PNRR validati
- Il Master è aggiornato
- L'anagrafica attuale è corretta

---

## 📋 Strutture Extra (NON nel Master)

### CDC Extra (28)

Queste strutture sono nell'anagrafica ma non nel Master.
**Ragione**: Sono strutture operative ma **non progetti PNRR**.

Esempi:
- CdC Villafranca in Lunigiana
- CdC Castelnuovo
- CdC Gallicano
- CdC Piazza al Serchio
- CdC Tabarracci
- ... (totale 28)

**Azione**: ✅ **Mantenerle** nell'anagrafica (sono valide)

### ODC Extra (4)

1. OdC BIENTINA Bientina [PNRR: SI]
2. OdC SANTA MARIA MADDALENA DI VOLTERRA [PNRR: SI]
3. OdC OSPEDALE DI COMUNITA PORTOFERRAIO [PNRR: SI]
4. OdC LE PIANE (DETTA VILLETTA) [PNRR: SI]

**Nota**: Questi 4 ODC sono marcati PNRR=SI ma non compaiono nel Master.
Da **verificare** se sono progetti PNRR reali o errori.

---

## 📊 Strutture con Match PNRR Corretto (9 CDC)

Le seguenti 9 CDC hanno PNRR correttamente allineato Master-Attuale:

1. CdC DI MONTIGNOSO [PNRR: SI]
2. CdC CARRARA CENTRO [PNRR: SI]
3. CdC di PIETRASANTA [PNRR: SI]
4. CdC SAN LEONARDO IN TREPONZIO [PNRR: SI]
5. CdC LIVORNO EST [PNRR: SI]
6. CdC SAN GIULIANO TERME [PNRR: SI]
7. CdC POMARANCE [PNRR: SI]
8. CdC PONTEDERA [PNRR: SI]
9. CdC VOLTERRA [PNRR: SI]

---

## 🎯 Piano d'Azione Raccomandato

### Fase 1: Backup ✅
```bash
cp strutture_sanitarie.csv strutture_sanitarie.csv.pre_correzione_pnrr
```

### Fase 2: Correzione Automatica
```bash
python correggi_pnrr_da_master.py
```

Output:
- `strutture_sanitarie_CORRETTE.csv` (nuovo file)
- Report correzioni applicate

### Fase 3: Verifica
```bash
# Confronta prima/dopo
python verifica_correzioni_pnrr.py
```

### Fase 4: Applicazione
```bash
# Se OK
cp strutture_sanitarie_CORRETTE.csv strutture_sanitarie.csv

# Rigenera dati
python integra_anagrafiche_v3.py

# Commit
git add strutture_sanitarie.csv
git commit -m "fix: Corregge PNRR da file master ELENCO PROGETTI"
git push
```

### Fase 5: Aggiorna Dashboard
La dashboard si aggiornerà automaticamente dopo il push.

---

## 📝 Note Tecniche

### Matching Strutture

Lo script usa **fuzzy matching** per associare nomi simili:
- "CdC di PONTREMOLI" ↔ "CdC Pontremoli"
- "CdC SAN LEONARDO IN TREPONZIO" ↔ "CdC S. Leonardo In Treponzio"

### Campi Aggiornati

Solo il campo **PNRR** viene modificato:
- `SI` → `NO` per le 14 strutture in mismatch
- Altri campi restano invariati

### Strutture Mantenute

Tutte le 32 strutture extra restano inalterate nell'anagrafica.

---

## 🆘 Domande Frequenti

**Q: Perché l'attuale ha più strutture del Master?**
A: Il Master contiene solo progetti PNRR, l'attuale include anche strutture operative non-PNRR.

**Q: Possiamo fidarci del Master?**
A: Il Master è l'elenco ufficiale progetti PNRR validati. È la fonte autoritativa.

**Q: Cosa succede alle dotazioni delle 14 strutture?**
A: Le dotazioni restano invariate, cambia solo se vengono conteggiate nei fabbisogni PNRR.

**Q: Serve conferma prima di correggere?**
A: Sì, lo script genera prima un file CORRETTE.csv da verificare prima di applicare.

---

## 📊 Impatto Correzioni

### Prima della Correzione
- Strutture PNRR=SI: 37
- Fabbisogno PNRR stimato: €X (sovrastimato)

### Dopo la Correzione
- Strutture PNRR=SI: 23 (37 - 14)
- Fabbisogno PNRR stimato: €Y (corretto)

**Differenza**: -14 strutture CDC (-37.8%)

---

**Prossimo Step**: Eseguire `python correggi_pnrr_da_master.py`
