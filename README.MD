# Student Feedback Backend

Django REST API for collecting and managing student feedback. Includes JWT-based auth (cookies), feedback CRUD, and admin workflows.

**Requirements**

- **Python:** 3.10+ (recommended)
- **Packages:** See `requirements.txt` ([requirements.txt](requirements.txt))

**Environment variables**

- **SECRET_KEY:** Django secret key
- **DEBUG:** `TRUE` or `FALSE`
- **DJANGO_ENV:** `production` to enable secure cookies
- **DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT:** PostgreSQL credentials

**Quick Setup**

- Create and activate a virtual env, then install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

- Create a `.env` file with the required environment variables above.
- Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

- Start the development server:

```bash
python manage.py runserver
```

**Project structure**

- **manage.py:** [manage.py](manage.py)
- **Config:** [config/settings.py](config/settings.py), [config/urls.py](config/urls.py)
- **Authentication:** [auth/authentication.py](auth/authentication.py), [auth/views.py](auth/views.py)
- **Feedback app:** [feedback/models.py](feedback/models.py), [feedback/serializers.py](feedback/serializers.py), [feedback/views.py](feedback/views.py), [feedback/urls.py](feedback/urls.py)

**Authentication & Tokens**

- The project uses `rest_framework_simplejwt` and stores tokens in HTTP-only cookies:
  - `access_token` cookie (used by API requests)
  - `refresh_token` cookie (used to refresh access)
- Custom cookie authentication class: `auth.authentication.CookieJWTAuthentication` ([auth/authentication.py](auth/authentication.py)).
- Endpoints for auth (defined in [config/urls.py](config/urls.py)):
  - `POST /api/register/` — register new user (sets cookies)
  - `POST /api/token/` — login (sets cookies)
  - `POST /api/token/refresh/` — refresh access token (reads `refresh_token` cookie)
  - `GET /api/me/` — validate current token and return user info (requires authentication)

**Feedback API**

- Routes (prefixed with `/api/`, see [feedback/urls.py](feedback/urls.py)):
  - `GET /api/feedbacks/` — list feedbacks (staff/admin sees all; users see their own)
  - `POST /api/feedbacks/` — create feedback (authenticated users only)
  - `PUT /api/feedbacks/:id` — update feedbacks (status gets resetted to pending)
  - `DELETE /api/feedbacks/:id` — delete feedbacks(authenticated users only, staff/admin cant delete)

**Models**

- `Feedback` model (see [feedback/models.py](feedback/models.py)) fields:
  - `subject`
  - `category` (academics|infrastructure|activities|other),
  - `message`
  - `rating` (1-5),
  - `status` (pending|reviewed|resolved)
  - `created_at`, `updated_at`, `user` (Django `User`)

**Serializers**

- `FeedbackSerializer` — for regular users; fields read-only: `user`, `status`, `created_at` and `updated_at`
- `AdminFeedbackSerializer` — for staff; allows status updates (see [feedback/serializers.py](feedback/serializers.py))

**Permissions & Behavior**

- All feedback endpoints require authentication (`IsAuthenticated`).
- Non-staff users can only access and modify their own feedback. When non-staff users update a feedback, `status` is forced to `pending`.
- Staff users can list and operate on all feedback and use the admin serializer.


**Notes & Next Steps**

- Configure `CORS_ALLOWED_ORIGINS` in `config/settings.py` for your frontend (it currently allows `http://localhost:3000`).
- Ensure `.env` includes database and secret values before running in production and set `DJANGO_ENV=production` to enable secure cookie flags.
