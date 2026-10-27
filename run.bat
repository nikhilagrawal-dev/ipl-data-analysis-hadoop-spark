@echo off
echo Starting IPL Analytics Hub...
python -m streamlit run src/dashboard/app.py --server.port=8502
pause
