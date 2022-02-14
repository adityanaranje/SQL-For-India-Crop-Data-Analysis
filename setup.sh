mkdir -p ~/.streamlit/
echo "[theme]
primaryColor='#13fbe6'
backgroundColor='#080808'
secondaryBackgroundColor='#22222d'
textColor='#fffefe'
font='serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml