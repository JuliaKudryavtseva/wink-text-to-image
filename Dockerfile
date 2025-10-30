FROM python:3.9-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем пользователя для безопасности
RUN useradd -m -r appuser && \
    chown -R appuser:appuser /app
USER appuser

# Создаем директории
RUN mkdir -p outputs

EXPOSE 5000

CMD ["python", "app/main.py"]