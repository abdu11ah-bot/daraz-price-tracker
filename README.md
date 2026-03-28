# Daraz Price Tracker

A FastAPI + PostgreSQL price tracker for Daraz/Lazada products, ready to deploy on Render.

## Project Structure

```
price-tracker/
├── main.py                  # FastAPI app entry point
├── requirements.txt
├── render.yaml              # Render blueprint (auto-provisions DB + web service)
├── build.sh                 # Build script (installs Chrome + dependencies)
├── .gitignore
└── app/
    ├── __init__.py
    ├── database.py          # SQLAlchemy engine (reads DATABASE_URL env var)
    ├── model.py             # Product ORM model
    ├── data_process.py      # DB read/write + price comparison logic
    ├── webscraper.py        # Selenium scraper for Daraz product pages
    ├── logger.py            # Logging setup
    └── templates/
        └── index.html       # Dark-themed frontend
```

## Deploy to Render (Step-by-step)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/price-tracker.git
git push -u origin main
```

### 2. Create services on Render

**Option A — Blueprint (recommended, auto-creates everything)**
1. Go to https://render.com → New → Blueprint
2. Connect your GitHub repo
3. Render will read `render.yaml` and create both the PostgreSQL database and the web service automatically

**Option B — Manual**
1. Go to https://render.com → New → PostgreSQL → Create (Free plan)
2. Copy the **Internal Database URL** from the database dashboard
3. Go to New → Web Service → Connect your repo
4. Set:
   - **Build Command:** `bash build.sh`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable:
   - `DATABASE_URL` → paste the Internal Database URL

### 3. That's it
Render will build, install Chrome, and start the app. Visit your `.onrender.com` URL.

## Local Development

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# SQLite for local dev (no DATABASE_URL needed)
uvicorn main:app --reload
```

Open http://localhost:8000

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | SQLite fallback (`webscraper.db`) |

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Frontend UI |
| `GET` | `/track/{url}` | Scrape & track a product URL |
| `GET` | `/products` | List all tracked products with current prices |
| `DELETE` | `/products/by-url` | Delete product by URL |
| `DELETE` | `/products/{id}` | Delete product by ID |
