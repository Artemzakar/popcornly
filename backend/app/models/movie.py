from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


# === Таблица связи (Many-to-Many) ===
class MovieGenre(Base):
    __tablename__ = "movie_genres"

    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)


# === Жанры ===
class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # Связь с фильмами (для удобства, если понадобится)
    movies = relationship("Movie", secondary="movie_genres", back_populates="genres")


# === Фильмы ===
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)  # Внутренний ID

    title = Column(String(255), nullable=False)
    poster_url = Column(String(512), nullable=True)
    description = Column(Text, nullable=True)
    release_year = Column(Integer, nullable=True)

    # Ссылка на IMDb
    imdb_id = Column(String(20), unique=True, index=True, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    # lazy="selectin" критически важен для асинхронности (подгружает жанры сразу)
    genres = relationship("Genre", secondary="movie_genres", back_populates="movies", lazy="selectin")

    # Индекс для Trigram поиска (как в SQL)
    __table_args__ = (
        Index(
            'idx_movies_title_trgm',
            'title',
            postgresql_ops={'title': 'gin_trgm_ops'},
            postgresql_using='gin'
        ),
    )


# === Глобальные рекомендации ===
class GlobalRecommendation(Base):
    __tablename__ = "global_recommendations"

    rank = Column(Integer, primary_key=True)  # 1, 2, 3...
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))

    movie = relationship("Movie")  # Чтобы легко вытащить инфу о фильме