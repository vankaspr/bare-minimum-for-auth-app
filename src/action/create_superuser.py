import sys
import os
import asyncio 

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.exc import IntegrityError
from core.database import db_helper
from utilities.security import hash_password
from core.database.models import User


async def create_superuser(
    email: str = "admin@example.com",
    username: str = "admin",
    password: str = "admin",
) -> User:
    """ Create superuser admin"""
    
    hashed_password = hash_password(password)
    
    superuser = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        is_active=True,
        is_verified=True,
        is_superuser=True
    )
    
    try:
        async with db_helper.session_factory() as session:
            session.add(superuser)
            await session.commit()
            await session.refresh(superuser)
            print(f"Admin created: {email}")
            return superuser
    except IntegrityError:
        print("❌ Admin with this email or username already exists!")
        raise 
    


if __name__ == "__main__":
    asyncio.run(create_superuser())