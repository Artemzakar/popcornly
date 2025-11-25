# backend/scripts/seed_db.py
import os
import sys
from pathlib import Path

# Добавляем корень проекта в PATH, чтобы импортировать app.*
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models.user import User
from app.models.movie import Movie, Genre, MovieGenre
from app.security import get_password_hash


def main():
    # Преобразуем асинхронный URL в синхронный (убираем +asyncpg)
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "")
    engine = create_engine(sync_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Удаляем данные (в обратном порядке из-за внешних ключей)
        session.query(MovieGenre).delete()
        session.query(Movie).delete()
        session.query(Genre).delete()
        session.query(User).delete()
        session.commit()

        # Создаём пользователя
        admin = User(
            email="admin@example.com",
            username="admin",
            password_hash=get_password_hash("123456"),
            is_active=True
        )
        session.add(admin)
        session.flush()  # Получаем admin.id

        # Жанры
        genre_names = ["Action", "Sci-Fi", "Drama", "Comedy", "Animation"]
        genres = {name: Genre(name=name) for name in genre_names}
        session.add_all(genres.values())
        session.commit()  # Теперь у жанров есть id

        # Фильмы
        movies = [
            {"title": "Inception", "year": 2010, "imdb": "tt1375666", "genres": ["Action", "Sci-Fi"]},
            {"title": "The Matrix", "year": 1999, "imdb": "tt0133093", "genres": ["Action", "Sci-Fi"]},
            {"title": "Shrek", "year": 2001, "imdb": "tt0126029", "genres": ["Animation", "Comedy"]},
            {"title": "Interstellar", "year": 2014, "imdb": "tt0816692", "genres": ["Sci-Fi", "Drama"]},
        ]

        for m in movies:
            movie = Movie(
                title=m["title"],
                release_year=m["year"],
                imdb_id=m["imdb"],
                description="Test movie for seeding",
                poster_url=None
            )
            session.add(movie)
            session.flush()

            # Связываем с жанрами
            for g_name in m["genres"]:
                mg = MovieGenre(movie_id=movie.id, genre_id=genres[g_name].id)
                session.add(mg)

        session.commit()
        print("✅ База данных успешно заполнена тестовыми данными!")

    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()