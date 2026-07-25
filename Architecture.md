<div align="center">

# 🧭 Factify Enterprise Architecture

### How the Enterprise gateway and Factify Core work together

</div>

---

## 📖 Overview

**Factify Enterprise** is the enterprise-facing gateway of the Factify platform.

Its primary responsibility is to provide a **secure, scalable, and maintainable API** for enterprise customers — while delegating all AI verification logic to **Factify Core**.

> 🧩 This separation lets both systems evolve independently, without duplicating business logic.

---

## 📚 Table of Contents

- [System Architecture](#-system-architecture)
- [Why Two Services?](#-why-two-services)
- [Verification Flow](#-verification-flow)
- [Authentication Flow](#-authentication-flow)
- [API Key Lifecycle](#-api-key-lifecycle)
- [Usage Tracking](#-usage-tracking)
- [Dependency Injection](#-dependency-injection)
- [Repository Pattern](#-repository-pattern)
- [Unit of Work Pattern](#-unit-of-work-pattern)
- [Service Layer](#-service-layer)
- [External Services](#-external-services)
- [Design Principles](#-design-principles)
- [Future Improvements](#-future-improvements)

---

## 🏗️ System Architecture

```
                    Enterprise Client
               (Website / Mobile / API)

                           │
                    HTTPS + API Key
                           │
                           ▼

               ┌────────────────────────┐
               │ Factify Enterprise API │
               │      FastAPI           │
               └────────────────────────┘

                           │

      ┌───────────────────────────────────────┐
      │ Enterprise Responsibilities           │
      │                                       │
      │ • Authentication                      │
      │ • API Key Validation                  │
      │ • Organization Management             │
      │ • Monthly Usage Limits                │
      │ • Usage Logging                       │
      │ • API Gateway                         │
      │ • Health Monitoring                   │
      └───────────────────────────────────────┘

                           │
                    HTTP (REST)

                           ▼

              ┌──────────────────────┐
              │    Factify Core      │
              │      Next.js         │
              └──────────────────────┘

                           │

        ┌─────────────────────────────────────┐
        │ Verification Responsibilities       │
        │                                     │
        │ • Evidence Gathering                │
        │ • Google Gemini                     │
        │ • OpenAI Fallback                   │
        │ • Rule-Based Verification           │
        │ • Verification Reports              │
        └─────────────────────────────────────┘

                           │

                           ▼

                 Verification Report

                           │

                           ▼

                 Enterprise Client
```

---

## 🤔 Why Two Services?

Factify follows a **service-oriented architecture**. Instead of combining enterprise concerns with AI verification logic, responsibilities are split across two independent services.

<table>
<tr>
<td width="50%" valign="top">

### 🏢 Factify Enterprise
*Everything related to customers*

- 🔐 Authentication
- 🏬 Organizations
- 🔑 API Keys
- 📊 Usage Tracking
- 💳 Billing Data
- 🚦 Monthly Limits
- 🌐 Enterprise APIs

> ⛔ Never performs AI verification.

</td>
<td width="50%" valign="top">

### 🤖 Factify Core
*Everything related to fact-checking*

- 🔎 Search
- 📑 Evidence Gathering
- ✨ Gemini
- 🔁 OpenAI
- ✍️ Prompt Engineering
- 📐 Rule-Based Analysis
- 📄 Report Generation

> ⛔ Knows nothing about API keys or organizations.

</td>
</tr>
</table>

---

## 🔄 Verification Flow

```
Enterprise Client
        │
POST /verify
        │
Authenticate API Key
        │
Locate Organization
        │
Check Monthly Usage
        │
Verification Service
        │
FactifyClient
        │
POST Factify Core
        │
verifyClaim()
        │
Evidence Gathering
        │
Gemini
        │
OpenAI Fallback
        │
Rule-Based Verification
        │
Verification Report
        │
Factify Enterprise
        │
Log Request
        │
Return Response
```

---

## 🔐 Authentication Flow

```
Client
        │
X-API-Key
        │
SHA-256 Hash
        │
Database Lookup
        │
Active?
 ┌───────────────┐
 │               │
No             Yes
 │               │
401         Continue
                │
Organization
                │
Verification
```

---

## 🗝️ API Key Lifecycle

```
Organization
        │
Create API Key
        │
Generate Secure Key
        │
Hash Key
        │
Store Hash
        │
Return Plain Key Once
        │
Client Stores Key
        │
Every Request
        │
Hash Incoming Key
        │
Compare Hash
        │
Authenticate
```

> ⚠️ The plaintext key is shown **exactly once**, at creation. Only its hash is ever persisted.

---

## 📊 Usage Tracking

```
Incoming Request
        │
Authenticate
        │
Find Organization
        │
Count Monthly Usage
        │
Exceeded?
 ┌───────────────┐
 │               │
Yes             No
 │               │
429        Continue
                │
Forward Request
                │
Verification
                │
Log Request
                │
Update API Key Last Used
                │
Return Response
```

---

## 🧩 Dependency Injection

The project uses FastAPI's built-in dependency injection system to keep route handlers thin.

```
API Route
        │
Depends()
        │
Service
        │
Unit Of Work
        │
Repository
        │
SQLAlchemy
        │
PostgreSQL
```

This keeps route handlers thin while centralizing business logic within the service layer.

---

## 📦 Repository Pattern

Repositories encapsulate **all** database operations.

```
Route
        │
Service
        │
Repository
        │
Database
```

**Benefits:**

- ✅ Separation of concerns
- ✅ Easier testing
- ✅ Cleaner business logic
- ✅ Centralized database access

---

## 🔄 Unit of Work Pattern

A Unit of Work coordinates multiple repository operations inside a single transaction.

**Example:**

```
Verification Request
        │
Log Usage
        │
Update API Key
        │
Commit Transaction
```

> ↩️ If any operation fails, the entire transaction is rolled back.

---

## 🛠️ Service Layer

Business logic resides inside services. Current services include:

| Service | Responsibility |
|---|---|
| `ApiKeyService` | API key creation, validation, lifecycle |
| `UsageService` | Usage tracking & monthly limit enforcement |
| `VerificationService` | Orchestrates calls to Factify Core |

> 📏 **Rule of thumb:** Services never contain HTTP-specific code. Routes never contain business logic.

---

## 🔌 External Services

### 🐘 PostgreSQL (Neon)

Stores:

- Organizations
- API Keys
- Usage Logs

### 🤖 Factify Core

Provides:

- Verification Engine
- AI Analysis
- Report Generation

---

## 🧠 Design Principles

The architecture follows several core software engineering principles.

**Single Responsibility Principle**
Each layer has one responsibility — routes receive requests, services execute business logic, repositories access data, and Factify Core performs verification.

**Separation of Concerns**
Enterprise concerns are isolated from AI concerns, allowing both services to evolve independently.

**Dependency Inversion**
Routes depend on abstractions (services), not implementations — making the application easier to test and maintain.

**Scalability**
Because Enterprise and Core are separate services:

- 📈 Enterprise can scale independently
- 📈 Factify Core can scale independently
- 🔄 AI providers can change without affecting Enterprise clients

---

## 🔮 Future Improvements

- [ ] ⚡ Redis caching
- [ ] 🧵 Background verification jobs
- [ ] 🔔 Webhooks
- [ ] 📊 API analytics dashboard
- [ ] 💳 Billing integration
- [ ] 👥 Team workspaces
- [ ] 🔐 OAuth authentication
- [ ] 📦 SDKs for Python, JavaScript, and C#