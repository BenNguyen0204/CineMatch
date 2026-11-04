# Decisions

Entries are append-only. To change a decision, add a new entry and mark the old one `Superseded by D-XXX`.

Statuses: `Accepted` is the chosen direction. `Proposed` still needs the project owner's confirmation.

Entries D-001 to D-006 were recorded from the README, which states the choices but not the reasons. Their reasons are inferred, so correct them if they are wrong.

## D-001: Flask with server-rendered templates
- Date: 2026-11-03
- Status: Accepted
- Decision: Build a Flask app with templates and Bootstrap, using Flask-Login for auth.
- Reason (inferred): A single Python codebase can serve both the web app and the recommender.

## D-002: PostgreSQL on Neon
- Date: 2026-11-03
- Status: Accepted
- Decision: Store data in a hosted Neon PostgreSQL database, accessed through SQLAlchemy.
- Reason (inferred): It provides managed Postgres without running a local server.

## D-003: Flask-Migrate for schema changes
- Date: 2026-11-03
- Status: Accepted
- Decision: Manage the schema with migrations.
- Reason (inferred): The README setup uses `flask db upgrade`, which keeps schema changes versioned.

## D-004: TMDB as the movie data source, loaded by a batch job
- Date: 2026-11-03
- Status: Accepted
- Decision: `scripts/sync_movies.py` pulls from `/discover/movie`, enriches each movie through `/movie/{id}?append_to_response=credits`, and stores the results in PostgreSQL.
- Reason (inferred): Serving movies from the local database keeps pages independent of TMDB rate limits, and the recommender needs all movies available locally.

## D-005: Content-based filtering with TF-IDF and cosine similarity
- Date: 2026-11-03
- Status: Accepted
- Decision: Vectorize each movie's genres, director, cast and overview with TF-IDF, and compare movies with cosine similarity.
- Reason (inferred): It works with no user data and is simple to build and explain. Collaborative filtering and embeddings stay on the README roadmap.

## D-006: Rating-weighted user profiles
- Date: 2026-11-03
- Status: Accepted
- Decision: Build each user's profile as a rating-weighted average of the movies they liked, compare it against all movies, and filter out anything they have watched.
- Reason (inferred): Higher-rated movies should influence recommendations more, and watched movies should never be suggested.

## D-007: App factory layout
- Date: 2026-11-03
- Status: Accepted
- Decision: `app/__init__.py` defines unbound `db`, `migrate` and `login_manager` instances and a `create_app()` factory. `create_app()` imports models and routes internally and registers a blueprint named `main`. A missing `SECRET_KEY` or `DATABASE_URL` fails at startup. The SQLAlchemy engine uses `pool_pre_ping`.
- Reason: Unbound extensions avoid circular imports with models and routes. Failing early makes configuration errors obvious. Pre-ping avoids errors from idle connections that Neon has closed.
