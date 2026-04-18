FROM python:3.11-slim

WORKDIR /app

# Set Ollama host for Docker Desktop (Mac/Windows)
# This tells the container to reach Ollama on the host machine
# Linux users: override with -e OLLAMA_HOST=http://172.17.0.1:11434
ENV OLLAMA_HOST=http://host.docker.internal:11434
# Disable CrewAI telemetry and tracing prompts (hangs in non-interactive Docker)
ENV CREWAI_DISABLE_TELEMETRY=true
ENV OTEL_SDK_DISABLED=true
ENV CREWAI_TRACING_ENABLED=false

COPY requirements.txt .
COPY requirements-crewai.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-crewai.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
