# Running a Demo

How to stand up a working preview of this template in under five minutes —
locally or on a public URL — so you can evaluate it before customising.

---

## Option A — Local preview (fastest)

```bash
git clone <repo-url>
cd <project-directory>
uv sync --group dev
cp .env.example .env
```

Generate and set a `SECRET_KEY` in `.env`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py seed_demo
uv run python manage.py runserver
```

Open **<http://127.0.0.1:8000>**.

The site renders immediately with starter content — four example projects,
six service descriptions, and a populated About page. Log in to
**<http://127.0.0.1:8000/admin>** to explore the content management interface.

---

## Option B — Docker (no Python on the host)

```bash
git clone <repo-url>
cd <project-directory>
cp .env.example .env      # set SECRET_KEY in .env
docker compose up --build
```

In a second terminal:

```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_demo
```

Open **<http://localhost:8000>**.

---

## Option C — Public preview URL (share with others)

The easiest way to share a live preview is to deploy to Railway using the
included configuration. The repo has a `Procfile` and `railway.toml` ready.

1. Push the repo to your GitHub account
2. Create a new Railway project from the repo
3. Set these environment variables in Railway:

```dotenv
SECRET_KEY=<generate one>
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.prod
ALLOWED_HOSTS=<your-railway-domain>
CSRF_TRUSTED_ORIGINS=https://<your-railway-domain>
DATABASE_URL=<Railway will inject this automatically with a Postgres plugin>
CONTACT_EMAIL=hello@yourdomain.com
```

4. After the first deploy, open a shell and run:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
```

> **Note on media uploads in demo mode:** Production uses Cloudinary for
> media storage. For a demo without Cloudinary, media uploads (portrait,
> project images) will not persist across deploys. The starter content seeded
> by `seed_demo` contains no image files and renders cleanly without images.

---

## What the demo shows

After running `seed_demo`, the site contains:

**Home page**
- Practice tagline
- Three featured projects in the portfolio grid
- Services summary section
- Three client testimonials

**Projects**
- Four complete project records across residential, cultural, commercial, and interior categories
- Each project has a full narrative: overview, challenge, concept, and outcome
- Category filter works on the list page

**Services**
- Six service descriptions with `who_for`, `value_proposition`, and `deliverables` fields

**About**
- Populated biography, philosophy, and credentials sections
- `experience_years` is set to `0` as a placeholder — update in admin to see the correct display

**Contact**
- Fully functional contact form
- Submissions save to the database and appear in admin under Contact Inquiries
- Email notifications require SMTP configuration (local dev uses console backend — emails print to terminal)

**Admin**
- Log in at `/admin/` to see the full content management interface
- All content visible on the site is managed entirely through admin — no template editing required

---

## Resetting demo content

To reset the starter content to a clean slate (destructive):

```bash
uv run python manage.py flush --no-input
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py seed_demo
```

Or to wipe only projects and start fresh there:

```bash
# In the Django shell
uv run python manage.py shell
>>> from apps.projects.models import Project, ProjectImage, Testimonial
>>> Testimonial.objects.all().delete()
>>> ProjectImage.objects.all().delete()
>>> Project.objects.all().delete()
```
