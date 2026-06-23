# CodeVector Take Home Assignment

A backend service that allows browsing ~200,000 products with filtering and fast pagination while handling changing data efficiently.

## Tech Stack

- Python
- FastAPI
- MySQL
- SQLAlchemy
- Faker (data generation)

Bonus:

- HTML + JavaScript frontend

---

# Features

- Generate and store 200,000 products
- Browse products ordered by newest first
- Filter products by category
- Fast cursor-based pagination
- Bonus lightweight frontend

---

# Project Structure

```text
Codeverse/

app/
├── database.py
├── main.py
├── models.py
└── routes.py

scripts/
└── seed.py

frontend/
└── index.html

requirements.txt
README.md
```

---

# Database Schema

Products table:

| Column | Type |
|--------|------|
| id | CHAR(36) |
| name | VARCHAR(255) |
| category | VARCHAR(100) |
| price | DECIMAL(10,2) |
| created_at | DATETIME |
| updated_at | DATETIME |

Indexes:

```sql
CREATE INDEX idx_updated_id
ON products(updated_at DESC,id DESC);

CREATE INDEX idx_category_updated_id
ON products(category,updated_at DESC,id DESC);
```

These indexes optimize sorting and filtering queries.

---

# Why Cursor Pagination?

I intentionally used cursor-based pagination instead of OFFSET pagination.

Problems with OFFSET:

- Performance degrades as data grows
- Database scans skipped rows repeatedly
- Can lead to duplicate or missing products when data changes while users are browsing

Cursor pagination solves this by using:

```text
updated_at DESC
id DESC
```

Cursor values:

```text
cursor_updated_at
cursor_id
```

This makes pagination more scalable and stable.

---

# API Endpoints

## Home

```http
GET /
```

Response:

```json
{
  "message":"CodeVector Backend Running"
}
```

---

## Browse Products

```http
GET /products
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| limit | int | Number of products per page |
| category | string | Filter by category |
| cursor_updated_at | string | Pagination cursor |
| cursor_id | string | Pagination cursor |

Examples:

Get first page:

```http
/products
```

Filter by category:

```http
/ products?category=electronics
```

Paginate:

```http
/ products?limit=20&cursor_updated_at=...&cursor_id=...
```

---

# Data Generation

The application includes a seed script that generates 200,000 products.

Generation strategy:

- Batch inserts
- Faker generated data
- Randomized timestamps
- UUID primary keys

Run:

```bash
python -m scripts.seed
```

---

# Running Locally

## 1. Clone repository

```bash
git clone <repo-url>

cd Codeverse
```

## 2. Create virtual environment

```bash
python3 -m venv venv

source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure MySQL

Create database:

```sql
CREATE DATABASE codevector;
```

Update database connection inside:

```text
app/database.py
```

## 5. Start backend

```bash
python -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

## 6. Seed data

```bash
python -m scripts.seed
```

## 7. Run frontend (Bonus)

```bash
python3 -m http.server 5500
```

Frontend:

```text
http://localhost:5500/frontend/index.html
```

---

# Technical Decisions

- Used FastAPI for simplicity and speed.
- Used SQLAlchemy ORM.
- Used MySQL indexing for efficient querying.
- Used batch inserts while seeding.
- Used cursor pagination instead of OFFSET pagination.

---

# Improvements With More Time

I would improve the project by:

1. Implementing session/snapshot-based pagination to fully guarantee consistent browsing while products are updated concurrently.

2. Moving secrets into environment variables.

3. Dockerizing the application.

4. Adding automated tests.

5. Adding deployment configuration.

---

# AI Usage

AI was used as a productivity tool to:

- Generate FastAPI boilerplate
- Discuss pagination approaches
- Debug environment setup issues
- Speed up implementation

All generated code was manually reviewed, understood, modified and integrated.
