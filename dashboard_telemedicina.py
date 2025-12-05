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


@st.cache_data
def carica_dati():
    """Carica tutti i dati necessari"""
    try:
        # Carica strutture
        df_strutture = pd.read_csv('strutture_sanitarie.csv')

        # Carica catalogo dotazioni
        df_catalogo = pd.read_csv('dotazioni_telemedicina_catalogo.csv')

        # Carica dotazioni per struttura
        df_dotazioni = pd.read_csv('dotazioni_strutture_telemedicina.csv')

        return df_strutture, df_catalogo, df_dotazioni
    except FileNotFoundError as e:
        st.error(f"❌ Errore: File non trovato - {e}")
        st.stop()


def calcola_fabbisogno(df_dotazioni, df_catalogo):
    """Calcola il fabbisogno complessivo per dotazione"""

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

    # Calcola costo per struttura
    df_merge['Costo_Totale'] = df_merge['Quantita_Da_Acquistare'] * df_merge['Costo_Unitario_EUR']

    return df_merge


def pagina_riepilogo_generale(df_strutture, df_catalogo, df_dotazioni, df_fabbisogno):
    """Pagina riepilogo generale"""
    st.header("📊 Riepilogo Generale")

    # KPI principali
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

    # Top 10 dotazioni per costo
    st.subheader("🔝 Top 10 Dotazioni per Fabbisogno")

    top_dotazioni = df_fabbisogno.groupby(['Descrizione', 'Costo_Unitario_EUR']).agg({
        'Quantita_Da_Acquistare': 'sum',
        'Costo_Totale': 'sum'
    }).reset_index().sort_values('Costo_Totale', ascending=False).head(10)

    fig_bar = px.bar(
        top_dotazioni,
        x='Costo_Totale',
        y='Descrizione',
        orientation='h',
        title='Top 10 Dotazioni per Costo Totale',
        labels={'Costo_Totale': 'Costo Totale (€)', 'Descrizione': 'Dotazione'},
        text='Costo_Totale'
    )
    fig_bar.update_traces(texttemplate='€%{text:,.0f}', textposition='outside')
    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)


def pagina_strutture(df_strutture, df_fabbisogno):
    """Pagina elenco strutture"""
    st.header("🏥 Elenco Strutture")

    # Filtri
    col1, col2, col3 = st.columns(3)

    with col1:
        tipo_filtro = st.multiselect(
            "Tipologia",
            options=df_strutture['Tipologia'].unique(),
            default=df_strutture['Tipologia'].unique()
        )

    with col2:
        provincia_filtro = st.multiselect(
            "Provincia",
            options=sorted(df_strutture['Provincia'].unique()),
            default=sorted(df_strutture['Provincia'].unique())
        )

    with col3:
        pnrr_filtro = st.multiselect(
            "PNRR",
            options=['SI', 'NO'],
            default=['SI', 'NO']
        )

    # Applica filtri
    df_filtrato = df_strutture[
        (df_strutture['Tipologia'].isin(tipo_filtro)) &
        (df_strutture['Provincia'].isin(provincia_filtro)) &
        (df_strutture['PNRR'].isin(pnrr_filtro))
    ]

    # Calcola fabbisogno per struttura
    fabbisogno_struttura = df_fabbisogno.groupby('Codice_Struttura')['Costo_Totale'].sum().reset_index()
    fabbisogno_struttura.columns = ['Codice', 'Fabbisogno_EUR']

    # Merge con strutture
    df_display = df_filtrato.merge(fabbisogno_struttura, on='Codice', how='left')
    df_display['Fabbisogno_EUR'] = df_display['Fabbisogno_EUR'].fillna(0)

    st.metric("Strutture visualizzate", len(df_display))

    # Tabella strutture
    st.dataframe(
        df_display[['Tipologia', 'Nome_Struttura', 'Comune', 'Provincia', 'PNRR', 'Fabbisogno_EUR']].style.format({
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

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tipologia", info_struttura['Tipologia'])
    with col2:
        st.metric("Comune", info_struttura['Comune'])
    with col3:
        st.metric("Provincia", info_struttura['Provincia'])
    with col4:
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
            df_diag[['Descrizione', 'Quantita_Presente', 'Quantita_Richiesta', 'Quantita_Da_Acquistare',
                     'Costo_Unitario_EUR', 'Costo_Totale', 'Note']].style.format({
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
            df_attr[['Descrizione', 'Quantita_Presente', 'Quantita_Richiesta', 'Quantita_Da_Acquistare',
                     'Costo_Unitario_EUR', 'Costo_Totale', 'Note']].style.format({
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


def main():
    """Funzione principale"""

    # Titolo
    st.title("🏥 Dashboard Telemedicina")
    st.subheader("Dotazioni Tecnologiche - USL Toscana Nord Ovest")

    # Carica dati
    with st.spinner("Caricamento dati in corso..."):
        df_strutture, df_catalogo, df_dotazioni = carica_dati()
        df_fabbisogno = calcola_fabbisogno(df_dotazioni, df_catalogo)

    # Sidebar navigazione
    st.sidebar.title("Navigazione")
    pagina = st.sidebar.radio(
        "Seleziona una vista",
        ["Riepilogo Generale", "Elenco Strutture", "Dettaglio Dotazioni Struttura", "Fabbisogno Complessivo"]
    )

    st.sidebar.divider()

    # Info dataset
    st.sidebar.subheader("📊 Info Dataset")
    st.sidebar.metric("Strutture", len(df_strutture))
    st.sidebar.metric("Dotazioni Catalogo", len(df_catalogo))
    st.sidebar.metric("Configurazioni", len(df_dotazioni))

    # Routing pagine
    if pagina == "Riepilogo Generale":
        pagina_riepilogo_generale(df_strutture, df_catalogo, df_dotazioni, df_fabbisogno)
    elif pagina == "Elenco Strutture":
        pagina_strutture(df_strutture, df_fabbisogno)
    elif pagina == "Dettaglio Dotazioni Struttura":
        pagina_dotazioni_struttura(df_strutture, df_catalogo, df_fabbisogno)
    elif pagina == "Fabbisogno Complessivo":
        pagina_fabbisogno_complessivo(df_fabbisogno, df_strutture)


if __name__ == "__main__":
    main()
