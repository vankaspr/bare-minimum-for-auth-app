import jwt
import logging


from typing import Optional
from datetime import timedelta

from fastapi import (
    Request, 
    BackgroundTasks,
    )

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database.schemas.user import UserCreate
from core.database.models import User

from utilities.security import hash_password, verify_password
from utilities.jwt_token import create_jwt_token, verify_token

from exceptions import auth

from core.mailing import (
    send_answer_after_verify,
    send_verification_email,
    send_pasword_reset_email,
    send_answer_after_reset_password,
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

        
class UserService:
    def __init__(
        self, 
        session: AsyncSession,
        background_task: Optional[BackgroundTasks] = None
    ):
        self.session = session
        self.background_task = background_task
        
    async def create_user(
        self,
        user_data: UserCreate
    ) -> User:
        """
        Creates a new user with a unique email and username, 
        hashes the password, 
        and sends a token to the email for email confirmation.
        """
        
        # logic for unique email and username
        if await self.get_user_by_email(user_data.email):
            raise auth.EmailAlreadyExist
        if await self.get_user_by_username(user_data.username):
            raise auth.UsernameAlreadyExist
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
        
        # generate token 
        verification_token = await self.generate_verification_token(user.id)
        
        # send verification email
        await self.after_request_verify(user=user, token=verification_token)

        logger.info(
            """
            📧 Verification email sent to %r:
            Token: %r
            """, 
            user.email, verification_token
        )
        return user
    
    async def authenticate(
        self,
        login: str,
        password: str,
    ) -> User:
        """
        Authenticates only active and verified users.
        Allows you to log in using your email or username.
        """
        if "@" in login:
            user = await self.get_user_by_email(login)
        else:
            user = await self.get_user_by_username(login)
            
        if not user:
            raise auth.UserNotFound
        
        if not user.is_active:
            raise auth.AccountDeactivated
        
        if not user.is_verified:
            raise auth.EmailNotVerified
        
        # verifying password
        if not verify_password(password, user.hashed_password):
            raise auth.InvalidPassword
        
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
    
    
    async def generate_verification_token(
        self,
        user_id: int,
    ) -> str:
        """Generate verification token"""
        
        token_data = {
            "sub": str(user_id),
            "type": "email_verification"
        }
        
        return create_jwt_token(
            token_data,
            expires_delta=timedelta(minutes=5)
        )
        
    
    async def after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
    
        """ 
        Generates a verification link and 
        sends an email to the user as a background task.
        """

        # todo: bridge link
        verification_link = f"http://localhost:8000/api/auth/verify-email?token={token}"

        self.background_task.add_task(
            send_verification_email,
            user=user,
            verification_link=verification_link
        )

        logger.info(
            """
            🫴 Email was send with link:
            %r
            to user: %r
            """, 
            verification_link, user.username
        )
    
    
    
    async def verify_email_token(
        self,
        token: str,
    ):
        """
        Verifies the user using a verification token.
        Changes the verification flag to True if this is the case.
        Sends an email confirming successful verification.
        """
        
        try:
            payload = verify_token(token=token)
            
            if not payload or payload.get("type") != "email_verification":
                raise auth.InvalidToken
            
            user_id = int(payload.get("sub"))
            user = await self.get_user_by_id(user_id)

            if not user:
                raise auth.UserNotFound

            user.is_verified = True
            await self.session.commit()
        
            # sending confirm email about verification:
            self.background_task.add_task(
                send_answer_after_verify,
                user=user,
            )
        
            return user
        
        except jwt.ExpiredSignatureError:
            raise auth.ExpiredToken
            
        except jwt.InvalidTokenError:
            raise auth.InvalidToken
    
    # todo: 🫦 create password validation (after check all auth)
    async def validate_password():
        pass
    
    
    async def forgot_password(
        self,
        email: str,
        request: Optional[Request] = None,
    ):
        """ 
        Generates a token and sends the user an email 
        with a link containing the token's query parameter.
        """
        user = await self.get_user_by_email(email=email)
        
        if not user:
            raise auth.UserNotFound
        
        if not user.is_active:
            raise auth.AccountDeactivated
        
        if not user.is_verified:
            raise auth.EmailNotVerified
        
        reset_data = {
            "sub": str(user.id),
            "type": "password_reset",
        }
        
        # create token 
        reset_token =  create_jwt_token(
            reset_data,
            expires_delta=timedelta(minutes=5)
        )
        
        # todo: bridge link
        reset_link = f"http://localhost:8000/api/auth/reset-password?token={reset_token}"
        
        # sent email
        self.background_task.add_task(
            send_pasword_reset_email,
            user=user,
            reset_link=reset_link,
        )
        
        logger.info(
            """
            Password reset link sent to %r:
            Reset link: %r
            Token: %r,
            """,
            email,
            reset_link,
            reset_token,
        )
    
    async def reset_password(
        self,
        token: str,
        new_password: str,
        request: Optional[Request] = None,
    ):
        """ 
        Verifies the token, finds the user by their ID, 
        and hashes the new password. 
        Sends a confirmation email that the password 
        has been changed.
        """
        try:
            payload = verify_token(token=token)
            if not payload or payload.get("type") != "password_reset":
                raise 
            
            user_id = int(payload.get("sub"))
            user = await self.get_user_by_id(user_id=user_id)
            
            if not user:
                raise auth.UserNotFound
            
            if not user.is_active:
                raise auth.AccountDeactivated
            
            user.hashed_password = hash_password(new_password)
            await self.session.commit()
            
            # sent email
            self.background_task.add_task(
                send_answer_after_reset_password,
                user=user,
            )
            
            logger.info(
                """
                Password reset succesfully for user.id: 
                - %r - !! 
                """, user_id
            )
        except jwt.ExpiredSignatureError:
            raise auth.ExpiredToken
        
        except jwt.InvalidTokenError:
            raise auth.InvalidToken