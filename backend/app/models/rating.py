from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Явный индекс для user_id (для ускорения выборки истории пользователя)
    __table_args__ = (
        Index('idx_ratings_userid', 'user_id'),
    )