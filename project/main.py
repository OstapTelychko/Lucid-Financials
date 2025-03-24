from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword
from fastapi.openapi.models import SecuritySchemeType
from fastapi.openapi.utils import get_openapi

from app.models import Base
from app.database import engine
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)