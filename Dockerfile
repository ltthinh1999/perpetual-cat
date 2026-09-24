# =====================================================================
# Stage 1: Build dependencies cleanly
# =====================================================================
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# =====================================================================
# Stage 2: Final minimal runtime container environment
# =====================================================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy installed Python packages from builder stage safely
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/

# Update internal binary paths
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

RUN mkdir -p data

CMD ["python", "src/main.py"]
