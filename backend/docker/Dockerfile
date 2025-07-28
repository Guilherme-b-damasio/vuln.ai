FROM python:3.11-slim

# Atualizar e instalar dependências básicas + libs SSL para Perl (suporte HTTPS no Nikto)
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
	libnet-ssleay-perl \
	libio-socket-ssl-perl \
	openssl \
	&& rm -rf /var/lib/apt/lists/*

# Instalar Nikto manualmente (com caminho correto)
RUN git clone https://github.com/sullo/nikto.git /opt/nikto && \
	ln -s /opt/nikto/program/nikto.pl /usr/local/bin/nikto && \
	chmod +x /opt/nikto/program/nikto.pl

# Opcional: atualizar módulos Perl necessários para Nikto (pode aumentar build)
RUN perl -MCPAN -e 'install Bundle::LWP' || true

# Instalar OWASP ZAP
RUN set -ex && \
	curl -L -v -o /tmp/zap.tar.gz https://github.com/zaproxy/zaproxy/releases/download/v2.16.1/ZAP_2.16.1_Linux.tar.gz && \
	FILE_SIZE=$(stat -c%s /tmp/zap.tar.gz) && \
	if [ "$FILE_SIZE" -lt 10000000 ]; then \
	echo "Erro: O arquivo ZAP baixado é muito pequeno ($FILE_SIZE bytes). O download falhou ou foi interrompido." && \
	exit 1; \
	fi && \
	tar -xzf /tmp/zap.tar.gz -C /opt/ && \
	rm /tmp/zap.tar.gz

ENV ZAP_HOME=/opt/ZAP_2.16.1
ENV PATH="${ZAP_HOME}:${PATH}"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/relatorios && chmod 777 /app/relatorios

RUN chmod +x docker/entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["docker/entrypoint.sh"]
