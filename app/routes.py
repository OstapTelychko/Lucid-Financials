from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, Body
from fastapi.responses import RedirectResponse

from app.schemas import UserLogin, PostCreate, Post, UserWithToken
from app.controllers import create_user, login, create_post, get_posts, delete_post
from app.database import get_db
from app.auth import get_current_user

if TYPE_CHECKING:
    from sqlalchemy.orm import Session



router = APIRouter()

@router.get("/", response_class=RedirectResponse)
def redirect_to_docs():
    """
    Redirect to the API documentation page.
    
    Returns:
        RedirectResponse: Redirects to the FastAPI documentation.
    """
    return RedirectResponse(url="/docs", status_code=301)


@router.post("/signup", response_model=UserWithToken)
def signup(user: UserLogin, db: Session = Depends(get_db)):
    """
    Register a new user in the system.
    
    Args:
        user (UserLogin): User credentials containing email and password.
        db (Session): Database session dependency.
    
    Returns:
        UserWithToken: Newly created user with access token for authentication.
        
    Raises:
        HTTPException: If email is already registered.
    """
    result = create_user(db, user)
    return result


@router.post("/login")
def authorize(form_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and provide an access token.
    
    Args:
        form_data (UserLogin): User credentials containing email and password.
        db (Session): Database session dependency.
    
    Returns:
        dict: Access token for authenticated user.
        
    Raises:
        HTTPException: If credentials are invalid.
    """
    return login(db, form_data.email, form_data.password)


@router.post("/addpost", response_model=Post)
def add_post(post: PostCreate, db: Session = Depends(get_db), token: str = Body(..., embed=True)):
    """
    Create a new post for the authenticated user.
    
    Args:
        post (PostCreate): Post content to be created.
        db (Session): Database session dependency.
        token (str): Authentication token for the current user.
    
    Returns:
        Post: Created post details.
        
    Raises:
        HTTPException: If token is invalid or post size exceeds limit.
    """
    current_user = get_current_user(db, token)
    return create_post(db, post, current_user)


@router.post("/getposts", response_model=list[Post])
def retrieve_posts(db: Session = Depends(get_db), token: str = Body(..., embed=True)):
    """
    Retrieve all posts belonging to the authenticated user.
    
    Args:
        db (Session): Database session dependency.
        token (str): Authentication token for the current user.
    
    Returns:
        list[Post]: List of posts owned by the authenticated user.
        
    Raises:
        HTTPException: If token is invalid.
    """
    current_user = get_current_user(db, token)
    return get_posts(db, current_user)


@router.delete("/deletepost/{post_id}")
def remove_post(post_id: int, db: Session = Depends(get_db), token: str = Body(..., embed=True)):
    """
    Delete a specific post owned by the authenticated user.
    
    Args:
        post_id (int): ID of the post to delete.
        db (Session): Database session dependency.
        token (str): Authentication token for the current user.
    
    Returns:
        dict: Success message confirming post deletion.
        
    Raises:
        HTTPException: If token is invalid or post doesn't exist.
    """
    current_user = get_current_user(db, token)
    return delete_post(db, post_id, current_user)
