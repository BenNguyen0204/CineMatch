# CineMatch

CineMatch helps you find movies you'll actually want to watch. It pulls movie data from the TMDB API, stores it in a Postgres database, and uses it to match you with films based on what you like.

Built with Python, PostgreSQL (hosted on Neon) and the TMDB API.

## Setup

Clone the repo and install the dependencies:

```
git clone <repo-url>
cd CineMatch
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, use `python3 -m venv .venv` and `source .venv/bin/activate` instead.

Create a `.env` file in the project folder:

```
TMDB_API_KEY=your_tmdb_key
DATABASE_URL=your_neon_connection_string
SECRET_KEY=any_long_random_string
```

- **TMDB_API_KEY**: make a free account on themoviedb.org, then go to Settings → API.
- **DATABASE_URL**: create a project on neon.com and copy the connection string from the Connect button. Keep `?sslmode=require` at the end.
- **SECRET_KEY**: generate one with `python -c "import secrets; print(secrets.token_hex(32))"`

## Notes

- The first query after a while can be slow because Neon's free tier sleeps when idle.
- Don't commit your `.env` file.

## Credits

Movie data from TMDB. This product uses the TMDB API but is not endorsed or certified by TMDB.
