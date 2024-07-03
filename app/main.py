import time
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"data": post}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    cursor.execute(""" Insert into Posts (title,content,published) values (%s,%s,%s) Returning *""",
                   (new_post.title, new_post.content, new_post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    sql = "select * from posts where id = %(id)s;"
    param = {"id": id}
    cursor.execute(sql, param)
    post = cursor.fetchone()
    return {"data": post}

    # post = find_post(id)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id {id} was not found")
    # return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    sql = "delete from posts where id = %(id)s returning * ;"
    param = {"id": id}
    cursor.execute(sql, param)
    deleted = cursor.fetchone()
    conn.commit()

    if deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    return {'message': 'post was successfully deleted'}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    sql = "update posts set title = %(title)s,content = %(content)s,published=%(published)s where id = %(id)s returning * ;"
    param = {"title": post.title, "content": post.content,
             "published": post.published, "id": id}
    cursor.execute(sql, param)
    updated = cursor.fetchone()
    conn.commit()

    if updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    return {'message': 'post was successfully updated', 'data': updated}
