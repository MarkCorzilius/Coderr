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

- Clone the repository
```bash
git clone <your-repo-url>
```

- Create a virtual environment:
```bash
python -m venv venv
```

- Activate Virtual Environment:
Windows:
```bash
venv\Scripts\activate
```
Mac:
```bash
source venv/bin/activate
```

- Install Dependencies:
```bash
pip install -r requirements.txt
```

- Run Database Migrations:
```bash
python manage.py migrate
```

- Create Superuser:
```bash
python manage.py createsuperuser
```

- Run Server:
```bash
python manage.py runserver
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

- Run Integration tests using command ```python manage.py test```
or
- Use Postman to test API
- Register or login first
- Copy token from login response

```bash
Authorization: Token <your_token>
```
