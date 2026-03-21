<div align="center">

# 🎯 Quizbot

**A production-grade Telegram quiz platform — create, manage, and run interactive quizzes at scale.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0-009485?logo=telegram)](https://pyrogram.org)
[![PTB](https://img.shields.io/badge/python--telegram--bot-20.x-0088CC?logo=telegram)](https://python-telegram-bot.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

**Sponsored by [Qzio](https://qzio.in) &nbsp;•&nbsp; Developed by [devgagan](https://devgagan.in)**

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [VPS Setup — Step-by-Step](#-vps-setup--step-by-step)
- [Running the Bots](#-running-the-bots)
  - [Running Both Bots Together](#running-both-bots-together)
  - [Running Separately](#running-separately)
- [BotFather Setup](#-botfather-setup)
- [Configuration Reference](#-configuration-reference)
- [Project Structure](#-project-structure)
- [Credits](#-credits)

---

## ✨ Features

| Category | Capability |
|---|---|
| **Quiz Creation** | Text input, TXT file, PDF, image/OCR, Drishti IAS URL, Wikipedia/BBC/news articles |
| **Quiz Formats** | Standard, Sectional (different timers per section), Marathon (unlimited questions) |
| **Poll Support** | Forward any Telegram quiz poll — bot auto-cleans `[1/100]` tags and filters |
| **Smart Filtering** | Remove usernames, links, or custom word lists from imported polls |
| **Editing** | Shuffle questions, add/change titles, edit timers, add/remove questions |
| **Access Control** | Free and paid quiz tiers — restrict by user ID or group chat |
| **Analytics** | Per-user performance, quiz engagement counters, topper comparison |
| **HTML Reports** | Beautiful self-contained HTML scorecards with light/dark theme |
| **Scheduling** | Launch quizzes at specific times via the scheduler bot |
| **Inline Sharing** | Share any quiz by ID via inline query |
| **Assignments** | Student submission tracking with creator reply forwarding |
| **Broadcast** | Send announcements to all users (owner only) |

---

## 🏗 Architecture

```
Quizbot/
│
├── main.py      ← Pyrogram bot  (quiz creation, file imports, management)
├── bot.py       ← PTB bot       (quiz runner, scheduler, poll tracking)
├── func.py      ← Shared helpers (DB, image, HTML, premium checks)
├── c.py         ← HTML report generator
└── config.py    ← Centralised configuration (reads from .env)
```

The two bots are **independent processes** sharing the same MongoDB database:

- **`main.py`** handles everything that requires the MTProto client (file downloads, channel reading, inline queries, quiz creation).
- **`bot.py`** handles high-throughput quiz sessions — sending polls rapidly, tracking answers, building leaderboards.

---

## 🔧 Prerequisites

| Requirement | Minimum Version | Notes |
|---|---|---|
| Python | 3.10+ | 3.11 recommended |
| MongoDB | Atlas free tier or self-hosted | `MONGO_URI` etc. in `.env` |
| Telegram API credentials | — | From [my.telegram.org](https://my.telegram.org) |
| Two Telegram bot tokens | — | One per bot, from @BotFather |
| VPS / Server | 1 vCPU, 1 GB RAM | Ubuntu 22.04 recommended |

---

## ⚡ Quick Start

```bash
git clone https://github.com/devgaganin/Quizbot.git
cd Quizbot
cp .env.example .env
nano .env          # fill in your values
pip install -r requirements.txt
playwright install chromium   # needed for PDF generation
python main.py &
python bot.py  &
```

---

## 🖥 VPS Setup — Step-by-Step

> Tested on **Ubuntu 22.04 LTS**. Commands require `sudo` where indicated.

### 1 — Update the system

```bash
sudo apt update && sudo apt upgrade -y
```

### 2 — Install Python 3.11

```bash
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
python3.11 --version   # should print Python 3.11.x
```

### 3 — Install system dependencies

```bash
sudo apt install -y \
  git \
  build-essential \
  libssl-dev \
  libffi-dev \
  libjpeg-dev \
  libpng-dev \
  libfreetype6-dev \
  fonts-noto \
  fonts-noto-cjk \
  wget curl unzip
```

### 4 — Clone the repository

```bash
cd /opt
sudo git clone https://github.com/devgaganin/Quizbot.git
sudo chown -R $USER:$USER /opt/Quizbot
cd /opt/Quizbot
```

### 5 — Create and activate a virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 6 — Install Python packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 7 — Install Playwright + Chromium (PDF generation)

```bash
playwright install chromium
playwright install-deps chromium
```

### 8 — Configure environment variables

```bash
cp .env.example .env
nano .env
```

Fill in **all** required values (see [Configuration Reference](#-configuration-reference) below). Save with `Ctrl+O`, exit with `Ctrl+X`.

### 9 — Verify the setup

```bash
python -c "from config import BOT_TOKEN; print('Config OK' if BOT_TOKEN else 'BOT_TOKEN missing')"
```

---

## 🚀 Running the Bots

### Running Both Bots Together

The easiest way on a VPS is to use **systemd** services so both bots auto-restart on crash or reboot.

#### Create systemd service for `main.py`

```bash
sudo nano /etc/systemd/system/quizbot-main.service
```

Paste:

```ini
[Unit]
Description=Quizbot — Pyrogram (main.py)
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/Quizbot
ExecStart=/opt/Quizbot/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

#### Create systemd service for `bot.py`

```bash
sudo nano /etc/systemd/system/quizbot-scheduler.service
```

Paste:

```ini
[Unit]
Description=Quizbot — PTB Scheduler (bot.py)
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/Quizbot
ExecStart=/opt/Quizbot/venv/bin/python bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

#### Enable and start both services

```bash
sudo systemctl daemon-reload
sudo systemctl enable quizbot-main quizbot-scheduler
sudo systemctl start  quizbot-main quizbot-scheduler
```

#### Check status

```bash
sudo systemctl status quizbot-main
sudo systemctl status quizbot-scheduler
```

#### View live logs

```bash
# main.py logs
sudo journalctl -u quizbot-main -f

# bot.py logs
sudo journalctl -u quizbot-scheduler -f

# Both together
sudo journalctl -u quizbot-main -u quizbot-scheduler -f
```

---

### Running Separately

If you prefer to run without systemd (e.g. for testing), use two terminal sessions or `screen`/`tmux`.

#### Install screen (if not present)

```bash
sudo apt install -y screen
```

#### Run `main.py` (Quiz Creator Bot)

```bash
# In terminal 1 (or screen session)
cd /opt/Quizbot
source venv/bin/activate
python main.py
```

#### Run `bot.py` (Quiz Scheduler Bot)

```bash
# In terminal 2 (or another screen session)
cd /opt/Quizbot
source venv/bin/activate
python bot.py
```

#### Using screen named sessions

```bash
# Start main.py in a named screen
screen -S quiz-main -dm bash -c "cd /opt/Quizbot && source venv/bin/activate && python main.py"

# Start bot.py in a named screen
screen -S quiz-bot  -dm bash -c "cd /opt/Quizbot && source venv/bin/activate && python bot.py"

# Attach to see output
screen -r quiz-main
screen -r quiz-bot

# Detach from screen (without stopping it)
# Press: Ctrl+A, then D
```

---

## 🤖 BotFather Setup

After creating both bots with [@BotFather](https://t.me/BotFather), set their command menus.

All commands are ready to copy from [`BOTFATHER_COMMANDS.txt`](BOTFATHER_COMMANDS.txt).

**Steps:**

1. Open Telegram → search `@BotFather`
2. Send `/setcommands`
3. Select **Bot 1** (creator/main bot)
4. Open `BOTFATHER_COMMANDS.txt`, copy the **BOT 1 block** (lines under the first `=====` section), paste and send
5. Send `/setcommands` again
6. Select **Bot 2** (scheduler bot)
7. Copy the **BOT 2 block** and send

**Additional recommended BotFather settings:**

```
/setinline      → Enable inline mode for Bot 1 (inline quiz sharing)
/setprivacy     → Disable group privacy for Bot 2 (to read group messages)
/setjoingroups  → Enable if you want users to add Bot 2 to groups
```

---

## ⚙️ Configuration Reference

All values live in `.env`. Full documented template: [`.env.example`](.env.example)

| Variable | Required | Description |
|---|---|---|
| `API_ID` | ✅ | Telegram API ID from my.telegram.org |
| `API_HASH` | ✅ | Telegram API Hash from my.telegram.org |
| `BOT_TOKEN` | ✅ | Token for the Pyrogram bot (main.py) |
| `BOT_TOKEN_2` | ✅ | Token for the PTB scheduler bot (bot.py) |
| `MONGO_URI` | ✅ | Primary MongoDB connection string |
| `MONGO_URI_2` | ✅ | Secondary MongoDB connection string |
| `MONGO_URIX` | ✅ | Async quizzes collection MongoDB URI |
| `DB_NAME` | ✅ | MongoDB database name (default: `quiz_bot`) |
| `OWNER_ID` | ✅ | Space-separated Telegram user IDs |
| `LOG_GROUP` | ✅ | Negative chat ID for error/log channel |
| `FORCE_SUB` | ✅ | Channel ID users must join |
| `BOT_GROUP` | ✅ | Main community group ID |
| `CHANNEL_ID` | ✅ | Announcement channel ID |
| `MASTER_KEY` | ✅ | AES key for quiz file encryption |
| `IV_KEY` | ✅ | AES IV prefix |
| `FREEMIUM_LIMIT` | ➖ | Free user question limit (0 = unlimited) |
| `PREMIUM_LIMIT` | ➖ | Premium user question limit (default: 500) |
| `FREE_BOT` | ➖ | `true` to skip all premium checks |
| `PAY_API` | ➖ | Payment API endpoint URL |
| `MYSQL_HOST/USER/PASS/DB` | ➖ | MySQL credentials for web panel |

---

## 📁 Project Structure

```
Quizbot/
├── main.py                  # Pyrogram bot — quiz creation & management
├── bot.py                   # PTB bot — scheduler, runner, leaderboard
├── func.py                  # Core utilities, DB helpers, image processing
├── c.py                     # HTML quiz report generator
├── config.py                # Central config (reads .env)
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .gitignore
├── LICENSE
├── BOTFATHER_COMMANDS.txt   # Ready-to-paste BotFather command lists
└── README.md
```

---

## 🙏 Credits

<div align="center">

| Role | |
|---|---|
| **Developed by** | [devgagan](https://devgagan.in) |
| **Sponsored by** | [Qzio](https://qzio.in) — The Smart Quiz Platform |
| **Telegram Library** | [Pyrogram](https://pyrogram.org) & [python-telegram-bot](https://python-telegram-bot.org) |
| **Database** | [MongoDB Atlas](https://mongodb.com) |

---

*Built with ❤️ for educators, exam aspirants, and quiz creators.*

**© 2025 devgagan · Sponsored by Qzio**

</div>
