from flask import Flask, request, jsonify
from scanners.zap_scanner import ZapScanner
from scanners.nikto_scanner import NiktoScanner
import os

app = Flask(__name__)

# Configurações: URL e API key do ZAP
zap_api_url = os.getenv("ZAP_API_URL", "http://localhost:8080")
zap_api_key = os.getenv("ZAP_API_KEY", None)

zap_scanner = ZapScanner(base_url=zap_api_url, api_key=zap_api_key)
nikto_scanner = NiktoScanner()

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    target_url = data["url"]

    # Rodar scan ZAP
    zap_alerts = zap_scanner.scan(target_url)
    zap_summary = [{"alert": a.get("alert"), "risk": a.get("risk"), "url": a.get("url")} for a in zap_alerts]

    # Rodar scan Nikto (ele salva resultado em arquivo e imprime no console)
    nikto_result_summary = []
    try:
        nikto_output_path = nikto_scanner.scan(target_url)
        print(f"Lendo relatório Nikto em: {nikto_output_path}")
        print(f"[DEBUG] Tentando abrir: {nikto_output_path}")
        print(f"[DEBUG] Arquivo existe? {os.path.exists(nikto_output_path)}")
        output_path = os.path.join("relatorios", "nikto_report.txt")
        with open(output_path, "r") as f:
            lines = f.readlines()
            nikto_result_summary = lines
    except Exception as e:
        nikto_result_summary = [f"Erro ao executar Nikto: {str(e)}"]

    return jsonify({
        "zap_alerts_count": len(zap_alerts),
        "zap_alerts": zap_summary,
        "nikto_summary": nikto_result_summary
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
