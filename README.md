
### Структура проекта

text-to-image-service/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   └── model_loader.py
│   ├── utils/
│   │   └── image_utils.py
│   └── templates/
│       ├── index.html
│       └── result.html
├── nginx/
│   └── nginx.conf
├── config/
│   └── config.yaml
├── scripts/
│   └── download_models.py
├── outputs/
│   └── .gitkeep
└── README.md


# Self-Hosted Text-to-Image Service

Локальный веб-сервис для генерации изображений по текстовому описанию.

## Возможности

- Генерация изображений через веб-интерфейс или API
- Поддержка Stable Diffusion 1.5, 2.1, XL
- Гибкие параметры генерации
- Автоочистка старых файлов
- GPU acceleration (NVIDIA)

## Быстрый старт

### С Docker Compose (рекомендуется)

```bash
# Клонируйте репозиторий
git clone https://github.com/JuliaKudryavtseva/wink-text-to-image.git
cd wink-text-to-image

# Запустите сервис
docker-compose up -d

# Откройте в браузере
# http://localhost
```
## Использование


### Без Docker

```bash
pip install -r requirements.txt
python app/main.py
```


### Запуск с Docker:
```bash
docker-compose up -d
# Открыть http://localhost