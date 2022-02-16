mkdir -p ~/.streamlit/

echo "\
[theme]\n\
primaryColor='#d33682'\n\
backgroundColor='#002b36'\n\
secondaryBackgroundColor='#586e75'\n\
textColor='#fafafa'\n\
font='sans serif'\n\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
