FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local

# copy backend files
COPY app.py .
COPY index.html .

RUN useradd -m appuser
USER appuser

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
