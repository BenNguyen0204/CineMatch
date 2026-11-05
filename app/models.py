"""Database tables for CineMatch."""
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


def utcnow():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    watched = db.relationship("Watched", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    overview = db.Column(db.Text)
    release_date = db.Column(db.Date)
    poster_path = db.Column(db.String(255))
    genres = db.Column(db.String(255))  # e.g. "Action,Comedy"
    vote_average = db.Column(db.Float)
    popularity = db.Column(db.Float)

    watched_by = db.relationship("Watched", back_populates="movie", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Movie {self.title}>"


class Watched(db.Model):
    __tablename__ = "watched"
    # A user can only mark the same movie as watched once.
    __table_args__ = (db.UniqueConstraint("user_id", "movie_id", name="uq_user_movie"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False, index=True)
    rating = db.Column(db.Integer)  # 1-10, optional
    watched_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    user = db.relationship("User", back_populates="watched")
    movie = db.relationship("Movie", back_populates="watched_by")

    def __repr__(self):
        return f"<Watched user={self.user_id} movie={self.movie_id}>"


@login_manager.user_loader
def load_user(user_id):
    # Flask-Login calls this to get the User from the id stored in the session.
    return db.session.get(User, int(user_id))