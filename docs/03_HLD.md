# High Level Design (HLD)

# BioSync AI
### An Intelligent Health Operating System for Personalized Recovery & Daily Planning

| Document Version | 1.0 |
|------------------|-----|
| Document Type | High Level Design |
| Project | BioSync AI |
| Prepared By | Priyansh Aggarwal |
| Status | Draft |
| Last Updated | July 2026 |

---

# Table of Contents

1. Introduction
2. Design Goals
3. System Overview
4. Architectural Principles
5. High-Level Architecture
6. Component Design
7. Module Responsibilities
8. Data Flow
9. Deployment Architecture
10. Technology Decisions
11. Scalability Strategy
12. Security Architecture
13. Future Architecture
14. Conclusion

---

# 1. Introduction

The High Level Design (HLD) document describes the overall architecture of BioSync AI.

It explains:

- System Components
- Component Interaction
- Major Modules
- Data Flow
- Deployment Strategy
- Scalability

This document intentionally avoids implementation-level details.

---

# 2. Design Goals

The system has been designed with the following goals:

- Scalability
- Maintainability
- Security
- Modularity
- Extensibility
- High Performance
- AI Readiness

---

# 3. System Overview

BioSync AI is a modular AI-powered healthcare platform.

The platform collects health information from multiple sources before generating personalized recovery recommendations.

The architecture follows a layered approach.

```

                    User
                     │
                     ▼
              React Frontend
                     │
                     ▼
             FastAPI Backend
                     │
                     ▼
         Health Intelligence Layer
                     │
                     ▼
              PostgreSQL Database
                     │
                     ▼
             AI Recommendation Layer

```

---

# 4. Architectural Principles

The system follows the following principles.

## Separation of Concerns

Every module has one responsibility.

Examples

Authentication

Health Data

Recovery Engine

AI

Calendar

---

## Loose Coupling

Modules communicate through service interfaces.

No module directly accesses another module's database.

---

## High Cohesion

Related functionality remains inside the same module.

---

## API First Design

Every feature is exposed through REST APIs.

The frontend never communicates directly with the database.

---

## AI as a Service

The LLM is isolated from the business logic.

Business logic determines **what** recommendation should be generated.

The LLM determines **how** it should be explained.

---

# 5. High-Level Architecture

```text
                                   USER
                                     │
                                     ▼
                            React Frontend
                                     │
                                     ▼
                             FastAPI Backend
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        ▼                            ▼                            ▼
 Authentication              Health Service               Calendar Service
        │                            │                            │
        │                            ▼                            │
        │                   Data Ingestion Layer                  │
        │                            │                            │
        │      ┌─────────────────────┼─────────────────────┐      │
        │      ▼                     ▼                     ▼      │
        │ Hospital EMR       Wearable APIs        Manual Input    │
        │      │                     │                     │      │
        │      └─────────────────────┼─────────────────────┘      │
        │                            ▼                            │
        │                  Data Normalization                     │
        │                            ▼                            │
        │                   Validation Engine                    │
        │                            ▼                            │
        │                 PostgreSQL + TimescaleDB               │
        │                            ▼                            │
        │                  Feature Engineering                   │
        │                            ▼                            │
        └────────────────────────────┼────────────────────────────┘
                                     ▼
                          Recovery Score Engine
                                     ▼
                             Decision Engine
                                     ▼
                             LLM Health Coach
                                     │
             ┌───────────────────────┼────────────────────────┐
             ▼                       ▼                        ▼
      Recovery Score       AI Recommendations      Calendar Suggestions
```

---

# 6. Component Design

The platform consists of the following major components.

## Frontend

Responsibilities

- User Interface
- Dashboard
- Charts
- Authentication Screens
- Calendar View

Technology

- React
- TypeScript
- Tailwind CSS

---

## Backend API

Responsibilities

- REST APIs
- Authentication
- Request Validation
- Business Logic

Technology

