FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/ .

RUN chown -R root:root /app && \
    find /app -type d -exec chmod 755 {} \; && \
    find /app -type f -exec chmod 644 {} \;

RUN useradd -m appuser
USER appuser

EXPOSE 10000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --workers 50 --timeout 10 --max-requests 100 --max-requests-jitter 10 main:app"]