import requests
import time
from urllib.parse import urlencode

class ZapScanner:
    def __init__(self, base_url="http://localhost:8080", api_key=None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key

    def _build_url(self, path, params=None):
        if params is None:
            params = {}
        if self.api_key:
            params['apikey'] = self.api_key
        query = urlencode(params)
        return f"{self.base_url}{path}?{query}"

    def scan(self, target_url):
        print("[ZAP] Iniciando scan...")
        params = {'url': target_url, 'recurse': 'true'}
        start_scan_url = self._build_url('/JSON/ascan/action/scan/', params)
        resp = requests.get(start_scan_url)
        if resp.status_code != 200:
            print(f"[ZAP] Erro ao iniciar scan: {resp.status_code}")
            return []
        scan_id = resp.json().get('scan')

        status = 0
        while status < 100:
            time.sleep(5)
            status_url = self._build_url('/JSON/ascan/view/status/', {'scanId': scan_id})
            status_resp = requests.get(status_url)
            if status_resp.status_code != 200:
                print(f"[ZAP] Erro ao obter status do scan: {status_resp.status_code}")
                break
            status = int(status_resp.json().get('status', 0))
            print(f"[ZAP] Scan em andamento: {status}%")

        alerts_url = self._build_url('/JSON/core/view/alerts/', {'baseurl': target_url})
        alerts_resp = requests.get(alerts_url)
        if alerts_resp.status_code != 200:
            print(f"[ZAP] Erro ao buscar alertas: {alerts_resp.status_code}")
            return []
        alerts = alerts_resp.json().get('alerts', [])
        print(f"[ZAP] Scan finalizado com {len(alerts)} alertas encontrados.")
        return alerts
