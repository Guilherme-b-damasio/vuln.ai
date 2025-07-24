import subprocess

class NiktoScanner:
    def scan(self, target_url):
        print("[Nikto] Iniciando scan...")
        try:
            result = subprocess.run(
                ["nikto", "-h", target_url, "-output", "nikto_report.txt"],
                capture_output=True, text=True, timeout=300
            )
            print("[Nikto] Scan finalizado.")
            with open("nikto_report.txt", "r") as f:
                lines = f.readlines()
                print("[Nikto] Resumo dos primeiros resultados:")
                for line in lines[:10]:
                    print("  " + line.strip())
        except subprocess.TimeoutExpired:
            print("[Nikto] Tempo esgotado para o scan.")
        except FileNotFoundError:
            print("[Nikto] Nikto não encontrado no PATH.")
