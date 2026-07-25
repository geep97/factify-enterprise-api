<div align="center">

# 🛰️ Factify Enterprise API

### Enterprise-grade API Gateway for the Factify AI Fact-Checking Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-6BA539?style=for-the-badge&logo=openapiinitiative&logoColor=white)](https://swagger.io/specification/)

[![Version](https://img.shields.io/badge/version-v1.0.0-blueviolet?style=flat-square)](#-version)
[![License](https://img.shields.io/badge/license-Proprietary-lightgrey?style=flat-square)](#-license)
[![Status](https://img.shields.io/badge/status-production-success?style=flat-square)](#)

</div>

---

## ✨ Overview

**Factify Enterprise** is the enterprise gateway into the Factify ecosystem — secure, scalable, authenticated REST access to Factify's AI-powered verification engine.

While **Factify Core** handles the heavy lifting of evidence gathering and AI-driven verification, **Factify Enterprise** is purpose-built for the concerns that come with running fact-checking at scale:

| 🔑 Auth | 🏢 Orgs | 📊 Usage | 🚦 Limits | 📖 Docs | ❤️ Health |
|:---:|:---:|:---:|:---:|:---:|:---:|
| API Keys | Multi-tenant | Tracking | Monthly caps | OpenAPI/Swagger | Live monitoring |

The Enterprise API talks to **Factify Core**, which performs:

- 🔍 Evidence gathering
- 🤖 Google Gemini verification
- 🔁 OpenAI fallback
- 📐 Rule-based verification
- 📄 Report generation

---

## 🏗️ Architecture

```
                   Enterprise Client
                          │
                   X-API-Key Header
                          │
                          ▼
              ╔═══════════════════════╗
              ║  Factify Enterprise   ║
              ║   (FastAPI Gateway)   ║
              ╠═══════════════════════╣
              ║  • Authentication     ║
              ║  • Organizations      ║
              ║  • API Keys           ║
              ║  • Monthly Limits     ║
              ║  • Usage Tracking     ║
              ║  • Verification GW    ║
              ╚═══════════════════════╝
                          │
                        HTTP
                          │
                          ▼
              ╔═══════════════════════╗
              ║      Factify Core     ║
              ║    (Next.js Service)  ║
              ╠═══════════════════════╣
              ║  • Evidence Gathering ║
              ║  • Google Gemini      ║
              ║  • OpenAI Fallback    ║
              ║  • Rule-based Verify  ║
              ╚═══════════════════════╝
                          │
                          ▼
                Verification Report
                          │
                          ▼
                   Enterprise Client
```

---

## 🚀 Features

### Enterprise-Grade

- 🔐 **API Key Authentication**
- 🏢 **Organization Support** — multiple keys per org
- 📈 **Monthly Usage Limits** & analytics
- 🌉 **Verification Gateway** to Factify Core
- 🧩 **Dependency Injection**
- 📦 **Repository Pattern**
- 🔄 **Unit of Work Pattern**
- 🗄️ **SQLAlchemy ORM**
- 🧬 **Alembic Migrations**
- ⚠️ **Structured Exception Handling**
- 📘 **OpenAPI / Swagger Docs**

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI |
| **Database** | PostgreSQL (Neon) |
| **ORM** | SQLAlchemy |
| **Validation** | Pydantic |
| **HTTP Client** | httpx |
| **Migrations** | Alembic |
| **Auth** | API Keys |
| **Docs** | Swagger / OpenAPI |
| **Verification Engine** | Factify Core |

---

## 📂 Project Structure

```
app
├── api/            # Route handlers
├── auth/           # API key & auth logic
├── clients/        # External service clients (Factify Core)
├── core/           # Config, settings, constants
├── db/             # Database session & models
├── middleware/      # Request/response middleware
├── repositories/    # Data access layer
├── schemas/         # Pydantic request/response models
├── services/         # Business logic
├── unit_of_work/     # Transaction boundaries
├── rate_limit/        # Usage & rate limiting
└── main.py             # App entrypoint
```

---

## 📡 API Endpoints

### ❤️ Health

```http
GET /api/v1/health/live
GET /api/v1/health/db
GET /api/v1/health/tables
GET /api/v1/health/ready
```

### 🔑 API Keys

```http
POST /api/v1/api-keys
GET  /api/v1/api-keys
POST /api/v1/api-keys/additional
GET  /api/v1/api-keys/test
```

### ✅ Verification

```http
POST /api/v1/verify
```

### 🔒 Protected

```http
GET /api/v1/protected/me
```

### 🚦 Rate Limits

```http
GET /api/v1/rate-limits/me
```

---

## 🔐 Authentication

All protected endpoints require an API key sent via header:

```http
X-API-Key: factify_xxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🧪 Example Request

```http
POST /api/v1/verify
X-API-Key: factify_xxxxxxxxx
Content-Type: application/json
```

```json
{
    "content": "NASA confirms humans will live on Mars permanently by 2027.",
    "mode": "headline"
}
```

## 📬 Example Response

```json
{
  "id": "...",
  "claim": "...",
  "summary": "...",
  "verdict": "False",
  "confidence": 94,
  "riskLevel": "High",
  "sourceCredibility": 82,
  "evidenceStrength": 91,
  "recommendations": [],
  "sources": []
}
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=

FACTIFY_CORE_API_URL=

API_KEY_PREFIX=factify_

ENVIRONMENT=production
```

---

## 🖥️ Running Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run database migrations
alembic upgrade head

# 3. Start the API
uvicorn app.main:app --reload
```

Then explore the interactive docs:

| Docs | URL |
|---|---|
| 📘 Swagger UI | `http://localhost:8000/docs` |
| 🧾 OpenAPI Spec | `http://localhost:8000/openapi.json` |

---

## ☁️ Deployment

Deploy anywhere that runs Python + FastAPI:

`Railway` · `Render` · `Azure App Service` · `DigitalOcean` · `AWS` · `Google Cloud Run`

The only required production configuration is updating:

```env
FACTIFY_CORE_API_URL=https://your-factify-core-url
```

---

## 🏷️ Version

<div align="center">

**v1.0.0**

</div>

---

## 📄 License

<div align="center">

© Factify. All rights reserved.

</div>