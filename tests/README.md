# Тесты

## Запуск

```bash
pip install -r requirements-dev.txt

pytest                 # все тесты (coverage по умолчанию включён через pytest.ini)
pytest --cov           # то же, явно
pytest tests/unit      # только unit
pytest -k profile      # фильтр по имени
```

## Структура

- `unit/` — изолированные тесты хендлеров, сервисов, репозиториев (моки, in-memory SQLite).
- `integration/` — сквозные флоу.
- `fixtures/` — фабрики тестовых данных (пользователи, сообщения, колбэки).

Фикстуры — в `tests/conftest.py`: `mock_bot`, `db_session` (in-memory SQLite), `fake_user`, `fake_message`, `fake_callback`.
