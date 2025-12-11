# Log Integrazione Stima Arredi PNRR

**Data**: 11 Dicembre 2024
**Fonte**: File "Stima arredi PNRR.xlsx" (fogli OdC e CdC)

## Riepilogo Operazione

È stata effettuata l'integrazione delle tecnologie dal file condiviso "Stima arredi PNRR" nelle dotazioni esistenti.

### File Elaborati

- `Stima arredi PNRR.xlsx - OdC.csv` (7 strutture ODC)
- `Stima arredi PNRR.xlsx - CdC.csv` (26 strutture CDC)

### Dati Estratti

**Totale voci tecnologie**: 56
**Strutture coinvolte**: 22
**Tipologie attrezzature**: 12

## Mappatura Strutture

Le strutture nel file Stima Arredi usano nomi semplificati. Mappatura applicata:

| Nome file Arredi | Nome registro | Codice |
|------------------|---------------|---------|
| OdC Campo Marte | OdC CAMPO DI MARTE Lucca | ODC007 |
| OdC Cecina | OdC OSPEDALE DI COMUNITA CECINA Cecina | ODC008 |
| OdC Piombino | OdC OSPEDALE DI COMUNITA PIOMBINO Piombino | ODC009 |
| OdC Livorno | OdC PADIGLIONE 5 Livorno | ODC006 |
| OdC Viareggio | OdC TABARRACCI | ODC012 |

## Mappatura Attrezzature

| Descrizione file Arredi | Codice Catalogo | Descrizione Catalogo |
|-------------------------|-----------------|----------------------|
| Letto elettrico degenza (LINET) | ATTR002 | Letto degenza elettrico |
| ECG | DIAG001 | ECG (con trasmissione tracciati) |
| LAMPADA VISITA SU STATIVO | ATTR003 | Lampada visita |
| FRIGORIFERO | ATTR006 | Frigofarmaco |
| DAE+ ASPIRATORE PER CARRELLO EMERGENZA | EMER002 | DAE con aspiratore |
| Lavapadelle (ARJO) | ATTR004 | Lavapadelle |
| Vuotatoio (ARJO) | ATTR005 | Vuotatorio |
| Sollevatore (ARJO) | ATTR007 | Sollevatore |
| LETTINO VISITA ELETTRICO | ATTR001 | Lettino visita elettrico |
| Lettino visita di tipo ginecologico (FAVERO) | GINEC001 | Lettino ginecologico |
| ECOGRAFO | DIAG004 | Ecografo portatile |
| spirometro da mettere in rete | DIAG003 | Spirometro |

## Risultati Integrazione

### Dotazioni Aggiornate

- **Aggiornamenti**: 9 dotazioni esistenti (quantità incrementate)
- **Nuove aggiunte**: 27 nuove configurazioni dotazioni
- **Totale dopo integrazione**: 343 dotazioni (era 316)

### Dispositivi Aggiunti

**Quantità totale**: 95 dispositivi

Distribuzione per tipologia:
- Lettini visita elettrici: 278 unità
- Letti degenza elettrici: 93 unità
- Lettini ginecologici: 13 unità
- Frigofarmaci: 11 unità
- Lavapadelle: 5 unità
- Lampade visita: 7 unità
- DAE con aspiratore: 6 unità
- ECG: 4 unità
- Sollevatori: 4 unità
- Vuotatoi: 4 unità
- Ecografi: 1 unità
- Spirometri: 1 unità

### Costi Stimati Tecnologie Arredi

**Totale**: €562.795,28

Principali voci:
- Lettini visita: €235.744,00
- Letti degenza: €160.251,09
- Frigofarmaci: €33.000,00
- Ecografi: €30.000,00
- Lavapadelle: €25.241,70
- Lettini ginecologici: €22.965,93

## Script Utilizzati

1. **`importa_arredi_pnrr.py`**: Estrae tecnologie dai file CSV Stima Arredi
2. **`integra_tecnologie_arredi.py`**: Mappa e integra nelle dotazioni esistenti
3. **`integra_anagrafiche_v3.py`**: Rigenera dati completi

## Note

- L'anagrafica strutture **NON è stata modificata** (come richiesto)
- Le tecnologie estratte sono solo dalla sezione "Tipologia Attrezzatura da acquistare" in fondo ai file
- Gli arredi (sezioni precedenti) sono stati **ignorati** come richiesto
- Tutte le nuove dotazioni sono marcate come `DA_ACQUISTARE`
- Le note indicano "Da Stima Arredi PNRR" per tracciabilità

## Backup Creati

- `dotazioni_strutture_telemedicina.csv.bak` - backup automatico script
- `dotazioni_strutture_telemedicina.csv.pre_arredi` - backup pre-integrazione

## Prossimi Aggiornamenti

Questo file "Stima arredi PNRR" è un file condiviso dove verranno caricati aggiornamenti futuri. Per integrare nuovi aggiornamenti:

1. Scaricare file aggiornato da Google Drive
2. Esportare fogli OdC e CdC come CSV
3. Eseguire `python importa_arredi_pnrr.py`
4. Eseguire `python integra_tecnologie_arredi.py`
5. Verificare output e applicare
6. Eseguire `python integra_anagrafiche_v3.py`
7. Commit e push
