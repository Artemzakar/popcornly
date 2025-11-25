from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

# Импортируем базу и модели (ОБЯЗАТЕЛЬНО, чтобы SQLAlchemy их увидела)
from app.database import engine, Base
from app.models.user import User
from app.models.movie import Movie, Genre, MovieGenre
from app.models.rating import Rating

from app.api import auth


# from app.api import movies, recs, ratings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Server starting... Checking Database...")

    # === МАГИЯ: АВТО-СОЗДАНИЕ ТАБЛИЦ ===
    async with engine.begin() as conn:
        # 1. Включаем расширение для поиска (если нет)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        # 2. Создаем все таблицы, которых еще нет
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Tables created/verified!")

    yield
    print("🛑 Server stopping...")

from app.config import settings
print(settings.DATABASE_URL)

app = FastAPI(
    title="Popcornly API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Popcornly API! 🍿"}