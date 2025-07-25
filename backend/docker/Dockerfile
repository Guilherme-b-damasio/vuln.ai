FROM python:3.11-slim

# Atualizar e instalar dependências básicas
# --no-install-recommends reduz o tamanho da imagem ao não instalar pacotes recomendados.
RUN apt-get update && apt-get install -y --no-install-recommends \
	openjdk-17-jre-headless \
	wget \
	unzip \
	curl \
	git \
	perl \
	ca-certificates \
	tar \
	gzip \
	# Limpa o cache do apt para reduzir o tamanho da imagem.
	&& rm -rf /var/lib/apt/lists/*

# Instalar Nikto manualmente (com caminho correto)
# Clona o Nikto em /opt/nikto, cria um symlink para fácil execução e o torna executável.
RUN git clone https://github.com/sullo/nikto.git /opt/nikto && \
	ln -s /opt/nikto/program/nikto.pl /usr/local/bin/nikto && \
	chmod +x /opt/nikto/program/nikto.pl

# Instalar OWASP ZAP
# Usa curl -L para downloads mais robustos, especialmente com redirecionamentos.
# O 'set -ex' faz com que o comando falhe imediatamente se alguma parte falhe e imprime o comando.
# Adicionado '-v' ao curl para saída mais detalhada (verbosa) em caso de falha de download.
# Adicionada uma verificação de tamanho do arquivo para garantir que o download foi completo.
# URL e formato de arquivo atualizados para a versão 2.16.1 do ZAP (agora .tar.gz).
RUN set -ex && \
	curl -L -v -o /tmp/zap.tar.gz https://github.com/zaproxy/zaproxy/releases/download/v2.16.1/ZAP_2.16.1_Linux.tar.gz && \
	# Verifica se o arquivo baixado tem um tamanho razoável (por exemplo, mais de 10MB)
	# ZAP 2.16.1 Linux.tar.gz tem aproximadamente 224MB, então 10MB é um limite seguro para indicar um download falho.
	FILE_SIZE=$(stat -c%s /tmp/zap.tar.gz) && \
	if [ "$FILE_SIZE" -lt 10000000 ]; then \
	echo "Erro: O arquivo ZAP baixado é muito pequeno ($FILE_SIZE bytes). O download falhou ou foi interrompido." && \
	exit 1; \
	fi && \
	# Descompacta o arquivo .tar.gz no diretório /opt/
	tar -xzf /tmp/zap.tar.gz -C /opt/ && \
	rm /tmp/zap.tar.gz

# Define ZAP_HOME e o adiciona ao PATH para fácil execução de scripts do ZAP.
# ZAP_HOME atualizado para a versão 2.16.1.
ENV ZAP_HOME=/opt/ZAP_2.16.1
ENV PATH="${ZAP_HOME}:${PATH}"

# Copiar código Python e instalar dependências
WORKDIR /app
COPY requirements.txt .
# Instala as dependências Python, --no-cache-dir reduz o tamanho da imagem.
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Garante que o script de entrypoint seja executável.
RUN chmod +x docker/entrypoint.sh

# Expor porta da API do ZAP (modo daemon)
EXPOSE 8080

# Entrypoint do container
# Usa ENTRYPOINT no formato executável para melhor tratamento de sinais e consistência.
ENTRYPOINT ["docker/entrypoint.sh"]
