# ---- Base Image ----
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

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

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Starting Streamlit app..."\n\
echo "PORT: $PORT"\n\
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:0:10}..."\n\
echo "GOOGLE_API_KEY: ${GOOGLE_API_KEY:0:10}..."\n\
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false' > /app/start.sh && \
chmod +x /app/start.sh

# Streamlit needs the port provided by Vercel
EXPOSE 8501

# ---- Start the app ----
CMD ["/app/start.sh"]