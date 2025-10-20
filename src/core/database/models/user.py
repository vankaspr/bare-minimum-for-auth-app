from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(100), 
        unique=True,
        index=True,
        nullable=False
        )
    hashed_password: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True,
        nullable=False
        )
    