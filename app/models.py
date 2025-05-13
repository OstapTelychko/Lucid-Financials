from __future__ import annotations
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.database import Base



class User(Base):
    """
    SQLAlchemy model for the users table.
    
    Represents a user in the system with authentication credentials and
    relationship to their posts.
    
    Attributes:
        id (int): Primary key for the user.
        email (str): User's email address (unique).
        hashed_password (str): Securely hashed password.
        posts (relationship): Relationship to the user's posts.
    """
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    email:Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password:Mapped[str] = mapped_column(String(255))

    # Relationship to Post model (one-to-many)
    posts:Mapped[list[Post]] = relationship("Post", back_populates="owner")


class Post(Base):
    """
    SQLAlchemy model for the posts table.
    
    Represents a post created by a user in the system.
    
    Attributes:
        id (int): Primary key for the post.
        text (str): Content of the post.
        owner_id (int): Foreign key to the users table.
        memory_id (str): UUID reference for in-memory storage.
        owner (relationship): Relationship to the user who owns the post.
    """
    __tablename__ = "posts"

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    text:Mapped[str] = mapped_column(String(2000))
    owner_id:Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relationship to User model (many-to-one)
    owner:Mapped[User] = relationship("User", back_populates="posts")
