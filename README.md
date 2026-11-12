# CineMatch

A full-stack movie recommendation app. Search thousands of movies, rate the ones you've seen, and CineMatch suggests what to watch next based on genres, keywords, cast, directors and plot. Built with Flask, SQLAlchemy and PostgreSQL, with a vanilla JavaScript frontend that works on desktop and phone.

Movie data comes from the TMDB API and is synced into my own database, so the recommender runs on local data instead of calling TMDB on every request.

**Live demo:** _coming soon_

<!-- ![Desktop view](docs/screenshots/desktop.png) -->

<!--
<p align="center">
  <img src="docs/screenshots/phone-home.png" alt="Phone: home" width="260">
  &nbsp;&nbsp;
  <img src="docs/screenshots/phone-movie.png" alt="Phone: movie page" width="260">
</p>
-->

## Features

**Movies**
- Search movies by title, filter by genre and sort by rating, popularity or release date
- Movie page with poster, overview, runtime, director and top cast
- "More like this" row on every movie
- Dark mode
- Phone layout: sidebar first, tap a section to open it, the back gesture returns to the sidebar

**Ratings and recommendations**
- Rate movies from 1 to 5 stars, change or remove a rating any time
- "For you" page built from the movies you rated highly
- Movies you already rated never show up as recommendations
- New users see popular and top-rated movies until they've rated a few

**Accounts**
- Sign up and log in, each user only sees their own ratings
- Display name and password change

## Tech stack

| Part | Tools |
|---|---|
| Backend | Python, Flask, REST API (JSON) |
| Database | SQLAlchemy, Flask-Migrate (Alembic), PostgreSQL on Neon, SQLite locally |
| Data | TMDB API, requests |
| Recommender | scikit-learn (TF-IDF, cosine similarity) |
| Auth and security | Flask-Login, Werkzeug password hashing, Flask-WTF (CSRF), Flask-Limiter |
| Frontend | HTML, CSS, vanilla JavaScript (no framework) |
| Testing | pytest, pytest-cov |
| Deployment | Render (gunicorn), Neon |

## Architecture

```mermaid
flowchart TB
    User(["Browser<br/>(desktop or phone)"])
    subgraph Render["Render (gunicorn)"]
        Pages["pages + auth<br/>HTML pages, log in / sign up"]
        API["api<br/>REST JSON"]
        Rec["recommender<br/>TF-IDF + cosine similarity"]
    end
    DB[("PostgreSQL<br/>on Neon")]
    Vec[["TF-IDF vectors"]]
    subgraph Jobs["Offline scripts"]
        Sync["sync_movies.py"]
        Build["build_similarity.py"]
    end
    TMDB["TMDB API"]
    CDN["TMDB image CDN"]

    User -- "page load, forms" --> Pages
    User -- "fetch + CSRF token" --> API
    User -- "poster images" --> CDN
    Pages --> DB
    API -- "SQLAlchemy, ratings scoped to current_user" --> DB
    API --> Rec
    Rec --> Vec
    TMDB -- "movies, genres, keywords, credits" --> Sync
    Sync -- "upsert" --> DB
    DB --> Build --> Vec
```

**How a request goes**

1. The browser loads `/` once. Flask renders `index.html` with the CSRF token in a `<meta>` tag.
2. After that the JavaScript only talks to `/api/...` with `fetch`, sending the token in an `X-CSRFToken` header.
3. Flask-Login reads the session cookie. Every rating query filters by `current_user.id`, so nobody can read or change someone else's ratings.
4. For recommendations, the API passes the user's ratings to the recommender, which scores movies with the precomputed vectors and returns movie ids. The API then loads those movies from the database.
5. Posters load straight from TMDB's image CDN, so the server never stores images.

**Code layout**

- `create_app()` builds the app, so tests can make a fresh one with their own config
- 3 blueprints: `pages`, `auth` and `api` (under `/api`)
- The recommender is plain Python with no Flask code, so it can be tested on its own
- Database changes go through Flask-Migrate, and Render runs `db upgrade` on every deploy

**Data model**

```mermaid
erDiagram
    USER ||--o{ RATING : gives
    MOVIE ||--o{ RATING : receives
    MOVIE }o--o{ GENRE : "has (movie_genres)"
    MOVIE }o--o{ KEYWORD : "has (movie_keywords)"
    MOVIE }o--o{ PERSON : "cast (movie_cast)"
    USER {
        int id
        string username
        string display_name
        string password_hash
    }
    MOVIE {
        int tmdb_id
        string title
        string overview
        date release_date
        string poster_path
        float vote_average
        int vote_count
        float popularity
        string director
    }
    RATING {
        int user_id
        int tmdb_id
        int rating
        datetime created_at
    }
    GENRE {
        int id
        string name
    }
    KEYWORD {
        int id
        string name
    }
    PERSON {
        int id
        string name
    }
```

