#!/bin/bash
# Iniciar OWASP ZAP daemon sem API key
$ZAP_HOME/zap.sh -daemon -config api.key.enabled=false -port 8080 &
ZAP_PID=$!

# Esperar o ZAP iniciar (ajuste o sleep conforme necessário)
sleep 15

# Rodar seu script Python que orquestra os scans
# O './app.py' garante que o script seja executado a partir do diretório atual de trabalho (/app).
python ./app/app.py

# Parar o ZAP
kill $ZAP_PID
wait $ZAP_PID 2>/dev/null
