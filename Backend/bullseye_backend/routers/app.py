from fastapi import FastAPI, Request
from typing import Optional
from .user import router as user_route
from .login import router as login_route
from .store import router as store_route
from .order import router as order_route
# from dotenv import load_dotenv
from ..config import isConfigured, OathSetUp, SECRET_KEY

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse



app = FastAPI()


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(user_route)
app.include_router(store_route)
app.include_router(order_route)
app.mount('/auth', login_route)



@app.get('/')
def public(request: Request):
    return HTMLResponse(f'<p>Hello from Bullseye API!</p>')
