from fastapi import HTTPException

class AuthExecption(HTTPException):
    def __init__(
        self, 
        status_code: int, 
        detail: str,
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            )
        
class EmailAlreadyExist(AuthExecption):
    def __init__(self):
        super().__init__(400, "Email already registered 🤯")
        
        
class UsernameAlreadyExist(AuthExecption):
    def __init__(self):
        super().__init__(400, "Username already registered 🤯")
        
        
class InvalidPassword(AuthExecption):
    def __init__(self):
        super().__init__(400, "Invalid password 🫵🧔👎")


class UserNotFound(AuthExecption):
    def __init__(self):
        super().__init__(404, "User not found 😵")
        
        
class AccountDeactivated(AuthExecption):
    def __init__(self):
        super().__init__(403, "Account is deactivated 🤬")
        
        
class EmailNotVerified(AuthExecption):
    def __init__(self):
        super().__init__(403, "Email not verified 🙎‍♀️")


class InvalidToken(AuthExecption):
    def __init__(self):
        super().__init__(400, "Invalid token 🤌")
        
        
class ExpiredToken(AuthExecption):
    def __init__(self):
        super().__init__(400, "Token expired 💥🕜")
        
        
class Unauthorized(AuthExecption):
    def __init__(self):
        super().__init__(401, "Unauthorized 😳")
    