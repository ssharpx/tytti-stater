# Tytti Starter

A Telegram bot that tracks chat activity and posts a daily statistics report.

## Features

- Counts messages sent by each chat member
- Tracks new members joining the chat, including Telegram Premium accounts
- Posts a daily report at 00:00 UTC (configurable via `UPDATE_TIME` in `config.py`) with:
  - number of new followers and how many of them have Premium
  - total number of messages
  - top 10 most active users
- Resets message counters after each report

## Example report

```
Chat statistics for 27.10.2026:

➕ New followers: +12
🟩 Premium accounts among new subscribers: 3

✍️ Total messages sent: 845

👥 Top users:
1. @alice (124)
2. @bob (98)
3. No username user (76)
```

## Tech stack

- Python 3.12
- [aiogram 3](https://docs.aiogram.dev/) — Telegram Bot API framework
- SQLAlchemy 2 (async) + asyncpg
- PostgreSQL 15
- APScheduler — scheduled reports
- Docker & Docker Compose

## Requirements

- [Docker](https://docs.docker.com/get-docker/) with Docker Compose
- `make` (optional, for shortcut commands)

## Bot setup in Telegram

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the token.
2. Disable privacy mode so the bot can read all group messages:
   `/mybots` → your bot → **Bot Settings** → **Group Privacy** → **Turn off**.
3. Add the bot to your group and **make it an administrator**.
   Admin rights are required to receive member join events.

> If the bot was already in the group before privacy mode was disabled, remove it and add it again.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ssharpx/tytti-starter.git
   cd tytti-starter
   ```

2. Create the environment file and fill in the values:

   ```bash
   cp .env.example .env
   ```

3. Start the bot and the database:

   ```bash
   make up
   ```

4. Check that everything is running:

   ```bash
   make logs
   ```

## Configuration

All settings are stored in `.env`:

| Variable      | Description                                   | Example          |
|---------------|-----------------------------------------------|------------------|
| `TOKEN_BOT`   | Bot token from @BotFather                     | `123:ABC…`       |
| `OUTPUT_CHAT` | ID of the chat where reports are sent         | `-1001234567890` |
| `DB_HOST`     | Database host (service name in Compose)       | `database`       |
| `DB_PORT`     | Database port                                 | `5432`           |
| `DB_NAME`     | Database name                                 | `tytti`          |
| `DB_USER`     | Database user                                 | `tytti`          |
| `DB_PASS`     | Database password                             | —                |

Values must be written without quotes and without spaces around `=`.

### How to get the chat ID

Group and supergroup IDs are negative numbers, usually starting with `-100`.
The easiest way to find one is to add [@getidsbot](https://t.me/getidsbot) to the chat
or forward any message from the chat to it.

## Commands

| Command                          | Description                                  |
|----------------------------------|----------------------------------------------|
| `make up`                        | Build and start all services                 |
| `make down`                      | Stop and remove containers                   |
| `make restart`                   | Restart the bot                              |
| `make rebuild`                   | Rebuild the bot without cache                |
| `make logs`                      | Follow bot logs                              |
| `make logs-db`                   | Follow database logs                         |
| `make ps`                        | Show container status                        |
| `make db-shell`                  | Open `psql` in the database container        |
| `make db-backup`                 | Dump the database to `backups/`              |
| `make db-restore FILE=<path>`    | Restore the database from a dump             |
| `make clean`                     | Stop containers and **delete all data**      |

Without `make`, use Docker Compose directly, e.g. `docker compose up -d --build`.

## Project structure

```
.
├── main.py                 # Entry point: bot, dispatcher, scheduler
├── config.py               # Settings and logging
├── src/
│   ├── controler/          # Telegram handlers
│   ├── service/            # Business logic and report formatting
│   ├── repository/         # Database queries
│   ├── models/             # SQLAlchemy models
│   └── core/               # Database engine and session
├── Dockerfile
├── compose.yaml
├── Makefile
├── requirements.txt
└── .env.example
```

## License

MIT