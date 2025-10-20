from fastapi import HTTPException, status 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database.schemas.user import UserCreate
from core.database.models import User
from utilities.security import hash_password, verify_password


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_user(
        self,
        user_data: UserCreate
    ) -> User:
        """Create new one"""
        
        # logic for unique email and username
        if await self.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
        )
        if await self.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Username already taken"
        )
        
        # password hashing
        hashed_password = hash_password(user_data.password)
        
        # create user
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=False,
            is_superuser=False,
        )
        
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def authenticate(
        self,
        login: str,
        password: str,
    ) -> User:
        """Authenticate user"""
        if "@" in login:
            user = await self.get_user_by_email(login)
        else:
            user = await self.get_user_by_username(login)
            
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
        )
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account is deactivated"
        )
        
        # verifying password
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
        )
        
        return user
    
    async def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Found user by EMAIL and return User 
        or if not found return None.
        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_by_username(
        self,
        username: str,
    ) -> User | None:
        """
        Found user by USERNAME and return User
        or if not found return None.
        """
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
        
    async def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        """
        Found user by ID and return User
        or if not found return None.
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()