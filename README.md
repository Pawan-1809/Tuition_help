# Tuition Connect

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Poppins&weight=700&size=28&pause=1200&color=1D9BF0&center=true&vCenter=true&width=900&lines=Tutor+Discovery+Platform+Built+With+Django;Role-Based+Onboarding+%2B+Payments+%2B+Chat;Production-Ready+Deployments+With+Seeded+Demo+Data" alt="Typing banner" />
</div>

<div align="center">
  <img src="https://img.shields.io/badge/Django-5.1-0d3b2e?style=for-the-badge&logo=django&logoColor=white" alt="Django 5.1" />
  <img src="https://img.shields.io/badge/Channels-WebSockets-1b4965?style=for-the-badge&logo=django&logoColor=white" alt="Channels" />
  <img src="https://img.shields.io/badge/PostgreSQL-Production-264653?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/SQLite-Development-4c956c?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Razorpay-Integrated-2457f5?style=for-the-badge" alt="Razorpay" />
</div>

<p align="center">
  <b>Tuition Connect</b> is a full-stack Django marketplace for connecting students and parents with tutors through rich tutor profiles, onboarding, filtering, payments, and chat.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active%20Development-0f766e?style=flat-square" alt="Status" />
  <img src="https://img.shields.io/badge/Demo%20Seed-Kolkata%20Tutors-f59e0b?style=flat-square" alt="Demo seed" />
  <img src="https://img.shields.io/badge/Deploy-Render%20Ready-7c3aed?style=flat-square" alt="Deploy ready" />
</p>

---

## Snapshot

```text
Students/Parents -> Search tutors -> Filter -> View profile -> Chat / Connect
Tutors -> Register -> Complete onboarding -> Pay when transactions are enabled -> Go live
Admins -> Track users, tutor activity, and payment metrics
```

## Note

> Transactions are temporarily paused in the current setup.
> Tutors can complete registration without payment while the payment gate is paused.
> If transactions are activated again, tutors will only be able to register and go live after successful payment.

## Highlights

- Modular Django monolith with focused apps for `accounts`, `tutors`, `payments`, `dashboard`, and `chat`
- Custom user model with tutor, parent/student, and admin roles
- Multi-step tutor onboarding with profile details, subjects, languages, pricing, and location
- Tutor directory with filtering by subject, language, grade level, teaching method, experience, and price
- Razorpay payment flow for tutor registration fees
- Real-time chat foundation powered by Django Channels
- Demo-safe production flow with automatic seeding of Kolkata tutor sample data on deploy/startup
- Docker, Render, PostgreSQL, and SQLite support

## Architecture

### Apps

- `apps/accounts`
  Handles auth, onboarding, custom user model, tutor profiles, parent profiles, OTP flow, and account pages.
- `apps/tutors`
  Handles tutor directory, search, filters, subjects, languages, reviews, and seed data.
- `apps/payments`
  Handles Razorpay order creation, payment verification, webhooks, and payment records.
- `apps/dashboard`
  Handles admin analytics and user management views.
- `apps/chat`
  Handles inbox, thread views, message persistence, and WebSocket consumers.

### Core Data Flow

```text
User
├── TutorProfile
│   ├── Subjects (many-to-many)
│   ├── Languages (many-to-many)
│   └── Payments / Reviews
└── ParentProfile
    ├── Preferred Subjects
    └── Preferred Languages
```

## Tech Stack

| Layer | Tools |
|---|---|
| Backend | Django 5.1, Django Channels, Daphne |
| Database | PostgreSQL in production, SQLite in development |
| Auth | Django Allauth, custom email/phone backends, OTP flow |
| Payments | Razorpay |
| Frontend | Django templates, custom CSS, vanilla JavaScript |
| Realtime | WebSockets via Channels |
| Security | Argon2, Django Axes, CSRF and proxy-aware production settings |
| Deployment | Docker, Docker Compose, Render |

## Project Structure