- FastAPI

---

## Authentication Service

Responsibilities

- User Registration
- Login
- JWT Token Generation
- Password Hashing

---

## Health Service

Responsibilities

- Health Metric Storage
- Timeline Generation
- User Health Summary

---

## Data Ingestion Layer

Responsibilities

- Hospital Import
- Wearable Import
- Manual Entry

---

## Data Normalization

Responsibilities

Convert all incoming data into a unified internal schema.

---

## Validation Engine

Responsibilities

Validate every incoming record.

Example

Heart Rate

30–220 BPM

Sleep

0–24 Hours

Hydration

0–20 Litres

---

## Database

Responsibilities

Persistent storage.

Technology

- PostgreSQL
- TimescaleDB

---

## Feature Engineering

Responsibilities

Generate derived features.

Examples

- Weekly Sleep Average
- Sleep Debt
- Recovery Indicators
- Hydration Trend

---

## Recovery Engine

Responsibilities

Compute Recovery Score.

Inputs

- Sleep
- Activity
- Heart Rate
- Hydration

Output

Recovery Score

---

## Decision Engine

Responsibilities

Determine recommendations.

Examples

Low Recovery

↓

Recommend Recovery Day

High Stress

↓

Recommend Meditation

---

## LLM Health Coach

Responsibilities

Transform structured decisions into natural language.

Example

Recovery Score = 42

↓

"You slept below your weekly average and your activity level was high yesterday. Consider light exercise today."

---

# 7. Module Responsibilities

| Module | Responsibility |
|---------|---------------|
| Authentication | Identity Management |
| Health Service | Health Data Management |
| Timeline Engine | Chronological Health History |
| Recovery Engine | Health Score Calculation |
| AI Engine | Recommendation Generation |
| Calendar | Schedule Suggestions |

---

# 8. Data Flow

```
User

↓

Login

↓

Authentication

↓

Import Health Data

↓

Normalization

↓

Validation

↓

Database

↓

Feature Engineering

↓

Recovery Engine

↓

Decision Engine

↓

LLM

↓

Dashboard
```

---

# 9. Deployment Architecture

```
                 Browser
                    │
                    ▼
             React Frontend
                    │
              HTTPS / REST
                    │
                    ▼
             FastAPI Backend
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
 PostgreSQL            Ollama (LLM)
         │
         ▼
   TimescaleDB
```

Future Deployment

```
Frontend

↓

Nginx

↓

FastAPI

↓

Redis

↓

PostgreSQL

↓

AI Server
```

---

# 10. Technology Decisions

| Layer | Technology |
|--------|------------|
| Frontend | React |
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Database | PostgreSQL |
| Time Series | TimescaleDB |
| AI | Ollama |
| LLM | Llama 3 |
| Authentication | JWT |
| Deployment | Docker |

---

# 11. Scalability Strategy

Current Architecture

Modular Monolith

Reasons

- Easier development
- Faster debugging
- Simpler deployment

Future

Selected modules can be extracted into microservices.

Examples

- AI Service
- Notification Service
- Calendar Service

---

# 12. Security Architecture

Authentication

JWT

Password Hashing

bcrypt

Communication

HTTPS

Data Protection

Encrypted Tokens

Future

OAuth

Role Based Access

Audit Logging

---

# 13. Future Architecture

Version 2

- Nutrition Engine
- Sleep Prediction
- Weekly Reports

Version 3

- Doctor Dashboard
- Remote Monitoring
- Caregiver Portal

Version 4

- Predictive Healthcare
- Hospital Integration
- Smart Patient Matching
- Home Healthcare Logistics

---

# 14. Conclusion

The architecture of BioSync AI has been designed to support long-term scalability while keeping Version 1 intentionally simple.

The modular monolith architecture enables rapid development while maintaining clear boundaries between system components.

The platform is prepared for future AI-driven healthcare capabilities without requiring major architectural changes.=