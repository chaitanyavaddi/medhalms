# djangocv

Django boilerplate for multi-tenant SaaS apps. Each organization lives on its own subdomain (`org.myapp.com`). Includes auth, Google OAuth, dashboard, Bunny CDN, Cloudflare cache purge, and Resend email — ready to rename and ship.

---

## What's included

- **Auth** — login, signup, forgot/reset password, Google OAuth
- **Organizations** — create org, subdomain routing via middleware
- **Dashboard** — Overview + Settings tabs (general, appearance, domain, account, danger zone)
- **Bunny CDN** — file upload and delete
- **Cloudflare** — cache purge on org save
- **Resend** — welcome and password reset emails (async)
- **HTMX** — partial page updates, no full reloads
- **Dockerfile** — multi-stage Python 3.13 build
- **Traefik** — wildcard subdomain routing config

---

## Local setup

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/chaitanyavaddi/djangocv.git
cd djangocv
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in at minimum:

```
SECRET_KEY=any-long-random-string
DJANGO_SETTINGS_MODULE=config.settings.dev
```

Everything else (Google, Resend, Bunny, Cloudflare) can be left blank locally — those features just won't work until you fill them in.

### 4. Understand how subdomains work locally

The app uses `lvh.me` in dev — it's a public domain that resolves all subdomains to `127.0.0.1`, so `myorg.lvh.me` automatically points to your local machine. No hosts file edits needed.

`dev.py` is already configured for this:

```python
MAIN_DOMAIN = "myapp.lvh.me:8000"
SESSION_COOKIE_DOMAIN = ".lvh.me"
```

So when you create an org with subdomain `acme`, the dashboard will be at:
`http://acme.lvh.me:8000/dashboard/`

### 5. Run migrations

```bash
PYTHONPATH=src python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
PYTHONPATH=src python manage.py createsuperuser
```

### 7. Start the dev server

```bash
PYTHONPATH=src python manage.py runserver
```

Visit `http://myapp.lvh.me:8000` — you'll see the home page.

Go to `/signup/`, create an account, then create an org. You'll be redirected to `http://<subdomain>.lvh.me:8000/dashboard/`.

> **VS Code users:** use the included launch config. Open Run & Debug → `Start App` — it sets `PYTHONPATH` and `DJANGO_SETTINGS_MODULE` automatically.

---

## Rename the boilerplate

Search and replace `myapp` with your app name across:

| File | What to change |
|------|---------------|
| `config/settings/base.py` | `MAIN_DOMAIN`, `BUNNY_CDN_BASE`, email froms, brand colors, font |
| `config/settings/dev.py` | `MAIN_DOMAIN`, cookie domains |
| `config/settings/prod.py` | `ALLOWED_HOSTS`, `MAIN_DOMAIN`, cookie domains |
| `.env.example` | all `myapp.com` references |
| `traefik.yml` | all `myapp.com` and `myapp-` references |
| `templates/base.html` | site name in nav and footer |

---

## Customising brand colors and fonts

Everything lives in `config/settings/base.py` — no template changes needed.

### Colors

```python
BRAND_PRIMARY   = "#e67f0f"   # buttons, links, accents
BRAND_SECONDARY = "#f5f2ee"   # backgrounds, subtle tones
```

These are also editable per-org from the dashboard Settings → Appearance tab.

### Font

```python
BRAND_FONT_URL    = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"
BRAND_FONT_FAMILY = "'Inter', system-ui, sans-serif"
```

