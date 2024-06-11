FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install -r requirements.txt
COPY . .
EXPOSE 9500

# Ensure commands run inside the virtual environment
CMD ["/opt/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9500"]
