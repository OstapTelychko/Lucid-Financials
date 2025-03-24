from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
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

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))

    # Relationship to Post model (one-to-many)
    posts = relationship("Post", back_populates="owner")


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

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(2000))
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationship to User model (many-to-one)
    owner = relationship("User", back_populates="posts")
