import subprocess
import os

class NiktoScanner:
    def scan(self, target_url):
        print("[Nikto] Iniciando scan...")

        output_dir = "../app/relatorios"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "nikto_report.txt")

        # Abre o arquivo para escrita enquanto lê a saída do processo
        with open(output_path, "w", encoding="utf-8") as outfile:
            # Executa o nikto e captura stdout em tempo real
            process = subprocess.Popen(
                [
                    "nikto",
                    "-h", target_url,
                    "-output", output_path
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            for line in process.stdout:
                print("[Nikto]", line.strip()) 
                outfile.write(line)             
                outfile.flush()                 

            process.wait()

        if process.returncode == 0:
            print("[Nikto] Scan finalizado com sucesso.")
            return output_path
        else:
            print(f"[Nikto] Scan finalizado com erro, código: {process.returncode}")
            return None
