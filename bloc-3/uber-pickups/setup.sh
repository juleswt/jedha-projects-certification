mkdir -p ~/bloc-3/uber-pickups/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/bloc-3/uber-pickups/.streamlit/config.toml
