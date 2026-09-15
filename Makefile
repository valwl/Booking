.PHONY: up down restart test lint format status logs clean

# Запуск всех контейнеров в фоновом режиме
up:
	docker compose up -d

# Остановка контейнеров
down:
	docker compose down

# Перезапуск инфраструктуры
restart:
	docker compose down && docker compose up -d

# Просмотр статуса контейнеров
status:
	docker compose ps

# Запуск тестов проекта (автоматически подхватит настройки из pyproject.toml)
test:
	docker compose exec -e PYTHONDONTWRITEBYTECODE=1 backend pytest

# Проверка кода линтером Ruff
lint:
	docker compose exec backend ruff check .

# Автоматическое форматирование кода с помощью Ruff
format:
	docker compose exec backend ruff format .

# Просмотр логов бэкенда в реальном времени
logs:
	docker compose logs -f backend

# Очистка проекта от временных файлов Celery и кэша Python локально
clean:
	rm -rf .pytest_cache .ruff_cache __pycache__
	rm -f backend/booking_project/celerybeat-schedule*
