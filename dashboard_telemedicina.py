#!/usr/bin/env python3
"""
Dashboard Telemedicina - Dotazioni tecnologiche strutture sanitarie
USL Toscana Nord Ovest - Case di Comunità e Ospedali di Comunità

Visualizza dotazioni tecnologiche per telemedicina con fabbisogno complessivo

Utilizzo:
    streamlit run dashboard_telemedicina.py
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# Configurazione pagina
st.set_page_config(
    page_title="Dashboard Telemedicina - USL TNO",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data(ttl=600, show_spinner="Caricamento dati...")
def carica_dati():
    """Carica tutti i dati necessari (cache: 10 minuti)"""
    try:
        # Carica strutture
        df_strutture = pd.read_csv('strutture_sanitarie.csv')

        # Carica catalogo dotazioni
        df_catalogo = pd.read_csv('dotazioni_telemedicina_catalogo.csv')

        # Carica dotazioni per struttura
        df_dotazioni = pd.read_csv('dotazioni_strutture_telemedicina.csv')

        # Carica dotazioni minime standard
        df_dotazioni_minime = pd.read_csv('dotazioni_minime_standard.csv')

        return df_strutture, df_catalogo, df_dotazioni, df_dotazioni_minime
    except FileNotFoundError as e:
        st.error(f"❌ Errore: File non trovato - {e}")
        st.stop()


def calcola_fabbisogno(df_dotazioni, df_catalogo):
    """Calcola il fabbisogno complessivo per dotazione con distinzione stati finanziamento"""

    # Merge con catalogo per ottenere descrizione e costo
    df_merge = df_dotazioni.merge(
        df_catalogo,
        left_on='Codice_Dotazione',
        right_on='Codice',
        how='left'
    )

    # Calcola quantità da acquistare
    df_merge['Quantita_Da_Acquistare'] = df_merge['Quantita_Richiesta'] - df_merge['Quantita_Presente']
    df_merge['Quantita_Da_Acquistare'] = df_merge['Quantita_Da_Acquistare'].clip(lower=0)

    # Calcola costo per struttura (solo ciò che serve acquistare)
    df_merge['Costo_Totale'] = df_merge['Quantita_Da_Acquistare'] * df_merge['Costo_Unitario_EUR']

    # Calcola costi separati per stato finanziamento
    df_merge['Costo_Da_Finanziare'] = df_merge.apply(
        lambda row: row['Costo_Totale'] if row.get('Stato_Finanziamento') == 'DA_ACQUISTARE' else 0, axis=1
    )
    df_merge['Costo_Gia_Finanziato'] = df_merge.apply(
        lambda row: row['Quantita_Richiesta'] * row['Costo_Unitario_EUR'] if row.get('Stato_Finanziamento') == 'FINANZIATO' else 0, axis=1
    )
    df_merge['Costo_Presente'] = df_merge.apply(
        lambda row: row['Quantita_Presente'] * row['Costo_Unitario_EUR'] if row.get('Stato_Finanziamento') == 'PRESENTE' else 0, axis=1
    )

    return df_merge


def pagina_riepilogo_generale(df_strutture, df_catalogo, df_dotazioni, df_fabbisogno):
    """Pagina riepilogo generale"""
    st.header("📊 Riepilogo Generale")

    # KPI principali - prima riga
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        n_strutture = len(df_strutture)
        st.metric("Strutture Totali", n_strutture)

    with col2:
        n_cdc = len(df_strutture[df_strutture['Tipologia'] == 'CdC'])
        st.metric("Case di Comunità", n_cdc)

    with col3:
        n_odc = len(df_strutture[df_strutture['Tipologia'] == 'OdC'])
        st.metric("Ospedali di Comunità", n_odc)

    with col4:
        fabbisogno_totale = df_fabbisogno['Costo_Totale'].sum()
        st.metric("Fabbisogno Totale", f"€{fabbisogno_totale:,.2f}")

    # KPI PNRR vs non-PNRR - seconda riga
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        n_pnrr = len(df_strutture[df_strutture['PNRR'] == 'SI'])
        st.metric("🎯 Strutture PNRR", n_pnrr, delta=f"{n_pnrr/len(df_strutture)*100:.1f}%")

    with col2:
        n_non_pnrr = len(df_strutture[df_strutture['PNRR'] == 'NO'])
        st.metric("📍 Strutture non-PNRR", n_non_pnrr, delta=f"{n_non_pnrr/len(df_strutture)*100:.1f}%")

    with col3:
        # Merge per ottenere PNRR dalle strutture
        df_fabb_strutt = df_fabbisogno.merge(df_strutture[['Codice', 'PNRR']],
                                              left_on='Codice_Struttura', right_on='Codice', how='left')
        fabb_pnrr = df_fabb_strutt[df_fabb_strutt['PNRR'] == 'SI']['Costo_Totale'].sum()
        st.metric("💰 Fabbisogno PNRR", f"€{fabb_pnrr:,.2f}")

    with col4:
        fabb_non_pnrr = df_fabb_strutt[df_fabb_strutt['PNRR'] == 'NO']['Costo_Totale'].sum()
        st.metric("💰 Fabbisogno non-PNRR", f"€{fabb_non_pnrr:,.2f}")

    # KPI per stato finanziamento - terza riga
    st.markdown("### 💸 Analisi Finanziamento")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        costo_da_finanziare = df_fabbisogno['Costo_Da_Finanziare'].sum()
        st.metric(
            "🔴 DA FINANZIARE",
            f"€{costo_da_finanziare:,.2f}",
            delta="Richiede nuovo finanziamento",
            delta_color="inverse"
        )

    with col2:
        costo_gia_finanziato = df_fabbisogno['Costo_Gia_Finanziato'].sum()
        st.metric(
            "🟢 GIÀ FINANZIATO",
            f"€{costo_gia_finanziato:,.2f}",
            delta="Budget già allocato"
        )

    with col3:
        costo_presente = df_fabbisogno['Costo_Presente'].sum()
        st.metric(
            "🔵 GIÀ PRESENTE",
            f"€{costo_presente:,.2f}",
            delta="Valore esistente"
        )

    with col4:
        # Conteggi per stato
        n_da_acquistare = len(df_fabbisogno[df_fabbisogno['Stato_Finanziamento'] == 'DA_ACQUISTARE'])
        n_finanziato = len(df_fabbisogno[df_fabbisogno['Stato_Finanziamento'] == 'FINANZIATO'])
        n_presente = len(df_fabbisogno[df_fabbisogno['Stato_Finanziamento'] == 'PRESENTE'])
        st.metric(
            "📊 Configurazioni",
            f"{n_da_acquistare} / {n_finanziato} / {n_presente}",
            delta="Da finanz. / Finanz. / Presenti"
        )

    # Alert PNRR se filtrato
    df_fabb_strutt_pnrr = df_fabbisogno.merge(df_strutture[['Codice', 'PNRR']],
                                               left_on='Codice_Struttura', right_on='Codice', how='left')
    costo_da_finanz_pnrr = df_fabb_strutt_pnrr[
        (df_fabb_strutt_pnrr['PNRR'] == 'SI') &
        (df_fabb_strutt_pnrr['Stato_Finanziamento'] == 'DA_ACQUISTARE')
    ]['Costo_Da_Finanziare'].sum()

    if costo_da_finanz_pnrr > 0:
        st.warning(
            f"⚠️ **PRIORITÀ ALTA**: €{costo_da_finanz_pnrr:,.2f} da finanziare per interventi **PNRR** "
            f"(scadenza: **marzo 2026**)"
        )

    st.divider()

    # Fabbisogno per categoria
    st.subheader("💰 Fabbisogno per Categoria")

    fabbisogno_cat = df_fabbisogno.groupby('Categoria').agg({
        'Quantita_Da_Acquistare': 'sum',
        'Costo_Totale': 'sum'
    }).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        # Grafico a torta
        fig_pie = px.pie(
            fabbisogno_cat,
            values='Costo_Totale',
            names='Categoria',
            title='Distribuzione Costi per Categoria',
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Tabella riepilogo
        st.dataframe(
            fabbisogno_cat.style.format({
                'Quantita_Da_Acquistare': '{:.0f}',
                'Costo_Totale': '€{:,.2f}'
            }),
            hide_index=True,
            use_container_width=True
        )

    st.divider()

    # Tutte le dotazioni per costo
    st.subheader("🔝 Dotazioni per Fabbisogno")

    tutte_dotazioni = df_fabbisogno.groupby(['Descrizione', 'Costo_Unitario_EUR']).agg({
        'Quantita_Da_Acquistare': 'sum',
        'Costo_Totale': 'sum'
    }).reset_index()

    # Filtra solo dotazioni con costo > 0 (esclude quelle già complete)
    tutte_dotazioni = tutte_dotazioni[tutte_dotazioni['Costo_Totale'] > 0].sort_values('Costo_Totale', ascending=False)

    # Altezza dinamica in base al numero di dotazioni (min 400px, 40px per dotazione)
    altezza_grafico = max(400, len(tutte_dotazioni) * 40)

    fig_bar = px.bar(
        tutte_dotazioni,
        x='Costo_Totale',
        y='Descrizione',
        orientation='h',
        title=f'Tutte le Dotazioni per Costo Totale ({len(tutte_dotazioni)} dotazioni)',
        labels={'Costo_Totale': 'Costo Totale (€)', 'Descrizione': 'Dotazione'},
        text='Costo_Totale',
        custom_data=['Quantita_Da_Acquistare'],
        height=altezza_grafico
    )
    fig_bar.update_traces(
        texttemplate='%{customdata[0]:.0f} unità - €%{text:,.0f}',
        textposition='outside'
    )
    fig_bar.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(r=200),  # Margine destro più ampio per etichette lunghe
        xaxis=dict(range=[0, tutte_dotazioni['Costo_Totale'].max() * 1.25])  # Estendi asse X del 25%
    )
    st.plotly_chart(fig_bar, use_container_width=True)


def pagina_strutture(df_strutture, df_fabbisogno):
    """Pagina elenco strutture"""
    st.header("🏥 Elenco Strutture")

    # Filtri
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        tipo_filtro = st.multiselect(
            "Tipologia",
            options=df_strutture['Tipologia'].unique(),
            default=df_strutture['Tipologia'].unique()
        )

    with col2:
        # Filtra zone non vuote
        zone_disponibili = sorted([z for z in df_strutture['Zona'].unique() if pd.notna(z) and str(z).strip() != ''])
        if zone_disponibili:
            zona_filtro = st.multiselect(
                "Zona Distretto",
                options=zone_disponibili,
                default=zone_disponibili
            )
        else:
            zona_filtro = []

    with col3:
        # Filtra classificazioni non vuote
        class_disponibili = sorted([c for c in df_strutture['Classificazione'].unique() if pd.notna(c) and str(c).strip() != ''])
        if class_disponibili:
            class_filtro = st.multiselect(
                "Classificazione",
                options=class_disponibili,
                default=class_disponibili
            )
        else:
            class_filtro = None

    with col4:
        # Determina default in base al filtro sidebar già applicato
        valori_pnrr_presenti = df_strutture['PNRR'].unique().tolist()
        pnrr_filtro = st.multiselect(
            "PNRR",
            options=['SI', 'NO'],
            default=valori_pnrr_presenti  # Usa i valori già filtrati dalla sidebar
        )

    # Applica filtri
    df_filtrato = df_strutture[df_strutture['Tipologia'].isin(tipo_filtro)]

    if zona_filtro:
        df_filtrato = df_filtrato[df_filtrato['Zona'].isin(zona_filtro)]

    if class_filtro:
        df_filtrato = df_filtrato[df_filtrato['Classificazione'].isin(class_filtro)]

    # Applica filtro PNRR solo se ci sono entrambi i valori (altrimenti è già filtrato dalla sidebar)
    if set(pnrr_filtro) != set(valori_pnrr_presenti):
        df_filtrato = df_filtrato[df_filtrato['PNRR'].isin(pnrr_filtro)]

    # Calcola fabbisogno per struttura
    fabbisogno_struttura = df_fabbisogno.groupby('Codice_Struttura')['Costo_Totale'].sum().reset_index()
    fabbisogno_struttura.columns = ['Codice', 'Fabbisogno_EUR']

    # Merge con strutture
    df_display = df_filtrato.merge(fabbisogno_struttura, on='Codice', how='left')
    df_display['Fabbisogno_EUR'] = df_display['Fabbisogno_EUR'].fillna(0)

    st.metric("Strutture visualizzate", len(df_display))

    # Tabella strutture - includi nuovi campi
    colonne_da_mostrare = ['Tipologia', 'Nome_Struttura', 'Zona', 'Classificazione', 'Comune', 'PNRR', 'Fabbisogno_EUR']
    st.dataframe(
        df_display[colonne_da_mostrare].style.format({
            'Fabbisogno_EUR': '€{:,.2f}'
        }),
        hide_index=True,
        use_container_width=True,
        height=500
    )

    # Mappa geografica (placeholder - richiede coordinate)
    st.divider()
    st.subheader("📍 Distribuzione Geografica")
    st.info("ℹ️ Per visualizzare la mappa geografica è necessario aggiungere le coordinate GPS alle strutture")


def pagina_dotazioni_struttura(df_strutture, df_catalogo, df_fabbisogno):
    """Pagina dettaglio dotazioni per struttura"""
    st.header("🔍 Dettaglio Dotazioni per Struttura")

    # Selezione struttura
    struttura_selezionata = st.selectbox(
        "Seleziona Struttura",
        options=df_strutture['Codice'],
        format_func=lambda x: df_strutture[df_strutture['Codice'] == x]['Nome_Struttura'].values[0]
    )

    # Info struttura
    info_struttura = df_strutture[df_strutture['Codice'] == struttura_selezionata].iloc[0]

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Tipologia", info_struttura['Tipologia'])
    with col2:
        zona = info_struttura.get('Zona', '')
        if pd.notna(zona) and str(zona).strip():
            st.metric("Zona", zona)
        else:
            st.metric("Zona", "-")
    with col3:
        class_val = info_struttura.get('Classificazione', '')
        if pd.notna(class_val) and str(class_val).strip():
            st.metric("Classificazione", class_val)
        else:
            st.metric("Classificazione", "-")
    with col4:
        st.metric("Comune", info_struttura['Comune'])
    with col5:
        st.metric("PNRR", info_struttura['PNRR'])

    st.divider()

    # Filtra dotazioni per struttura
    df_strutt = df_fabbisogno[df_fabbisogno['Codice_Struttura'] == struttura_selezionata].copy()

    if len(df_strutt) == 0:
        st.warning("⚠️ Nessuna dotazione configurata per questa struttura")
        return

    # Calcola totali
    fabbisogno_totale = df_strutt['Costo_Totale'].sum()
    dotazioni_da_acquistare = (df_strutt['Quantita_Da_Acquistare'] > 0).sum()
    dotazioni_complete = (df_strutt['Quantita_Da_Acquistare'] == 0).sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Fabbisogno Totale", f"€{fabbisogno_totale:,.2f}")
    with col2:
        st.metric("Dotazioni da Acquistare", dotazioni_da_acquistare)
    with col3:
        st.metric("Dotazioni Complete", dotazioni_complete)

    st.divider()

    # Tabelle per categoria
    st.subheader("🔬 Dispositivi Diagnostici")
    df_diag = df_strutt[df_strutt['Categoria'] == 'Dispositivi Diagnostici']

    if len(df_diag) > 0:
        st.dataframe(
            df_diag[['Descrizione', 'Stato_Finanziamento', 'Quantita_Presente', 'Quantita_Richiesta', 'Quantita_Da_Acquistare',
                     'Costo_Unitario_EUR', 'Costo_Totale', 'Note']].style.format({
                'Quantita_Presente': '{:.0f}',
                'Quantita_Richiesta': '{:.0f}',
                'Quantita_Da_Acquistare': '{:.0f}',
                'Costo_Unitario_EUR': '€{:,.2f}',
                'Costo_Totale': '€{:,.2f}'
            }),
            hide_index=True,
            use_container_width=True
        )
        st.metric("Subtotale Dispositivi Diagnostici", f"€{df_diag['Costo_Totale'].sum():,.2f}")
    else:
        st.info("Nessun dispositivo diagnostico configurato")

    st.divider()

    st.subheader("🛏️ Attrezzature Sanitarie")
    df_attr = df_strutt[df_strutt['Categoria'] == 'Attrezzature Sanitarie']

    if len(df_attr) > 0:
        st.dataframe(
            df_attr[['Descrizione', 'Stato_Finanziamento', 'Quantita_Presente', 'Quantita_Richiesta', 'Quantita_Da_Acquistare',
                     'Costo_Unitario_EUR', 'Costo_Totale', 'Note']].style.format({
                'Quantita_Presente': '{:.0f}',
                'Quantita_Richiesta': '{:.0f}',
                'Quantita_Da_Acquistare': '{:.0f}',
                'Costo_Unitario_EUR': '€{:,.2f}',
                'Costo_Totale': '€{:,.2f}'
            }),
            hide_index=True,
            use_container_width=True
        )
        st.metric("Subtotale Attrezzature Sanitarie", f"€{df_attr['Costo_Totale'].sum():,.2f}")
    else:
        st.info("Nessuna attrezzatura sanitaria configurata")


def pagina_fabbisogno_complessivo(df_fabbisogno, df_strutture):
    """Pagina fabbisogno complessivo dettagliato"""
    st.header("💰 Fabbisogno Complessivo")

    # Fabbisogno per dotazione
    st.subheader("Riepilogo per Dotazione")

    fabbisogno_dot = df_fabbisogno.groupby(['Categoria', 'Descrizione', 'Costo_Unitario_EUR']).agg({
        'Quantita_Da_Acquistare': 'sum',
        'Costo_Totale': 'sum'
    }).reset_index().sort_values(['Categoria', 'Costo_Totale'], ascending=[True, False])

    # Visualizza per categoria
    for categoria in fabbisogno_dot['Categoria'].unique():
        with st.expander(f"**{categoria}**", expanded=True):
            df_cat = fabbisogno_dot[fabbisogno_dot['Categoria'] == categoria]

            st.dataframe(
                df_cat[['Descrizione', 'Quantita_Da_Acquistare', 'Costo_Unitario_EUR', 'Costo_Totale']].style.format({
                    'Quantita_Da_Acquistare': '{:.0f}',
                    'Costo_Unitario_EUR': '€{:,.2f}',
                    'Costo_Totale': '€{:,.2f}'
                }),
                hide_index=True,
                use_container_width=True
            )

            st.metric(f"Totale {categoria}", f"€{df_cat['Costo_Totale'].sum():,.2f}")

    st.divider()

    # Fabbisogno per struttura
    st.subheader("Fabbisogno per Struttura")

    fabbisogno_strutt = df_fabbisogno.groupby('Codice_Struttura')['Costo_Totale'].sum().reset_index()
    fabbisogno_strutt.columns = ['Codice', 'Fabbisogno_EUR']

    # Merge con info strutture
    df_merge = fabbisogno_strutt.merge(
        df_strutture[['Codice', 'Tipologia', 'Nome_Struttura', 'Comune', 'Provincia']],
        on='Codice',
        how='left'
    ).sort_values('Fabbisogno_EUR', ascending=False)

    # Top 10 strutture
    st.subheader("Top 10 Strutture per Fabbisogno")
    top10 = df_merge.head(10)

    fig_top10 = px.bar(
        top10,
        x='Fabbisogno_EUR',
        y='Nome_Struttura',
        orientation='h',
        color='Tipologia',
        title='Top 10 Strutture per Fabbisogno',
        labels={'Fabbisogno_EUR': 'Fabbisogno (€)', 'Nome_Struttura': 'Struttura'},
        text='Fabbisogno_EUR'
    )
    fig_top10.update_traces(texttemplate='€%{text:,.0f}', textposition='outside')
    fig_top10.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_top10, use_container_width=True)

    # Tabella completa
    st.subheader("Elenco Completo")
    st.dataframe(
        df_merge[['Tipologia', 'Nome_Struttura', 'Comune', 'Provincia', 'Fabbisogno_EUR']].style.format({
            'Fabbisogno_EUR': '€{:,.2f}'
        }),
        hide_index=True,
        use_container_width=True,
        height=400
    )

    # Totale generale
    totale_generale = df_merge['Fabbisogno_EUR'].sum()
    st.success(f"### 💰 FABBISOGNO TOTALE COMPLESSIVO: €{totale_generale:,.2f}")


def pagina_standard_conformita(df_strutture, df_catalogo, df_dotazioni, df_dotazioni_minime):
    """Pagina Standard e Conformità - Verifica dotazioni minime"""
    st.header("⭐ Standard e Conformità DM 77/2022")

    st.info("📋 Questa pagina mostra le **dotazioni minime obbligatorie** per CDC e ODC secondo le linee guida nazionali")

    # Tabs per CDC e ODC
    tab_cdc, tab_odc, tab_comuni = st.tabs(["🏥 CDC - Case di Comunità", "🏥 ODC - Ospedali di Comunità", "🔧 Dotazioni Comuni"])

    with tab_cdc:
        st.subheader("Dotazioni Minime per Case di Comunità (CDC)")

        # Filtra dotazioni minime CDC
        dotazioni_cdc = df_dotazioni_minime[df_dotazioni_minime['Tipologia'] == 'CDC']

        # Mostra tabella dotazioni minime
        st.markdown("### 📌 Dotazioni Obbligatorie")
        st.dataframe(
            dotazioni_cdc[['Dispositivo', 'Quantita_Minima', 'Note']],
            hide_index=True,
            use_container_width=True
        )

        # Analisi conformità
        st.markdown("### ✅ Analisi Conformità")

        # Conta quante strutture CDC hanno ogni dotazione
        strutture_cdc = df_strutture[df_strutture['Tipologia'] == 'CdC']
        n_cdc = len(strutture_cdc)

        st.metric("Totale Case di Comunità", n_cdc)

        # Info box
        st.info(f"📊 Ogni CDC deve avere **{len(dotazioni_cdc)}** dotazioni diagnostiche minime obbligatorie")

    with tab_odc:
        st.subheader("Dotazioni Minime per Ospedali di Comunità (ODC)")

        # Filtra dotazioni minime ODC
        dotazioni_odc = df_dotazioni_minime[df_dotazioni_minime['Tipologia'] == 'ODC']

        # Mostra tabella dotazioni minime
        st.markdown("### 📌 Dotazioni Obbligatorie")
        st.dataframe(
            dotazioni_odc[['Dispositivo', 'Quantita_Minima', 'Note']],
            hide_index=True,
            use_container_width=True
        )

        # Analisi conformità
        st.markdown("### ✅ Analisi Conformità")

        # Conta quante strutture ODC ci sono
        strutture_odc = df_strutture[df_strutture['Tipologia'] == 'OdC']
        n_odc = len(strutture_odc)

        st.metric("Totale Ospedali di Comunità", n_odc)

        # Info box
        st.info(f"📊 Ogni ODC deve avere **{len(dotazioni_odc)}** dotazioni diagnostiche minime obbligatorie")

    with tab_comuni:
        st.subheader("Dotazioni Comuni a CDC e ODC")

        # Filtra dotazioni comuni
        dotazioni_comuni = df_dotazioni_minime[df_dotazioni_minime['Tipologia'] == 'COMUNE']

        # Mostra tabella dotazioni comuni
        st.markdown("### 📌 Attrezzature Sanitarie Standard")
        st.dataframe(
            dotazioni_comuni[['Dispositivo', 'Quantita_Minima', 'Note']],
            hide_index=True,
            use_container_width=True
        )

        st.info(f"🔧 Sia CDC che ODC devono avere **{len(dotazioni_comuni)}** attrezzature sanitarie standard")

    # Sezione normativa
    st.divider()
    st.markdown("### 📜 Riferimenti Normativi")
    st.markdown("""
    Le dotazioni minime sono definite dal **DM 77/2022** - Decreto Ministeriale 23 maggio 2022, n. 77:
    - **Regolamento recante la definizione di modelli e standard per lo sviluppo dell'assistenza territoriale**
    - Pubblicato in G.U. Serie Generale n. 144 del 22-06-2022
    - Allegati tecnici con specifiche dotazioni per CDC e ODC

    🔗 [Maggiori informazioni sul sito del Ministero della Salute](https://www.salute.gov.it/)
    """)


def main():
    """Funzione principale"""

    # Titolo
    st.title("🏥 Dashboard Telemedicina")
    st.subheader("Dotazioni Tecnologiche - USL Toscana Nord Ovest")

    # Carica dati
    with st.spinner("Caricamento dati in corso..."):
        df_strutture_orig, df_catalogo, df_dotazioni_orig, df_dotazioni_minime = carica_dati()

    # Sidebar navigazione
    st.sidebar.title("Navigazione")
    pagina = st.sidebar.radio(
        "Seleziona una vista",
        ["Riepilogo Generale", "Elenco Strutture", "Dettaglio Dotazioni Struttura", "Fabbisogno Complessivo", "⭐ Standard e Conformità"]
    )

    st.sidebar.divider()

    # Filtro PNRR
    st.sidebar.subheader("🎯 Filtro PNRR")
    filtro_pnrr = st.sidebar.radio(
        "Interventi da visualizzare",
        ["TUTTI", "Solo PNRR", "Solo non-PNRR"],
        index=0,
        help="Filtra per interventi PNRR (scadenza marzo 2026) o non-PNRR"
    )

    # Applica filtro PNRR
    if filtro_pnrr == "Solo PNRR":
        df_strutture = df_strutture_orig[df_strutture_orig['PNRR'] == 'SI'].copy()
        codici_strutture = df_strutture['Codice'].unique()
        df_dotazioni = df_dotazioni_orig[df_dotazioni_orig['Codice_Struttura'].isin(codici_strutture)].copy()
        st.sidebar.info("🎯 Visualizzando solo interventi **PNRR** (scadenza marzo 2026)")
    elif filtro_pnrr == "Solo non-PNRR":
        df_strutture = df_strutture_orig[df_strutture_orig['PNRR'] == 'NO'].copy()
        codici_strutture = df_strutture['Codice'].unique()
        df_dotazioni = df_dotazioni_orig[df_dotazioni_orig['Codice_Struttura'].isin(codici_strutture)].copy()
        st.sidebar.info("📍 Visualizzando solo interventi **non-PNRR**")
    else:
        df_strutture = df_strutture_orig.copy()
        df_dotazioni = df_dotazioni_orig.copy()

    # Calcola fabbisogno con dati filtrati
    df_fabbisogno = calcola_fabbisogno(df_dotazioni, df_catalogo)

    st.sidebar.divider()

    # Pulsante refresh cache
    if st.sidebar.button("🔄 Aggiorna Dati", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.sidebar.caption("💡 Usa questo pulsante per ricaricare i dati aggiornati")

    st.sidebar.divider()

    # Info dataset
    st.sidebar.subheader("📊 Info Dataset")
    st.sidebar.metric("Strutture", len(df_strutture))
    st.sidebar.metric("Dotazioni Catalogo", len(df_catalogo))
    st.sidebar.metric("Configurazioni", len(df_dotazioni))

    st.sidebar.divider()

    # Popup dotazioni minime
    with st.sidebar.expander("📋 Dotazioni Minime Standard", expanded=False):
        st.markdown("### 🏥 Case di Comunità (CDC)")
        st.markdown("""
        **Dispositivi Diagnostici:**
        - ECG (Elettrocardiografo)
        - Holter cardiaco
        - Spirometro
        - Ecografo portatile
        - Monitor multiparametrico
        """)

        st.markdown("### 🏥 Ospedali di Comunità (ODC)")
        st.markdown("""
        **Dispositivi Diagnostici:**
        - Defibrillatore/DAE
        - Apparecchio radiologico
        - Emogasanalizzatore
        - POC (Point of Care)
        - Carrello emergenza
        - ECG portatile
        - Spirometro
        - Ecografo
        - Telemedicina (STANZA)
        """)

        st.markdown("### 🛏️ Attrezzature Sanitarie (CDC/ODC)")
        st.markdown("""
        **Comuni a tutte le strutture:**
        - Lettino visita elettrico
        - Lettino ginecologico
        - Letto degenza elettrico
        - DAE con aspiratore
        - Lampada visita
        - Frigofarmaco
        - Lavapadelle
        - Vuotatorio
        - Sollevatore/Sollevapazienti
        - Riunito oculistico completo
        """)

    # Routing pagine
    if pagina == "Riepilogo Generale":
        pagina_riepilogo_generale(df_strutture, df_catalogo, df_dotazioni, df_fabbisogno)
    elif pagina == "Elenco Strutture":
        pagina_strutture(df_strutture, df_fabbisogno)
    elif pagina == "Dettaglio Dotazioni Struttura":
        pagina_dotazioni_struttura(df_strutture, df_catalogo, df_fabbisogno)
    elif pagina == "Fabbisogno Complessivo":
        pagina_fabbisogno_complessivo(df_fabbisogno, df_strutture)
    elif pagina == "⭐ Standard e Conformità":
        pagina_standard_conformita(df_strutture, df_catalogo, df_dotazioni, df_dotazioni_minime)


if __name__ == "__main__":
    main()
