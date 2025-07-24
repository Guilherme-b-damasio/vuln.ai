FROM python:3.11-slim

# Instalar dependências básicas
RUN apt-get update && apt-get install -y \
	openjdk-11-jre-headless \
	nikto \
	wget \
	unzip \
	curl \
	&& rm -rf /var/lib/apt/lists/*

# Instalar OWASP ZAP
RUN wget -O /tmp/zap.zip https://github.com/zaproxy/zaproxy/releases/download/v2.13.0/ZAP_2_13_0_unix.zip \
	&& unzip /tmp/zap.zip -d /opt/ \
	&& rm /tmp/zap.zip
ENV ZAP_HOME=/opt/ZAP_2_13_0
ENV PATH="$ZAP_HOME:$PATH"

# Copiar código Python e instalar dependências
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expor porta da API do ZAP (se usar modo daemon)
EXPOSE 8080

# Script para iniciar ZAP em modo daemon e rodar seu scanner
CMD ["./entrypoint.sh"]
