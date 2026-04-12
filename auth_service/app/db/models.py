from sqlalchemy import String, Integer, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    __table_args__ = (
        Index("ix_users_email_unique", "email", unique=True),
    )
