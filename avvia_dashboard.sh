#!/bin/bash
# Script avvio automatico Dashboard Telemedicina
# USL Toscana Nord Ovest

echo "=========================================="
echo "  Avvio Dashboard Telemedicina USL TNO"
echo "=========================================="
echo ""

# Vai nella directory del progetto
cd /home/user/tecnologie-sanitarie-pnrr

# Attiva ambiente virtuale se esiste
if [ -d "venv" ]; then
    echo "🔧 Attivazione ambiente virtuale..."
    source venv/bin/activate
fi

# Avvia Streamlit con accesso LAN
echo "🚀 Avvio Streamlit su porta 8501..."
echo "📡 Accessibile da rete LAN"
echo ""
streamlit run dashboard_telemedicina.py --server.address 0.0.0.0 --server.port 8501 --server.headless true

# Se streamlit si chiude, tieni la finestra aperta
echo ""
echo "⚠️  Streamlit terminato. Premi un tasto per chiudere..."
read -n 1
