FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04
ARG DEBIAN_FRONTEND=noninteractive

# Remove any third-party apt sources to avoid issues with expiring keys.
RUN rm -f /etc/apt/sources.list.d/*.list

# Install some basic utilities.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    python3-dev \
    python3-pip \
    && python3 -m pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Create a working directory.
RUN mkdir /app
WORKDIR /app

COPY scripts/setup.sh requirements/server.txt /app

RUN apt update && bash setup.sh && rm setup.sh
RUN pip install -r server.txt && rm server.txt

COPY whisper_live /app/whisper_live

COPY run_server.py /app

RUN ls -la /app/whisper_live

CMD ["python3", "run_server.py", "--port", "9090", "--backend", "faster_whisper", "--faster_whisper_custom_model_path", "/app/whisper_live/models/faster-whisper-large-v3"]
# CMD ["python3", "run_server.py", "--port", "9090", "--backend", "faster_whisper", "--faster_whisper_custom_model_path", "/app/whisper_live/models/faster-whisper-large-v3", "--omp_num_threads", "4", "--no_single_model"]