Movies use TMDB's own ids, so syncing again updates a movie instead of adding a copy. Each user can rate a movie only once (1 to 5), and deleting a user deletes their ratings.

## How recommendations work

1. `scripts/sync_movies.py` pulls movies, genres, keywords and credits from TMDB into PostgreSQL. It's safe to run again: existing movies are updated, not duplicated.
2. `scripts/build_similarity.py` builds a text profile for every movie (genres, keywords, top cast, director, overview), turns the profiles into TF-IDF vectors and saves them.
3. **Similar movies:** the movies whose vectors are closest by cosine similarity.
4. **For you:** similarity scores added up across your highly rated movies, minus anything you've already rated, with a minimum vote count so obscure films don't take over.

## Security

- Passwords are stored as salted hashes, never in plain text
- Ratings are always looked up for the logged-in user, so nobody can read or change someone else's
- CSRF tokens on every form and API call, plus `SameSite=Lax`, `HttpOnly` and `Secure` cookies
- Rate limits on login and sign up
- All secrets (TMDB key, database URL, `SECRET_KEY`) come from environment variables, the app refuses to start without `SECRET_KEY`

## Run it locally

Needs Python 3.12 or newer and a free [TMDB API key](https://www.themoviedb.org/settings/api).

```powershell
git clone https://github.com/BenNguyen0204/CineMatch.git
cd CineMatch
python -m venv .venv
.venv\Scripts\Activate.ps1          # macOS / Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
```

Copy `.env.example` to `.env` and fill in `SECRET_KEY` and `TMDB_API_KEY`:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Leave `DATABASE_URL` empty to use a local SQLite file, or paste your Neon connection string.

```powershell
flask --app wsgi db upgrade              # create the tables
python -m scripts.sync_movies            # load movies from TMDB
python -m scripts.build_similarity       # build the recommendation data
flask --app wsgi run                     # http://127.0.0.1:5000
```

## Tests

```powershell
pytest              # run all tests
pytest --cov=app    # with coverage
```

Each test gets a fresh app and a temporary database, and TMDB calls are mocked so tests never hit the network. They cover login protection, rating CRUD, input validation, users not being able to change each other's ratings, and the recommender (right number of results, no already-rated movies, unknown ids).

## API

Routes marked with a lock need a logged-in user. All routes return JSON.

| Method | URL | What it does |
|---|---|---|
| `GET` | `/api/movies?q=&genre=&sort=` | Search, filter and sort movies |
| `GET` | `/api/movies/<id>` | One movie with genres, cast and director |
| `GET` | `/api/movies/<id>/similar` | Movies similar to this one |
| `GET` | `/api/genres` | All genres, for the filter menu |
| `GET` 🔒 | `/api/ratings` | All of my ratings |
| `PUT` 🔒 | `/api/ratings/<movie_id>` | Rate a movie (1–5) or change the rating |
| `DELETE` 🔒 | `/api/ratings/<movie_id>` | Remove a rating |
| `GET` 🔒 | `/api/recommendations` | My personalized recommendations |
| `GET` / `PATCH` 🔒 | `/api/account` | Read or update display name |
| `POST` 🔒 | `/api/account/password` | Change password |

## Project structure

```text
app/
  __init__.py      app factory, config, security settings
  extensions.py    db, migrate, login manager, csrf, limiter
  models.py        User, Movie, Genre, Keyword, Person, Rating
  api.py           REST API: movies, ratings, recommendations
  auth.py          sign up, log in, log out
  pages.py         main page, /healthz
  recommender.py   TF-IDF similarity and recommendations
  tmdb.py          TMDB API client
  templates/       HTML
  static/          CSS, JavaScript, images
scripts/           TMDB sync, building the recommendation data
migrations/        database migrations
tests/             pytest suite
wsgi.py            entry point for gunicorn
```

## Deployment

Runs on Render's free plan with a Neon PostgreSQL database.

- Build: `pip install -r requirements.txt`
- Start: `flask --app wsgi db upgrade && gunicorn wsgi:app --workers 1 --threads 4 --bind 0.0.0.0:$PORT`
- Health check: `/healthz`
- Environment variables: see `.env.example`

## What's next

- Weekly job to sync new releases from TMDB
- "Why this recommendation?" (shared genres and actors)
- Collaborative filtering once there's enough rating data
- Run the tests automatically on every push

---

This product uses the TMDB API but is not endorsed or certified by TMDB.
