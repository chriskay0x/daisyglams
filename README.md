# Daisyglams

A luxury nail studio website built with Django. Visitors can browse the gallery, view services, and book appointments; the studio owner manages everything through a custom admin dashboard.

## Features

- **Public site** — hero landing page, service listings, nail design gallery with category filtering
- **Booking system** — clients submit appointment requests with a preferred date/time, service, and optional inspiration photo
- **Payment proof upload** — clients upload a receipt/screenshot after paying, which the admin verifies to confirm the booking
- **Custom admin dashboard** (not Django's built-in `/admin/`) — manage bookings, verify payments, upload gallery designs, add/remove services, and update business/bank details

## Tech stack

- **Backend:** Django 6.0.7
- **Database:** PostgreSQL (hosted on Supabase, connected via `dj-database-url`)
- **Static files:** WhiteNoise
- **Production server:** Gunicorn
- **Email:** Gmail SMTP (for booking notifications)

## Project structure

```
daisyglams/
├── daisyglams/          # Project settings, root URLs, WSGI/ASGI
├── core/                 # Homepage, gallery, business info (NailDesign, BusinessAccount)
├── bookings/              # Services and appointment booking (Service, Appointment)
├── payments/              # Payment proof upload & verification (PaymentProof)
├── dashboard/              # Custom staff-only admin dashboard
├── templates/              # HTML templates
├── static/                  # Static assets (CSS/JS/images)
├── media/                    # User-uploaded images (designs, receipts, inspiration photos)
├── manage.py
└── requirements.txt
```

## Setup (local development)

**1. Clone the repo and enter the project folder**
```bash
git clone https://github.com/YOUR_USERNAME/daisyglams.git
cd daisyglams
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file** in the project root with the following variables:
```
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@host:5432/dbname
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
ADMIN_EMAIL=your-admin-email@gmail.com
```
> `.env` is gitignored — never commit real credentials.

**5. Run migrations**
```bash
python manage.py migrate
```

**6. Create an admin (staff) user**
```bash
python manage.py createsuperuser
```

**7. Start the dev server**
```bash
python manage.py runserver
```
The site runs at `http://127.0.0.1:8000/`.

## Admin dashboard

The custom dashboard lives at `/dashboard/login/` and requires a staff account (created via `createsuperuser` or Django's user model). It's separate from Django's default `/admin/` panel and is used for day-to-day studio management — bookings, payments, gallery, services, and settings.

## Deployment

The project is configured for deployment on [Render](https://render.com):

- **Build command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start command:** `gunicorn daisyglams.wsgi`
- Required environment variables: `SECRET_KEY`, `DEBUG=False`, `DATABASE_URL`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `ADMIN_EMAIL`, `CSRF_TRUSTED_ORIGINS`

> **Note:** Uploaded media (gallery designs, payment receipts, inspiration photos) is stored on local disk, which is ephemeral on Render's free tier — files will be lost on redeploy or restart unless a persistent disk or external storage (e.g. Cloudinary) is configured.

## License

Private project — all rights reserved.