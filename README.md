# Tuition Connect

A full-stack Django platform that connects parents and students with home tutors.

Tuition Connect includes role-based onboarding, tutor discovery with filtering, OTP and email authentication, secure login protection, real-time chat foundation, and production-ready deployment support.

## Why This Project

This project is built to solve a real workflow:

- Tutors can register, complete profile onboarding, and publish availability.
- Parents can browse, filter, and compare tutor profiles.
- The platform supports secure authentication and profile-driven matching.

## Key Features

- Role-based user system
  - Tutor
  - Parent/Student
  - Admin
- Authentication options
  - Email/password login
  - Phone OTP login and registration
  - Google OAuth via Django Allauth
- Tutor onboarding workflow
  - Multi-step guided profile completion
  - Subject/language selection
  - Location and teaching preferences
- Tutor directory
  - Filters for subjects, language, grade level, pricing, teaching method
  - Pagination and async-friendly partial rendering
- Payments integration
  - Razorpay order creation, verification, webhook handling
- Security hardening
  - Argon2 hashing
  - Django Axes brute-force protection
  - CSRF trusted origins and proxy-aware production settings
- Deployment-ready setup
  - Docker and docker-compose
  - Render scripts for build/start
  - PostgreSQL-ready production settings

## Temporary Demo Behavior

The project is currently configured for demonstration mode in production:

- Tutor payment gate is bypassed.
- Completed tutor profiles can go live directly.

Current toggle behavior:

- Base setting reads DEMO_BYPASS_PAYMENT from environment.
- Production currently forces DEMO_BYPASS_PAYMENT = True.

When you want to restore paid publishing, set the production override back to False and redeploy.

## Tech Stack

- Backend: Django 5.1, Channels, Daphne
- Database: PostgreSQL (production), SQLite (development default)
- Cache/Session: Redis optional in production with automatic fallback
- Frontend: Django templates, static CSS/JS
- Auth: Django Allauth, custom auth backends, OTP flow
- Security: Django Axes, Argon2, secure cookie and proxy settings
- Deployment: Docker, Render

## Project Structure

```text
Tuition_Connect/
├── apps/
│   ├── accounts/
│   ├── tutors/
│   ├── payments/
│   ├── dashboard/
│   └── chat/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── urls.py
├── templates/
├── static/
├── media/
├── Dockerfile
├── docker-compose.yml
├── build.sh
├── start.sh
├── manage.py
└── requirements.txt
```

## Quick Start (Local)

### 1) Clone and create virtual environment

```bash
git clone <your-repo-url>
cd Tuition_Connect
python -m venv venv
```

### 2) Activate environment

Windows PowerShell:

```powershell
venv\Scripts\Activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Run migrations

```bash
python manage.py migrate
```

### 5) Start server

```bash
python manage.py runserver
```

Application URL:

- http://127.0.0.1:8000/

## Run with Docker Compose

```bash
docker compose up --build
```

This starts:

- Web app on port 8000
- PostgreSQL on port 5432
- Redis on port 6379

## Environment Variables

Create a .env file at project root.

Recommended variables:

```env
DJANGO_SECRET_KEY=replace_me
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,home-tutor-finder-fpzm.onrender.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://home-tutor-finder-fpzm.onrender.com

DATABASE_URL=postgresql://user:password@host:5432/dbname
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

Notes:

- If REDIS_URL is empty in production, app falls back to local-memory cache and DB sessions.
- In demonstration mode, DEMO_BYPASS_PAYMENT allows direct tutor publishing.

## Core Routes

Public:

- /
- /tutors/
- /tutors/<id>/

Auth:

- /accounts/login/
- /accounts/register/
- /accounts/phone/login/
- /accounts/phone/verify/

Tutor onboarding and profile:

- /accounts/onboarding/<step>/
- /accounts/profile/

Payments:

- /payments/checkout/
- /payments/verify/
- /payments/webhook/

Health:

- /health/

## Deployment Notes (Render)

- Build script: build.sh
- Start script: start.sh
- Production settings include:
  - Proxy SSL header support
  - CSRF trusted origins handling
  - PostgreSQL via DATABASE_URL
  - Redis optional fallback

If using Docker runtime, ensure startup executes migrations before serving traffic.

## Security Notes

- Do not use default fallback secret key in production.
- Set strict ALLOWED_HOSTS and CSRF trusted origins.
- Configure secure HTTPS behavior in production environment.
- Keep OAuth and payment secrets in environment variables only.

## Troubleshooting

1) UndefinedTable errors in production

- Confirm DATABASE_URL is set.
- Confirm migrations run successfully during deployment.

2) CSRF 403 on POST in production

- Check DJANGO_CSRF_TRUSTED_ORIGINS includes your exact HTTPS domain.
- Verify proxy headers are correctly trusted.

3) Redis connection failure

- Provide REDIS_URL, or leave it empty to use built-in fallback.

## Author

Pawan Kumar

- Portfolio: https://pawan-portfolio-dev.vercel.app/
- GitHub: https://github.com/Pawan-1809
- Instagram: https://www.instagram.com/mr.pawan.kumar/
- Email: pawankr16123114@gmail.com

## License

This project is available for educational and demonstration purposes.
