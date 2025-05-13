from __future__ import annotations
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Base schema for user data.
    
    Attributes:
        email (EmailStr): User's email address.
    """
    email: EmailStr


class UserLogin(UserBase):
    """
    Schema for user login/registration.
    
    Extends UserBase with password field.
    
    Attributes:
        password (str): User's password in plain text.
    """
    password: str


class User(UserBase):
    """
    Schema for user representation.
    
    Extends UserBase with additional user information.
    
    Attributes:
        id (int): User's unique identifier.
        posts (list[Post]): List of posts created by the user.
    """
    id: int
    posts: list[Post] = []

    class Config:
        from_attributes = True


class UserWithToken(BaseModel):
    """
    Schema for user representation with authentication token.    class Config:
    ibutes = True
    Used when returning a user with their authentication token.
    
    Attributes:
        access_token (str): JWT token for authentication.class TokenData(BaseModel):
        token_type (str): Type of token (typically "bearer").        user (User): User object.
    """
    access_token: str
    user: User


class PostBase(BaseModel):
    """
    Base schema for post data.
    
    Attributes:
        text (str): Content of the post.
    """
    text: str


class PostCreate(PostBase):
    """
    Schema for post creation.
    
    Currently identical to PostBase, may be extended with
    additional fields in the future.
    
    Attributes:
        text (str): Content of the post.
    """
    text: str


class Post(PostBase):
    """
    Schema for post representation.
    
    Extends PostBase with additional post information.
    
    Attributes:
        id (int): Post's unique identifier.
        owner_id (int): ID of the user who owns the post.
        memory_id (str): Optional ID for in-memory reference.
    """
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    """
    Schema for token data.
    
    Used for token validation and authentication.
    
    Attributes:
        token (str): Authentication token.
    """
    token: str