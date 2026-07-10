# Low Level Design (LLD)

# BioSync AI
### An Intelligent Health Operating System for Personalized Recovery & Daily Planning

| Document Version | 1.0 |
|------------------|-----|
| Document Type | Low Level Design (LLD) |
| Project | BioSync AI |
| Prepared By | Priyansh Aggarwal |
| Status | Draft |
| Last Updated | July 2026 |

---

# Table of Contents

1. Introduction
2. Design Principles
3. Project Structure
4. Module Design
5. Request Flow
6. Authentication Flow
7. Health Data Flow
8. AI Processing Flow
9. Class Responsibilities
10. Design Patterns
11. Error Handling
12. Logging Strategy
13. Future Improvements

---

# 1. Introduction

This document describes the implementation-level architecture of BioSync AI.

It defines:

- Folder Structure
- Internal Modules
- Component Responsibilities
- API Flow
- Data Processing Pipeline
- Class Design
- Communication Between Components

Unlike the HLD, this document focuses on implementation details.

---

# 2. Design Principles

The implementation follows these principles:

- SOLID Principles
- Clean Architecture
- Domain Driven Design (DDD)
- Separation of Concerns
- Dependency Injection
- API First Design

---

# 3. Project Structure

```text
biosync-ai/

│

├── backend/
│
│   ├── app/
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── health.py
│   │   ├── recovery.py
│   │   ├── recommendations.py
│   │   ├── calendar.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── constants.py
│   │
│   ├── database/
│   │   ├── session.py
│   │   ├── base.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── health_metric.py
│   │   ├── recovery.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── metric.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── health_service.py
│   │   ├── recovery_service.py
│   │   ├── calendar_service.py
│   │
│   ├── ai/
│   │   ├── llm_engine.py
│   │   ├── prompt_builder.py
│   │   ├── recommendation_engine.py
│   │
│   ├── ingestion/
│   │   ├── emr.py
│   │   ├── manual.py
│   │   ├── wearable.py
│   │
│   ├── normalization/
│   │   ├── normalizer.py
│   │
│   ├── validation/
│   │   ├── validator.py
│   │
│   ├── feature_engineering/
│   │   ├── recovery_features.py
│   │
│   └── main.py
│
├── frontend/
│
├── docs/
│
└── docker/
```

---

# 4. Module Design

## Authentication Module

Responsibilities

- Registration
- Login
- JWT Generation
- Password Hashing

Input

User Credentials

Output

JWT Token

---

## User Module

Responsibilities

- User Profile
- Preferences
- Account Management

---

## Patient Module

Responsibilities

- Hospital Profile
- Medical History
- Diagnoses
- Allergies
- Medications

---

## Health Module

Responsibilities

- Health Metrics
- Timeline
- Health Summary

---

## Ingestion Module

Responsibilities

Collect data from

- Wearables
- Hospital EMR
- Manual Input

---

## Normalization Module

Responsibilities

Convert

Different Provider Formats

↓

Unified Internal Format

---

## Validation Module

Responsibilities

Validate incoming values

Example

Heart Rate

30–220 BPM

Hydration

0–20 Litres

Sleep

0–24 Hours

---

## Feature Engineering Module

Responsibilities

Generate

Sleep Debt

Weekly Average

Recovery Indicators

Hydration Trend

---

## Recovery Module

Responsibilities

Compute

Recovery Score

---

## Recommendation Module

Responsibilities

Generate

Structured Recommendations

Example

```json
{
  "action":"MOVE_WORKOUT",
  "reason":"Low Recovery"
}
```

---

## AI Module

Responsibilities

Generate natural language explanations

Input

Structured Recommendation

Output

Human-readable explanation

---

## Calendar Module

Responsibilities

Read Calendar

Generate Suggestions

Create Events

---

# 5. Request Flow

```text
Client

↓

FastAPI

↓

API Router

↓

Service Layer

↓

Database

↓

Response
```

---

# 6. Authentication Flow

```text
User

↓

Login API

↓

Auth Service

↓

Verify Password

↓

Generate JWT

↓

Return Token
```

---

# 7. Health Data Flow

```text
Wearable

↓

EMR

↓

Manual Entry

↓

Ingestion Layer

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
```

---

# 8. AI Processing Flow

```text
Recovery Score

↓

Decision Engine

↓

Prompt Builder

↓

LLM

↓

Recommendation

↓

Dashboard
```

---

# 9. Class Responsibilities

## User

Stores user information

Fields

- id
- email
- password
- created_at

---

## Patient

Stores medical profile

Fields

- blood_group
- allergies
- medications

---

## HealthMetric

Stores every metric

Fields

- metric_type
- value
- unit
- timestamp

---

## Recovery

Stores calculated recovery

Fields

- score
- confidence
- calculated_at

---

## Recommendation

Stores recommendations

Fields

- action
- title
- description
- priority

---

# 10. Design Patterns

The project uses

Repository Pattern

```
Service

↓

Repository

↓

Database
```

---

Dependency Injection

FastAPI Depends()

---

Factory Pattern

Metric Factory

Different metrics

↓

Same interface

---

Strategy Pattern

Recovery Algorithms

↓

Easy future replacement

---

Builder Pattern

LLM Prompt Builder

---

# 11. Error Handling

All APIs return

```json
{
  "success": false,
  "message": "...",
  "error_code": "..."
}
```

Common HTTP Codes

200

400

401

403

404

409

422

500

---

# 12. Logging Strategy

Log

Authentication

API Requests

Database Errors

Validation Errors

LLM Requests

Calendar Requests

Future

Centralized Logging

ELK Stack

---

# 13. Future Improvements

The architecture supports future extraction into microservices.

Candidate Services

- AI Service
- Notification Service
- Calendar Service
- Analytics Service
- EMR Integration Service

Current architecture remains a Modular Monolith for simplicity and maintainability.

---

# LLD Summary

The Low Level Design defines the internal implementation blueprint of BioSync AI.

The project follows Clean Architecture, Domain Driven Design, and modular service separation to ensure maintainability, scalability, and readiness for future AI enhancements.