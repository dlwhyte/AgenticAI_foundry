FROM python:3.11-slim

WORKDIR /app

# Note: OLLAMA_HOST is auto-detected at runtime
# - Tries localhost first (for local runs)
# - Falls back to host.docker.internal (Docker Desktop on Mac/Windows)
# - Can be overridden: docker run -e OLLAMA_HOST=http://your-host:11434 ...

COPY requirements.txt .
COPY requirements-crewai.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-crewai.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