To switch fonts:
1. Go to [fonts.google.com](https://fonts.google.com), pick a font, copy the `<link>` URL
2. Paste the URL into `BRAND_FONT_URL`
3. Set `BRAND_FONT_FAMILY` to the font name exactly as Google lists it — e.g. `"'Lato', sans-serif"`

The font loads in every page (`base.html` and `dashboard/base.html`) and is applied via CSS variables (`--font-ui`, `--font-serif`, `--font-reading`) that `dashboard.css` reads from. One change propagates everywhere — auth pages, dashboard, headings, inputs, all of it.

---

## Production deployment on Hetzner + Coolify

### Step 1 — Create a Hetzner VPS

1. Go to [hetzner.com/cloud](https://www.hetzner.com/cloud) → New Project → Add Server
2. Choose Ubuntu 24.04, any region, CPX21 or above recommended
3. Add your SSH key during creation
4. Note the public IP once the server is up

### Step 2 — Install Coolify on the VPS

SSH into your server:

```bash
ssh root@<your-server-ip>
```

Run the Coolify one-line installer:

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

This installs Docker, Traefik, and Coolify itself. It takes 2–3 minutes.

Once done, Coolify's UI is at `http://<your-server-ip>:8000`. Open it, create your admin account.

### Step 3 — Point your domain to the server

In your DNS provider (Cloudflare, etc.), add two A records pointing to the server IP:

```
A    myapp.com        →  <server-ip>
A    *.myapp.com      →  <server-ip>
```

The wildcard `*.myapp.com` is what makes subdomain routing work — every org subdomain hits the same server.

### Step 4 — Connect your GitHub repo to Coolify

1. In Coolify → **Sources** → Add GitHub → follow the OAuth flow
2. Go to **Projects** → New Project → New Resource → **Application**
3. Choose your GitHub repo (`djangocv`)
4. Build pack: **Dockerfile**
5. Set the port to `8000`

### Step 5 — Set environment variables in Coolify

In the app's **Environment Variables** tab, add all production values:

```
DJANGO_SETTINGS_MODULE=config.settings.prod
SECRET_KEY=<generate a long random string>
MAIN_DOMAIN=myapp.com
ALLOWED_HOSTS=myapp.com
SESSION_COOKIE_DOMAIN=.myapp.com
CSRF_COOKIE_DOMAIN=.myapp.com
CSRF_TRUSTED_ORIGINS=https://*.myapp.com,https://myapp.com

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

RESEND_API_KEY=
EMAIL_FROM_NOREPLY=App <noreply@myapp.com>
EMAIL_FROM_UPDATES=App <updates@myapp.com>

BUNNY_STORAGE_ENDPOINT=https://sg.storage.bunnycdn.com
BUNNY_STORAGE_ZONE=your-zone
BUNNY_ACCESS_KEY=
BUNNY_CDN_BASE=https://cdn.myapp.com

CLOUDFLARE_API_TOKEN=
CLOUDFLARE_ZONE_ID=

DB_NAME=postgres
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=5432
```

> Generate a secret key with: `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`

### Step 6 — Set up the database

Coolify can provision a PostgreSQL database for you:

1. **Projects** → same project → New Resource → **PostgreSQL**
2. Deploy it — Coolify gives you the host, port, user, password
3. Copy those into the `DB_*` env vars in your app

### Step 7 — Configure the domain in Coolify

In your app's **Domains** tab:

- Add `myapp.com` as the primary domain
- Add `*.myapp.com` as a second domain (this handles all org subdomains)
- Enable **HTTPS** — Coolify + Traefik handle Let's Encrypt certificates automatically

### Step 8 — Deploy

Hit **Deploy** in Coolify. It will:

1. Pull the repo
2. Build the Docker image (runs `minify.py` + `collectstatic`)
3. Run `manage.py migrate`
4. Start gunicorn on port 8000
5. Traefik routes `myapp.com` and `*.myapp.com` to the container

Check the deploy logs in Coolify if anything fails — they're shown in real time.

### Step 9 — Update Traefik config

`traefik.yml` in the repo is a reference. Coolify manages Traefik itself via its UI — you don't need to deploy this file manually. Update the domain names in it to match yours and keep it in the repo for documentation.

---

## Google OAuth setup

1. Go to [console.cloud.google.com](https://console.cloud.google.com) → APIs & Services → Credentials
2. Create an OAuth 2.0 Client ID (Web application)
3. Add authorized redirect URIs:
   - `http://myapp.lvh.me:8000/auth/google/callback/` (local)
   - `https://myapp.com/auth/google/callback/` (production)
4. Copy the Client ID and Secret into your `.env` / Coolify env vars

---

## Resend email setup

1. Sign up at [resend.com](https://resend.com)
2. Add and verify your sending domain
3. Create an API key
4. Set `RESEND_API_KEY` and `EMAIL_FROM_NOREPLY` in env vars

---

## Bunny CDN setup

1. Sign up at [bunny.net](https://bunny.net)
2. Create a Storage Zone — note the zone name and access key
3. Create a Pull Zone pointing at the storage zone — note the CDN URL
4. Set `BUNNY_STORAGE_ZONE`, `BUNNY_ACCESS_KEY`, `BUNNY_CDN_BASE` in env vars
