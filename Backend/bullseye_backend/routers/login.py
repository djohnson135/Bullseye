from fastapi import Request, APIRouter, Depends, FastAPI
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from ..config import OathSetUp
from ..jwt import create_token, CREDENTIALS_EXCEPTION, valid_email_from_db
from starlette.responses import JSONResponse
import bullseye_backend.crud.user as crud
from sqlalchemy.orm import Session
from ..dependencies import get_db
import bullseye_backend.schemas.user as schema
import json
from starlette.middleware.sessions import SessionMiddleware
from ..config import isConfigured, OathSetUp, SECRET_KEY
import bullseye_backend.models.user as model
from bullseye_backend.database import SessionLocal




router = FastAPI()

oauth = OathSetUp()
router.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


@router.get('/login-redirect')
async def login(request: Request):
    # redirect_uri = request.url_for('token')  # This creates the url for the /auth endpoint
    redirect_uri = 'https://api.bullseye.host/auth/token'
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/token')
async def token(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise CREDENTIALS_EXCEPTION
    request.session['user'] = dict(access_token['userinfo'])
    
    # #add user to database and create token
    userSession = request.session.get('user')
    email = userSession.get('email')
    
    if valid_email_from_db(email) is False:
        #add user to db
        db = SessionLocal()
        fname = userSession.get('given_name')
        lname = userSession.get('family_name')
        email = userSession.get('email')
        userData = {}
        userData['fname'] = fname
        userData['lname'] = lname
        userData['email'] = email
        newUser = model.User(**userData)
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        db.close()

    internal_auth_token = create_token(userSession.get('email'))
    redirect_url = f"https://www.bullseye.host/Path/?access_token={internal_auth_token}&user_email={email}"
    response = RedirectResponse(url=redirect_url)
    response.delete_cookie(key="state")
    return response


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')