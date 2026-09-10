# 📦 Coderr (Freelancer Developer Platform Backend)

## 📌 Description

A RESTful backend API for a freelancer developer platform, built with Python, Django, and Django REST Framework.
This project provides the core backend functionality for managing freelancers, customers, offers, and orders. 
It includes a secure authentication and authorization system, role-based permissions, API throttling, filtering, and business logic to handle interactions between users and developers.

## Features

- User authentication and authorization
- Role-based permissions for different user types
- Freelancer offers management
- Order creation and management
- Filtering and querying API data
- API throttling and request protection
- Secure REST API endpoints
- Database management with SQLite
- Automated API testing

## ⚙️ Tech Stack
- Python 3.14.0
- Django 6.0.6
- Django REST Framework 3.17.1
- SQLite 3.51.0

---

## 🚀 Quickstart Instructions

Clone the repository.

```bash
git clone <repo>
```

Copy the environment template and fill in your own values (DB, Redis, superuser, secret key).

```bash
cp .env.template .env
```

Build and start all services (Django, PostgreSQL, Redis) with Docker Compose.

```bash
docker compose -f compose.dev.yaml up --build
```

Follow the backend container logs.

```bash
docker compose -f compose.dev.yaml logs -f web
```

Stop all running containers.

```bash
docker compose -f compose.dev.yaml down
```

---

# 📡 API Overview

## 🔐 Authentication
- POST /api/registration/ → register user
- POST /api/login/ → login user + get token

---

## 👤 Profile
- GET /api/profile/{pk}/ → get profile details
- PATCH /api/profile/{pk}/ → update profile
- GET /api/profiles/business/ → list business profiles
- GET /api/profiles/customer/ → list customer profiles

---

## 📦 Offers
- GET /api/offers/ → list offers
- POST /api/offers/ → create offer
- GET /api/offers/{id}/ → get offer details
- PATCH /api/offers/{id}/ → update offer
- DELETE /api/offers/{id}/ → delete offer
- GET /api/offerdetails/{id}/ → get single offer detail item

---

## 🧾 Orders
- GET /api/orders/ → list orders
- POST /api/orders/ → create order
- PATCH /api/orders/{id}/ → update order
- DELETE /api/orders/{id}/ → delete order
- GET /api/order-count/{business_user_id}/ → count of open orders
- GET /api/completed-order-count/{business_user_id}/ → count of completed orders

---

## ⭐ Reviews
- GET /api/reviews/ → list reviews
- POST /api/reviews/ → create review
- PATCH /api/reviews/{id}/ → update review
- DELETE /api/reviews/{id}/ → delete review

---

## 🌐 Cross-cutting Endpoints
GET /api/base-info/ → aggregated base info (e.g. counts, stats)

---

# 🧪 Testing

Tests are written with Django's test framework and located under each app's `tests/` folder (e.g. `accounts_app/tests/`).

Run the full test suite inside the running backend container:

```bash
docker compose -f compose.dev.yaml exec web python manage.py test
```

Run tests for a single app:

```bash
docker compose -f compose.dev.yaml exec web python manage.py test accounts_app
```
