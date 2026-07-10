# API Specification

# BioSync AI
### REST API Specification

| Document Version | 1.0 |
|------------------|-----|
| Document Type | API Specification |
| Project | BioSync AI |
| API Style | REST |
| Data Format | JSON |
| Authentication | JWT Bearer Token |
| Prepared By | Priyansh Aggarwal |
| Last Updated | July 2026 |

---

# Table of Contents

1. Introduction
2. API Standards
3. Authentication
4. User APIs
5. Patient APIs
6. Health Metric APIs
7. Recovery APIs
8. Recommendation APIs
9. Calendar APIs
10. Error Responses
11. API Versioning

---

# 1. Introduction

BioSync AI exposes REST APIs for communication between the frontend, backend, and future third-party integrations.

All APIs return JSON responses.

Base URL

```

http://localhost:8000/api/v1

```

Production

```

https://api.biosync.ai/api/v1

```

---

# 2. API Standards

## Request Format

```

Content-Type: application/json

```

---

## Response Format

### Success

```json
{
    "success": true,
    "message": "Request Successful",
    "data": {}
}
```

---

### Error

```json
{
    "success": false,
    "message": "Validation Failed",
    "error": {}
}
```

---

# 3. Authentication

BioSync AI uses JWT Authentication.

```

Client

↓

Login

↓

JWT Token

↓

Authorization Header

↓

Protected APIs

```

Authorization Header

```

Authorization: Bearer <token>

```

---

# 4. User APIs

## Register User

### Endpoint

```

POST /auth/register

```

Request

```json
{
    "full_name":"John Doe",
    "email":"john@example.com",
    "password":"password123"
}
```

Response

```json
{
  "success": true,
  "message":"User Registered Successfully"
}
```

---

## Login

### Endpoint

```

POST /auth/login

```

Request

```json
{
    "email":"john@example.com",
    "password":"password123"
}
```

Response

```json
{
    "access_token":"JWT_TOKEN",
    "token_type":"Bearer"
}
```

---

## Get User Profile

```

GET /users/me

```

---

## Update User

```

PUT /users/me

```

---

# 5. Patient APIs

## Get Patient Profile

```

GET /patients/profile

```

---

## Update Patient Information

```

PUT /patients/profile

```

---

## Import Simulated Hospital EMR

```

POST /patients/emr/import

```

Purpose

Imports:

- Diagnoses
- Allergies
- Medications
- Lab Reports

---

# 6. Health Metric APIs

## Add Health Metric

```

POST /health/metrics

```

Request

```json
{
    "metric_type":"HEART_RATE",
    "value":72,
    "unit":"BPM",
    "source":"Wearable"
}
```

---

## Get Health Metrics

```

GET /health/metrics
```

Filters

- date
- metric_type

---

## Get Today's Health Summary

```

GET /health/summary/today

```

Returns

- Sleep
- Steps
- Calories
- Hydration
- Recovery Score

---

## Get Timeline

```

GET /health/timeline

```

Returns

Chronological patient history.

---

# 7. Recovery APIs

## Calculate Recovery Score

```

POST /recovery/calculate

```

Response

```json
{
    "score":84,
    "confidence":0.91
}
```

---

## Get Latest Recovery Score

```

GET /recovery/latest

```

---

## Get Recovery History

```

GET /recovery/history

```

---

# 8. Recommendation APIs

## Generate Recommendation

```

POST /recommendations/generate

```

Response

```json
{
  "title":"Recovery Day",
  "description":"Your recovery is below average today."
}
```

---

## Get Recommendations

```

GET /recommendations

```

---

# 9. Calendar APIs

## Connect Google Calendar

```

POST /calendar/connect

```

---

## Get Calendar Events

```

GET /calendar/events

```

---

## Generate Schedule Suggestions

```

POST /calendar/suggestions

```

Returns

- Workout Reschedule
- Hydration Reminder
- Sleep Reminder

---

# 10. Error Responses

| HTTP Code | Meaning |
|------------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Failed |
| 500 | Internal Server Error |

---

Example Error

```json
{
  "success":false,
  "message":"Heart Rate must be between 30 and 220 BPM"
}
```

---

# API Security

Protected APIs require JWT.

Protected Endpoints

- User Profile
- Patient Profile
- Health Metrics
- Recovery
- Recommendations
- Calendar

Public Endpoints

- Register
- Login

---

# API Versioning

Current Version

```

v1

```

Future

```

/api/v2

```

Version 2 may introduce

- Nutrition APIs
- Sleep Forecast APIs
- Doctor APIs
- Caregiver APIs

---

# API Summary

| Module | Endpoints |
|---------|-----------|
| Authentication | 2 |
| User | 2 |
| Patient | 3 |
| Health | 4 |
| Recovery | 3 |
| Recommendation | 2 |
| Calendar | 3 |

**Total Planned REST APIs (Version 1): ~19**