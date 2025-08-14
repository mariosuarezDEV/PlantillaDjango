FROM python:3.12-bullseye

WORKDIR /app

# Instalar dependencias del sistema necesarias para VS Code Server
RUN apt-get update && apt-get install -y \
    curl wget tar gzip libnss3 libx11-6 libxkbfile1 libsecret-1-0 libgtk-3-0 libasound2 git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "proyecto.asgi:application"]
