# ---- Base Image ----
FROM python:3.11-slim AS base

# Ensure stdout/stderr is unbuffered and default encoding is UTF-8
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUTF8=1

# Set work directory
WORKDIR /app

# ---- Dependencies Layer ----
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- Application Layer ----
COPY . .

# Streamlit needs the port provided by Vercel
EXPOSE 8501

# ---- Start the app ----
# Vercel sets the PORT env var automatically. Streamlit must bind to 0.0.0.0.
CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]