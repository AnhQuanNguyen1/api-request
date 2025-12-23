FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Chạy file bạn muốn làm entrypoint.
# CMD ["python", "api_request.py"]
# CMD ["python", "insert_records_clickhouse.py"]

# Nếu bạn muốn chạy insert_records_clickhouse.py thì đổi thành:
# CMD ["python", "insert_records_clickhouse.py"]
