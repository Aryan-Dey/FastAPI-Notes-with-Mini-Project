# FastAPI Patient Management + ML Prediction API (End-to-End)

A production-style **FastAPI project** that demonstrates strong backend fundamentals by building:
1) a **Patient Management System (CRUD API)** using FastAPI + Pydantic + JSON-based persistence, and  
2) a blueprint for serving a **Machine Learning prediction model** via a `/predict` API, optionally consumed by a lightweight **Streamlit frontend**.

This repo is designed to showcase **backend + API design skills** expected from fresher/junior roles, including clean validation, structured responses, proper HTTP status codes, and error handling.

---

## Why this project?

Recruiters often want to see:
- You can build real APIs (not just write code snippets)
- You understand REST principles, validation, error handling, status codes
- You can structure a project cleanly and write maintainable code
- You can extend a backend to support ML inference and frontend consumption

This project is built to demonstrate exactly that.

---

## Key Features

### ✅ Patient Management CRUD API
- Create a patient record (`POST /create`)
- View patients (single & list endpoints)
- Update patient partially (`PUT /edit/{patient_id}`) using **optional request body fields**
- Delete a patient (`DELETE /delete/{patient_id}`)
- Sort patients using **query parameters** (`GET /sort?sort_by=...&order=...`)

### ✅ Strong API Validation & Error Handling
- Input validation using **Pydantic models**
- Proper errors using **HTTPException**
- Correct status codes (e.g., `201 Created`, `404 Not Found`, `400 Bad Request`)

### ✅ Computed Fields (BMI + Verdict) handled correctly
- BMI and verdict are treated as derived fields, automatically re-computed after update
- Update flow ensures computed values stay consistent after partial updates

### ✅ API Readability Improvements
- Home endpoint (`GET /`) for human-readable confirmation
- Health check endpoint (`GET /health`) for machine-readable monitoring readiness
- Response models (for complex outputs like ML predictions)

### ✅ ML Inference API Blueprint (End-to-End Thinking)
- Designed flow for:
  - raw inputs → validation → feature engineering → model prediction → structured JSON response
- Typical industry approach: **POST** for inference because the client sends data to be processed

---

## Tech Stack

- **Python**
- **FastAPI**
- **Pydantic**
- **Uvicorn** (ASGI server)
- (Optional) **Streamlit** (Frontend consumer)
- JSON file used as a lightweight DB for the CRUD module

---