```text
Tuition_Connect/
├── apps/
│   ├── accounts/
│   ├── tutors/
│   │   └── management/commands/seed_data.py
│   ├── payments/
│   ├── dashboard/
│   └── chat/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/
├── static/
├── media/
├── build.sh
├── start.sh
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

## Local Setup

### 1. Create environment

```powershell
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root.

```env
DJANGO_SECRET_KEY=replace_me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000

DATABASE_URL=
REDIS_URL=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=
RAZORPAY_REGISTRATION_FEE=499

OTP_EXPIRY_SECONDS=300
DEMO_BYPASS_PAYMENT=True
```

### 3. Run migrations and seed data

```powershell
venv\Scripts\python manage.py migrate
venv\Scripts\python manage.py seed_data
```

### 4. Start the app

```powershell
venv\Scripts\python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## Demo Seed Data

The project now seeds a fuller demo dataset with:

- Kolkata-based tutor profiles with Indian names
- Subjects, languages, pricing, contact details, bios, and coordinates
- Parent demo accounts
- Tutor reviews

Run manually:

```powershell
venv\Scripts\python manage.py seed_data
```

The deploy pipeline also runs `seed_data` automatically after migrations in:

- `build.sh`
- `start.sh`
- `Dockerfile` runtime command

This fixes the common issue where local seed data appears in `db.sqlite3` but not on the deployed production database.

## Docker

```bash
docker compose up --build
```

Services:

- Web app on port `8000`
- PostgreSQL on port `5432`
- Redis on port `6379`

## Core Routes

| Route | Purpose |
|---|---|
| `/` | Landing page |
| `/accounts/login/` | Email login |
| `/accounts/register/` | Role-based registration |
| `/accounts/phone/login/` | OTP login |
| `/accounts/onboarding/<step>/` | Tutor onboarding |
| `/accounts/profile/` | Tutor or parent profile |
| `/tutors/` | Tutor directory |
| `/tutors/<id>/` | Tutor detail page |
| `/payments/checkout/` | Tutor payment checkout |
| `/payments/verify/` | Payment verification endpoint |
| `/payments/webhook/` | Razorpay webhook |
| `/chat/` | Chat inbox |
| `/admin/` | Custom admin dashboard |
| `/health/` | Health check |

## Deployment Notes

### Render

- `build.sh` installs dependencies, collects static files, runs migrations, and seeds demo data
- `start.sh` runs migrations again for safety, reseeds demo data idempotently, and starts Daphne
- Production uses `config.settings.production`
- Production database is expected via `DATABASE_URL`

### Important

- Local seeding updates `db.sqlite3`
- Server seeding updates the production database from `DATABASE_URL`
- If tutors are visible locally but not on the server, the deployed DB was not seeded before this change

## Security

- Argon2 password hashing
- Django Axes lockout protection
- CSRF protection and trusted origins support
- Secure proxy settings for hosted deployments
- Session hardening in production

## Recent Changes

- Tutor verification status has been removed from the active platform flow
- Removed the tutor verification badge/system from the active app flow
- Added richer Kolkata tutor seed data
- Updated deploy scripts so demo data seeds on the server automatically
- Kept payment integration in place while allowing transaction pause mode

## Troubleshooting

### Seed data is not showing on the server

Check the following:

1. The server is using `config.settings.production`
2. `DATABASE_URL` points to the expected production database
3. The latest deploy includes the updated `build.sh` and `start.sh`
4. Migrations completed successfully before `seed_data` ran

### Tutors are not live

Check:

1. The tutor profile is complete
2. `is_published=True`
3. `DEMO_BYPASS_PAYMENT=True` if transactions are paused

## Author

**Pawan Kumar**

- Portfolio: `https://pawan-portfolio-dev.vercel.app/`
- GitHub: `https://github.com/Pawan-1809`
- Instagram: `https://www.instagram.com/mr.pawan.kumar/`
- Email: `pawankr16123114@gmail.com`

---

<div align="center">
  <sub>Built for discoverability, onboarding clarity, and faster tutor-student matching.</sub>
</div>
