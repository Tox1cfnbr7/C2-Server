# Basis-Image
FROM python:3.10-slim

# Arbeitsverzeichnis festlegen
WORKDIR /app

# Abhängigkeiten zuerst kopieren und installieren (Docker-Caching nutzen)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Restlichen Code kopieren
COPY . .

# Port für den C2-Server freigeben
EXPOSE 8000

# Startkommando
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
 