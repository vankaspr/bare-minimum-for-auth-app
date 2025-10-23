from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id", 
            ondelete="CASCADE"
            )
        )
    
    token: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=func.now()
        )