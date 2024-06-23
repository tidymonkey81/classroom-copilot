FROM python:latest
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .
EXPOSE ${BACKEND_PORT}

# Ensure commands run inside the virtual environment
CMD /opt/venv/bin/uvicorn main:app --host 0.0.0.0 --port ${BACKEND_PORT}
