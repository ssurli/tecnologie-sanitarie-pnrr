@echo off
REM Script avvio automatico Dashboard Telemedicina
REM USL Toscana Nord Ovest

title Dashboard Telemedicina - USL TNO
color 0A

echo ==========================================
echo   Avvio Dashboard Telemedicina USL TNO
echo ==========================================
echo.

REM Vai nella directory del progetto (MODIFICA QUESTO PATH!)
cd /d C:\Users\TuoUtente\tecnologie-sanitarie-pnrr

REM Attiva ambiente virtuale se esiste
if exist venv\Scripts\activate.bat (
    echo [*] Attivazione ambiente virtuale...
    call venv\Scripts\activate.bat
)

REM Avvia Streamlit con accesso LAN
echo [*] Avvio Streamlit su porta 8501...
echo [*] Accessibile da rete LAN
echo.
streamlit run dashboard_telemedicina.py --server.address 0.0.0.0 --server.port 8501 --server.headless true

REM Se streamlit si chiude, tieni la finestra aperta
echo.
echo [!] Streamlit terminato. Premi un tasto per chiudere...
pause >nul
