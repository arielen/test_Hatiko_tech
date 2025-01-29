# 👥 IMEI Check Telegram Bot

## Table of Contents
| Section | Description |
|---------|------------|
| [Project Description](#-project-description) | Overview of the project and its features |
| [Technologies Used](#️-technologies-used) | List of technologies utilized in the project |
| [Features](#-features) | Functionalities provided by the system |
| [API Requests](#-3-api-requests) | API endpoint details for IMEI checking |
| [How to Run the Project](#️-how-to-run-the-project) | Steps to set up and run the project |
| [Testing](#-testing) | Instructions for running tests and linting |
| [Project Structure](#-project-structure) | Folder structure explanation |
| [Contacts](#-contacts) | Developer contact information |

## 🚀 Project Description
This project is a **backend system** built with **FastAPI**, integrated with a **Telegram bot** (`aiogram`), designed for **checking IMEI numbers** of devices.  
The system allows:
- 🌟 **Checking IMEI numbers via a Telegram bot**.
- 🔑 **Restricting access via a whitelist** of authorized users.
- 🔒 **Authenticating API requests using tokens**.
- 🛠️ **Using PostgreSQL** for data storage and **Redis** for caching.
- 🐳 **Running with Docker & docker-compose**.
- ✅ **Testing with Pytest, Tox** and **linting with Ruff**.

---

## ⚙️ **Technologies Used**
- **Backend:** ![Python 3.13](https://img.shields.io/badge/Python-3.13-000000?style=for-the-badge&labelColor=fafbfc&logo=python&logoColor=306998&color=2b3137) ![FastAPI](https://img.shields.io/badge/FastAPI-2b3137?style=for-the-badge&logo=fastapi)
- **Database:** ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-2b3137?style=for-the-badge&logo=postgresql)
- **Cache & Messaging:** ![Redis](https://img.shields.io/badge/Redis-2b3137?style=for-the-badge&logo=redis)
- **Telegram Bot:** ![Aiogram](https://img.shields.io/badge/Aiogram-2b3137?style=for-the-badge&logo=telegram&logoColor=white)
- **Testing & CI/CD:** ![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-fafbfc?style=for-the-badge&labelColor=fafbfc&logo=github-actions&logoColor=black&color=2b3137) ![Tox](https://img.shields.io/badge/Tox-2b3137?style=for-the-badge&logo=tox) ![Pytest](https://img.shields.io/badge/Pytest-2b3137?style=for-the-badge&logo=pytest) ![Ruff](https://img.shields.io/badge/Ruff-2b3137?style=for-the-badge&logo=ruff)
- **Deployment:** ![Docker & Docker Compose](https://img.shields.io/badge/Docker-Compose-fafbfc?style=for-the-badge&labelColor=fafbfc&logo=docker&locoColor=black&color=2b3137)

---

## 📌 **Features**
### 🔑 **1. Access Control**
- ✅ **Whitelist for Telegram users** – Only approved users can interact with the bot.
- ✅ **Token-based API authentication** – Only authorized requests can access the system.

### 🤖 **2. Telegram Bot Functionality**
- 🎡 **User sends an IMEI number to the bot**.
- 🛡️ **The bot validates the IMEI**.
- 📊 **The bot returns device information**.

### 🔗 **3. API Requests**
#### 🎡 **Endpoint: `POST /api/check-imei`**
🔹 **Request Parameters:**
```json
{
  "imei": "123456789012345",
  "token": "your_auth_token"
}
```
🔹 **Response Example:**
```json
{
  "id": "QlMEbz_nPPy4JkzW",
  "type": "api",
  "status": "successful",
  "orderId": null,
  "service": {
    "id": 12,
    "title": "Mock service with only successful results"
  },
  "amount": "0.00",
  "deviceId": "860479069365109",
  "processedAt": 1738168765,
  "properties": {
    "deviceName": "iPhone 13 Pro Max 256GB Gold [A2484] [iPhone14,3]",
    "image": "https://sources.imeicheck.net/images/5f8fce1d71ce09f9c773a51568971316.png",
    "imei": "860479069365109",
    "meid": "86047906936510",
    "imei2": "566392068297521",
    "serial": "OA1TPDDDVAXAF",
    "estPurchaseDate": 1712368292,
    "additional_data": {
      "replaced": false,
      "repairCoverage": false,
      "technicalSupport": false,
      "modelDesc": "SVC IPHONE 11 PRO MAX NA 64G GRY CI/AR",
      "replacement": false,
      "refurbished": false,
      "apple/modelName": "iPhone 13 Pro Max",
      "fmiOn": false,
      "lostMode": true,
      "usaBlockStatus": "Reported stolen by AT&T MOBILITY"
    }
  }
}
```
📌 **API uses the service [imeicheck.net](https://imeicheck.net/)**.  
🛠️ **Sandbox API Token:** `e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b`  

---

## 🛠️ **How to Run the Project**
### 🔹 **1. Clone the Repository**
```bash
git clone https://github.com/arielen/test_Hatiko_tech.git
cd test_Hatiko_tech
```

### 🔹 **2. Configure Environment Variables**
Create an `.env` file based on `.env.example`:
```bash
cp .env.example .env
```
Fill in **environment variables** (PostgreSQL, Redis, API Token, etc.).

### 🔹 **3. Run with Docker**
```bash
docker-compose up --build
```
👉 **The project will start in containers**:
- `FastAPI` at `http://localhost:8000`
- `PostgreSQL` at `localhost:5432`
- `Redis` at `localhost:6379`

---

## ✅ **Testing**
### 🔹 **Run `tox` for tests and linting**
```bash
tox             # for run all tests
# tox -e lint   # for check lint and codestyle
# tox -e py313  # for run tests
```

### 🔹 **Run `pytest`**
```bash
pytest tests
```


### 🔹 **Check code quality with `ruff lint`**
```bash
ruff check .
```

---

## 📜 **Project Structure**
```
📂 imei-bot/
├── 📂 bot/                    # TG Bot
│   ├── 📂 database/             # Database models and queries
│   ├── 📂 enums/                # Enum definitions for bot settings
│   ├── 📂 handlers/             # Handlers for bot commands and callbacks
│   ├── 📂 keyboards/            # Keyboard markup configurations for bot UI
│   ├── 📂 locales/              # Localization files for multi-language support
│   ├── bot.py                   # Main bot initialization and event loop
│   ├── config.py                # Bot configuration and settings
│   ├── signals.py               # Signal handling for bot events
├── 📂 src/                    # API 
│   ├── 📂 api/                  # FastAPI endpoints
│   ├── 📂 core/                 # Configuration
│   ├── 📂 schemas/              # Pydantic schemas
│   ├── 📂 services/             # IMEI checking logic
│   ├── main.py                  # FastAPI entry point
├── 📂 tests/                  # Pytest tests
├── .env.example                  # Example environment variables
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile.api                # Dockerfile for run API
├── Dockerfile.bot                # Dockerfile for run TG Bot
├── pyproject.toml                # Configuration for ruff & pytest
├── tox.ini                       # Tox configuration
├── requirements-api.txt          # Python dependencies API
├── requirements-bot.txt          # Python dependencies TG Bot
├── requirements-test.txt         # Python dependencies for tests
├── README.md                     # Project documentation
```

---

## 📞 **Contacts**
💻 **Developer:** [arielen](https://github.com/arielen)  
📧 **Email:** pavlov_zv@mail.ru  
📧 **TG:** [1 0](https://t.me/touch_con)  
