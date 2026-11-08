# Terms Of Reference

Telegram-бот, который проводит интервью с заказчиком и генерирует техническое задание через LLM.
Результат выгружается в DOCX и PDF и отправляется в чат.

## Стек

- Python 3.11+, aiogram 3
- OpenAI SDK (любой OpenAI-совместимый API)
- SQLAlchemy 2 async + SQLite (aiosqlite), Alembic
- Redis + arq (фоновый воркер)
- python-docx, fpdf2

## Быстрый старт

```bash
git clone https://github.com/HellenWeb/termsOfReference-llm.git
cd termsOfReference-llm
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # заполнить BOT_TOKEN и LLM_API_KEY
python -m bot.main
```

Файл БД `data/app.db` создаётся автоматически при первом запуске — каталог `data/` уже есть в репозитории.

Воркер запускается отдельным процессом (требуется Redis):

```bash
python -m bot.workers.run
```

## Переменные окружения

| Переменная | Назначение |
| --- | --- |
| `BOT_TOKEN` | Токен бота от [@BotFather](https://t.me/BotFather) |
| `LLM_API_KEY` | Ключ LLM-провайдера |
| `LLM_BASE_URL` | Базовый URL OpenAI-совместимого API |
| `LLM_MODEL` | Идентификатор модели |
| `DATABASE_URL` | DSN SQLite, по умолчанию `sqlite+aiosqlite:///./data/app.db` |
| `REDIS_URL` | Подключение к Redis для воркера и очереди |
| `GENERATION_COST_CREDITS` | Стоимость одной генерации в кредитах |
| `FREE_WELCOME_CREDITS` | Кредиты при первом запуске пользователя |

Полный список — в `.env.example`. `.env` в репозиторий не попадает.

## Структура проекта

```text
bot/
├── handlers/        # /start, интервью, профиль
├── keyboards/       # inline-клавиатуры
├── states/          # FSM-состояния диалога
├── services/        # LLM-клиент и генерация ТЗ
├── domain/          # enum'ы, порты, модели предметной области
├── application/     # сервисы кредитов и генерации
├── infrastructure/  # SQLAlchemy/SQLite, репозитории, Redis, arq
├── middlewares/     # сессия БД, пользователь
├── assets/fonts/    # DejaVu Sans для кириллицы в PDF
├── workers/         # arq-воркер
├── config.py        # настройки из .env
└── main.py          # точка входа
migrations/          # Alembic
data/                # файл SQLite
```

## Известные ограничения

- FSM хранится в памяти: при перезапуске незавершённые интервью теряются (`RedisStorage` в `bot/main.py` закомментирован).
- Воркер — скелет: `generate_tz_task` ничего не выполняет, генерация идёт в обработчике.
- Telegram Stars не реализованы: есть модель `Payment` и кнопка «Пополнить кредиты» без обработчика.
- Списание кредитов за генерацию не подключено; welcome-бонус начисляется в `UserMiddleware`.
- Схема создаётся через `Base.metadata.create_all` при старте; Alembic настроен, но миграции не применяются автоматически.
