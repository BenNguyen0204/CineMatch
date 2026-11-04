# 🎬 CineMatch

A movie recommendation web app: *"If you liked this movie, you might also like…"*.
Users mark the movies they've watched (with an optional rating), and CineMatch suggests similar movies — never recommending ones they've already seen.

## Features
- Browse and search thousands of popular movies (data from TMDB)
- Movie detail page with poster, genres, director, cast and similar-movie suggestions
- Mark movies as watched and rate them 1–5★
- Personalized recommendations based on your full watch history
- Watched movies are automatically excluded from all recommendations

## How it works
1. **ETL** – `scripts/sync_movies.py` pulls popular movies from the TMDB `/discover/movie` endpoint, then enriches each one with genres, director and top cast via `/movie/{id}?append_to_response=credits`, and stores everything in PostgreSQL.
2. **Content-based filtering** – each movie's genres, director, cast and overview are combined and vectorized with **TF-IDF**; similarity is measured with **cosine similarity**.
3. **Personalization** – a user profile is built as a rating-weighted average of the movies they liked, then compared against all movies. Anything in the user's `watched` table is filtered out.

## Tech stack
Python · Flask · SQLAlchemy · Flask-Login · PostgreSQL (Neon) · pandas · scikit-learn · TMDB API · Bootstrap

## Project structure
```
app/
├── __init__.py       # app factory
├── models.py         # User, Movie, Watched
├── tmdb.py           # TMDB API client
├── recommender.py    # TF-IDF recommendation engine
├── routes.py         # web routes
└── templates/
scripts/
└── sync_movies.py    # TMDB → PostgreSQL pipeline
run.py
```

## Getting started
**1. Clone and install**
```bash
git clone https://github.com/<your-username>/cinematch.git
cd cinematch
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

**2. Configure environment** — create a `.env` file:
```
TMDB_API_KEY=your_tmdb_api_key
DATABASE_URL=postgresql://<user>:<password>@<host>/<db>?sslmode=require
SECRET_KEY=a_long_random_string
```
Get a free API key at [themoviedb.org](https://www.themoviedb.org/settings/api) and a Postgres connection string from [Neon](https://neon.tech).

**3. Create tables and load movies**
```bash
export FLASK_APP=run.py
flask db upgrade
python scripts/sync_movies.py
```

**4. Run**
```bash
flask run --debug
```
Open http://127.0.0.1:5000

## Roadmap
- Onboarding: pick favorite movies to solve cold start
- Collaborative filtering ("users who liked A also liked B")
- Sentence embeddings + pgvector for better similarity
- Scheduled weekly sync of new movies

## Attribution
This product uses the TMDB API but is not endorsed or certified by TMDB.
