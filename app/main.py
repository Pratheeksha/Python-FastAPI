import time
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import psycopg
from sqlalchemy.orm import Session
from . import models
from .database import engine
from .routers import post, user, auth
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

while True:
    try:
        conn = psycopg.connect(
            host='localhost', dbname='fastapi', user='postgres', password='admin123')
        cursor = conn.cursor()
        print("connection to database was sucessfull")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error: ", error)
        time.sleep(2)
