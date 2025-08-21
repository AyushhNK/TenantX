# TenantX — Multi-Tenant SaaS Starter Kit

TenantX is a **production-ready Django + DRF starter kit** for building multi-tenant, subscription-based SaaS platforms. It ships with authentication, organizations, role-based access, billing via Stripe, async jobs with Celery/Redis, and analytics endpoints.

---

## 🚀 Features

* **User Authentication** — JWT + refresh tokens (via SimpleJWT)
* **Multi-Tenancy** — Organizations with multiple users
* **Role-Based Access** — Admin, Manager, Employee roles
* **Billing Integration** — Stripe Checkout + Webhooks (subscriptions)
* **Tenant Isolation** — Row-level filtering (schema-based possible via django-tenants)
* **Analytics Dashboard** — Sample endpoints for charts & reports
* **Async Processing** — Celery + Redis for background tasks
* **PostgreSQL** — Production-ready relational database

---

## 📂 Project Structure

```
tenantx/
├─ manage.py
├─ tenantx/             # project settings
├─ core/                # tenancy utilities, middleware, permissions
├─ accounts/            # users, auth, orgs, roles
├─ billing/             # Stripe integration
├─ dashboard/           # analytics endpoints
└─ worker/              # Celery tasks
```

---

## 🛠️ Tech Stack

* **Backend:** Django 5 + Django REST Framework
* **Auth:** djangorestframework-simplejwt (JWT & refresh)
* **Database:** PostgreSQL 16+
* **Cache/Broker:** Redis 7+
* **Async Jobs:** Celery 5
* **Payments:** Stripe API (Checkout & Webhooks)
* **Containerization:** Docker + docker-compose

---

## ⚙️ Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/yourusername/tenantx.git
cd tenantx
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```env
SECRET_KEY=change-me
DEBUG=1
DB_NAME=tenantx
DB_USER=tenantx
DB_PASSWORD=tenantx
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
STRIPE_API_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

### 3. Run with Docker

```bash
docker-compose up -d
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 📊 Roadmap

* [ ] Add support for `django-tenants` (schema-based multitenancy)
* [ ] Add PayPal integration
* [ ] Deploy templates for AWS/GCP/Azure
* [ ] Frontend dashboard with React or Next.js

---

## 📜 License

MIT © 2025 TenantX
