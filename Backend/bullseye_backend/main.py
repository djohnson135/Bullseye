import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from bullseye_backend.dependencies import create_database
from bullseye_backend.routers.app import app
import uvicorn

# create_database()

def start():
    uvicorn.run("bullseye_backend.main:app", host="0.0.0.0", port=8000)
