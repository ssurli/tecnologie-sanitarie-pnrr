#!/usr/bin/env python3
"""
Script per generare report HTML interattivo per la direzione
Report user-friendly con grafici, navigazione e design professionale

Utilizzo:
    python genera_report_html.py

Output:
    report_direzione_telemedicina_YYYYMMDD.html
"""

import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def genera_html_report():
    """Genera report HTML completo"""

    print("=" * 80)
    print("GENERAZIONE REPORT HTML - TELEMEDICINA USL TOSCANA NORD OVEST")
    print("=" * 80)
    print()

    # Carica dati
    print("📊 Caricamento dati...")
    df_strutture = pd.read_csv('strutture_sanitarie.csv')
    df_catalogo = pd.read_csv('dotazioni_telemedicina_catalogo.csv')
    df_dotazioni = pd.read_csv('dotazioni_strutture_telemedicina.csv')

    # Merge
    df_merge = df_dotazioni.merge(
        df_catalogo,
        left_on='Codice_Dotazione',
        right_on='Codice',
        how='left'
    )

    df_merge['Quantita_Da_Acquistare'] = df_merge['Quantita_Richiesta'] - df_merge['Quantita_Presente']
    df_merge['Quantita_Da_Acquistare'] = df_merge['Quantita_Da_Acquistare'].clip(lower=0)
    df_merge['Costo_Totale'] = df_merge['Quantita_Da_Acquistare'] * df_merge['Costo_Unitario_EUR']

    df_merge = df_merge.merge(
        df_strutture[['Codice', 'Nome_Struttura', 'Tipologia', 'Zona', 'PNRR']],
        left_on='Codice_Struttura',
        right_on='Codice',
        how='left',
        suffixes=('', '_Strutt')
    )

    # Calcoli
    n_strutture = len(df_strutture)
    n_cdc = len(df_strutture[df_strutture['Tipologia'] == 'CdC'])
    n_odc = len(df_strutture[df_strutture['Tipologia'] == 'OdC'])
    n_pnrr = len(df_strutture[df_strutture['PNRR'] == 'SI'])
    n_non_pnrr = len(df_strutture[df_strutture['PNRR'] == 'NO'])

    df_da_acq = df_merge[df_merge['Stato_Finanziamento'] == 'DA_ACQUISTARE']
    df_finanz = df_merge[df_merge['Stato_Finanziamento'] == 'FINANZIATO']
    df_presente = df_merge[df_merge['Stato_Finanziamento'] == 'PRESENTE']

    costo_da_acq_pnrr = df_da_acq[df_da_acq['PNRR'] == 'SI']['Costo_Totale'].sum()
    costo_da_acq_no = df_da_acq[df_da_acq['PNRR'] == 'NO']['Costo_Totale'].sum()
    costo_finanz = (df_finanz['Quantita_Richiesta'] * df_finanz['Costo_Unitario_EUR']).sum()
    costo_presente = (df_presente['Quantita_Presente'] * df_presente['Costo_Unitario_EUR']).sum()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"report_direzione_telemedicina_{timestamp}.html"

    print(f"📝 Generazione grafici...")

    # GRAFICO 1: Torta finanziamento
    fig_pie = go.Figure(data=[go.Pie(
        labels=['DA FINANZIARE<br>(PNRR)', 'DA FINANZIARE<br>(non-PNRR)', 'GIÀ FINANZIATO', 'GIÀ PRESENTE'],
        values=[costo_da_acq_pnrr, costo_da_acq_no, costo_finanz, costo_presente],
        hole=0.4,
        marker=dict(colors=['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']),
        textinfo='label+percent+value',
        texttemplate='%{label}<br>€%{value:,.0f}<br>(%{percent})',
        hovertemplate='%{label}<br>€%{value:,.0f}<br>%{percent}<extra></extra>'
    )])
    fig_pie.update_layout(
        title="Distribuzione Finanziamento",
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )

    # GRAFICO 2: Bar chart fabbisogno per dotazione
    df_fabb_dot = df_da_acq.groupby('Descrizione').agg({
        'Quantita_Da_Acquistare': 'sum',
        'Costo_Totale': 'sum'
    }).reset_index().sort_values('Costo_Totale', ascending=False).head(10).iloc[::-1]  # Inverto per avere valori alti in alto

    # Uso go.Bar per controllo completo sull'ordine
    fig_bar = go.Figure(go.Bar(
        x=df_fabb_dot['Costo_Totale'],
        y=df_fabb_dot['Descrizione'],
        orientation='h',
        text=[f'€{val:,.0f}'.replace(',', '.') for val in df_fabb_dot['Costo_Totale']],  # Punto come separatore migliaia
        textposition='outside',
        marker=dict(color='#1f77b4'),
        cliponaxis=False  # Permette ai testi di uscire dall'area del grafico
    ))
    fig_bar.update_layout(
        title='Top 10 Dotazioni per Costo Totale',
        xaxis_title='Costo Totale (€)',
        yaxis_title='Dotazione',
        height=500,
        showlegend=False,
        xaxis=dict(
            tickformat=',.0f',  # Formato con migliaia
            automargin=True  # Margine automatico per i testi esterni
        ),
        margin=dict(r=100)  # Margine destro per valori esterni
    )

    # Genera HTML
    print(f"📝 Generazione HTML: {filename}")

    html_content = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report Direzione - Telemedicina USL Toscana Nord Ovest</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .header p {{
            font-size: 1.2em;
            opacity: 0.95;
        }}

        .alert-banner {{
            background: linear-gradient(90deg, #d62728 0%, #ff6b6b 100%);
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 1.3em;
            font-weight: bold;
            border-bottom: 4px solid #a00;
        }}

        .alert-banner .deadline {{
            font-size: 1.5em;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}

        .nav {{
            background: #f8f9fa;
            padding: 15px;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            border-bottom: 2px solid #dee2e6;
            position: sticky;
            top: 0;
            z-index: 1000;
        }}

        .nav a {{
            text-decoration: none;
            color: #495057;
            padding: 10px 20px;
            border-radius: 25px;
            background: white;
            border: 2px solid #dee2e6;
            transition: all 0.3s;
            font-weight: 500;
        }}

        .nav a:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 50px;
            scroll-margin-top: 70px;
        }}

        .section h2 {{
            font-size: 2em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}

        .kpi-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}

        .kpi-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }}

        .kpi-card.red {{
            background: linear-gradient(135deg, #d62728 0%, #ff6b6b 100%);
        }}

        .kpi-card.green {{
            background: linear-gradient(135deg, #2ca02c 0%, #4caf50 100%);
        }}

        .kpi-card.blue {{
            background: linear-gradient(135deg, #1f77b4 0%, #42a5f5 100%);
        }}

        .kpi-label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .kpi-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .kpi-note {{
            font-size: 0.85em;
            opacity: 0.85;
        }}

        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            margin: 20px 0;
        }}

        .info-box {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}

        .info-box.warning {{
            background: #fff3e0;
            border-left-color: #ff9800;
        }}

        .info-box.success {{
            background: #e8f5e9;
            border-left-color: #4caf50;
        }}

        .info-box h3 {{
            margin-bottom: 10px;
            color: #1976d2;
        }}

        .info-box.warning h3 {{
            color: #f57c00;
        }}

        .info-box.success h3 {{
            color: #388e3c;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }}

        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #f0f0f0;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #6c757d;
            border-top: 2px solid #dee2e6;
        }}

        @media print {{
            body {{
                background: white;
            }}
            .nav {{
                display: none;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🏥 Report Direzione Telemedicina</h1>
            <p>USL Toscana Nord Ovest - Dotazioni Tecnologiche CDC/ODC</p>
            <p style="font-size: 0.9em; opacity: 0.8; margin-top: 10px;">Generato il {datetime.now().strftime("%d/%m/%Y alle %H:%M")}</p>
        </div>

        <!-- Alert Banner -->
        <div class="alert-banner">
            ⚠️ ATTENZIONE: Scadenza PNRR <span class="deadline">MARZO 2026</span> - €{costo_da_acq_pnrr:,.2f} da rendicontare
        </div>

        <!-- Navigation -->
        <div class="nav">
            <a href="#executive">Executive Summary</a>
            <a href="#finanziamento">Analisi Finanziamento</a>
            <a href="#dotazioni">Dotazioni</a>
        </div>

        <!-- Content -->
        <div class="content">
            <!-- Executive Summary -->
            <div id="executive" class="section">
                <h2>📊 Executive Summary</h2>

                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-label">Strutture Totali</div>
                        <div class="kpi-value">{n_strutture}</div>
                        <div class="kpi-note">{n_cdc} CDC + {n_odc} ODC</div>
                    </div>

                    <div class="kpi-card red">
                        <div class="kpi-label">Fabbisogno Totale</div>
                        <div class="kpi-value">€{costo_da_acq_pnrr + costo_da_acq_no:,.0f}</div>
                        <div class="kpi-note">Nuovo finanziamento richiesto</div>
                    </div>

                    <div class="kpi-card red">
                        <div class="kpi-label">🎯 PNRR (Priorità)</div>
                        <div class="kpi-value">€{costo_da_acq_pnrr:,.0f}</div>
                        <div class="kpi-note">Scadenza: Marzo 2026</div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-label">Non-PNRR</div>
                        <div class="kpi-value">€{costo_da_acq_no:,.0f}</div>
                        <div class="kpi-note">Programmabile nel tempo</div>
                    </div>

                    <div class="kpi-card green">
                        <div class="kpi-label">Già Finanziato</div>
                        <div class="kpi-value">€{costo_finanz:,.0f}</div>
                        <div class="kpi-note">Budget allocato</div>
                    </div>

                    <div class="kpi-card blue">
                        <div class="kpi-label">Già Presente</div>
                        <div class="kpi-value">€{costo_presente:,.0f}</div>
                        <div class="kpi-note">Valore esistente</div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-label">Strutture PNRR</div>
                        <div class="kpi-value">{n_pnrr}</div>
                        <div class="kpi-note">{n_pnrr/n_strutture*100:.1f}% del totale</div>
                    </div>
                </div>
            </div>

            <!-- Analisi Finanziamento -->
            <div id="finanziamento" class="section">
                <h2>💸 Analisi Finanziamento</h2>

                <div class="info-box warning">
                    <h3>📌 Punti Chiave</h3>
                    <ul style="margin-left: 20px; line-height: 1.8;">
                        <li><strong>€{costo_da_acq_pnrr + costo_da_acq_no:,.2f}</strong> di investimento necessario per completare la rete</li>
                        <li>Il <strong>{costo_da_acq_pnrr/(costo_da_acq_pnrr + costo_da_acq_no)*100:.1f}%</strong> sono fondi PNRR con scadenza obbligatoria</li>
                        <li>La rete ha già <strong>€{costo_presente:,.2f}</strong> di dotazioni operative</li>
                    </ul>
                </div>

                <div class="chart-container">
                    {fig_pie.to_html(include_plotlyjs=False, div_id="pie")}
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>Categoria</th>
                            <th>Importo</th>
                            <th>Percentuale</th>
                            <th>Note</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="background: #ffebee;">
                            <td><strong>🔴 DA FINANZIARE</strong></td>
                            <td><strong>€{costo_da_acq_pnrr + costo_da_acq_no:,.2f}</strong></td>
                            <td><strong>{(costo_da_acq_pnrr + costo_da_acq_no)/(costo_da_acq_pnrr + costo_da_acq_no + costo_finanz + costo_presente)*100:.1f}%</strong></td>
                            <td>Richiede approvazione immediata</td>
                        </tr>
                        <tr>
                            <td>  └─ PNRR (priorità)</td>
                            <td>€{costo_da_acq_pnrr:,.2f}</td>
                            <td>{costo_da_acq_pnrr/(costo_da_acq_pnrr + costo_da_acq_no + costo_finanz + costo_presente)*100:.1f}%</td>
                            <td>⚠️ Scadenza: Marzo 2026</td>
                        </tr>
                        <tr>
                            <td>  └─ Non-PNRR</td>
                            <td>€{costo_da_acq_no:,.2f}</td>
                            <td>{costo_da_acq_no/(costo_da_acq_pnrr + costo_da_acq_no + costo_finanz + costo_presente)*100:.1f}%</td>
                            <td>Programmabile nel tempo</td>
                        </tr>
                        <tr style="background: #e8f5e9;">
                            <td><strong>🟢 GIÀ FINANZIATO</strong></td>
                            <td><strong>€{costo_finanz:,.2f}</strong></td>
                            <td><strong>{costo_finanz/(costo_da_acq_pnrr + costo_da_acq_no + costo_finanz + costo_presente)*100:.1f}%</strong></td>
                            <td>Budget già allocato</td>
                        </tr>
                        <tr style="background: #e3f2fd;">
                            <td><strong>🔵 GIÀ PRESENTE</strong></td>
                            <td><strong>€{costo_presente:,.2f}</strong></td>
                            <td><strong>{costo_presente/(costo_da_acq_pnrr + costo_da_acq_no + costo_finanz + costo_presente)*100:.1f}%</strong></td>
                            <td>Dotazioni operative</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Dotazioni -->
            <div id="dotazioni" class="section">
                <h2>🔬 Fabbisogno per Dotazione</h2>

                <div class="info-box">
                    <h3>📋 Conformità Normativa</h3>
                    <p>Le dotazioni rispettano le <strong>linee guida DM 77/2022</strong> per le dotazioni minime standard di CDC e ODC.</p>
                </div>

                <div class="chart-container">
                    {fig_bar.to_html(include_plotlyjs=False, div_id="bar")}
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p><strong>USL Toscana Nord Ovest</strong> - Report Direzione Telemedicina</p>
            <p>Generato il {datetime.now().strftime("%d/%m/%Y alle %H:%M")}</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                Per informazioni e supporto: <strong>UOC Tecnologie</strong>
            </p>
        </div>
    </div>
</body>
</html>
"""

    # Scrivi file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✅ Report HTML generato: {filename}")
    print(f"\n📊 RIEPILOGO:")
    print(f"  • Fabbisogno PNRR (priorità):  € {costo_da_acq_pnrr:,.2f}")
    print(f"  • Fabbisogno non-PNRR:         € {costo_da_acq_no:,.2f}")
    print(f"  • TOTALE DA FINANZIARE:        € {costo_da_acq_pnrr + costo_da_acq_no:,.2f}")
    print(f"\n  ⚠️  SCADENZA PNRR: MARZO 2026")
    print(f"\n📱 Per aprire il report:")
    print(f"  • Doppio click su {filename}")
    print(f"  • Oppure: open {filename} (Mac) / start {filename} (Windows)")

    return filename


if __name__ == "__main__":
    print("=" * 80)
    print("GENERAZIONE REPORT HTML INTERATTIVO")
    print("=" * 80)
    print()

    filename = genera_html_report()

    print("\n" + "=" * 80)
    print("Il report HTML è pronto! User-friendly e pronto per la direzione!")
    print("=" * 80)
