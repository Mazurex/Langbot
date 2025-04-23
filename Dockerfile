FROM python:3.11-slim-bookworm

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python", "bot/main.py"]