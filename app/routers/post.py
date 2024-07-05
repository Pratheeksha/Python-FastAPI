from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)

    # convert to dictionary and unpack it insteaed of assigning each value
    # post_new = models.Post(
    #     title=new_post.title, content=new_post.content, published=new_post.published)
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retreive the newly created post

    # cursor.execute(""" Insert into Posts (title,content,published) values (%s,%s,%s) Returning *""",
    #                (new_post.title, new_post.content, new_post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post
    # sql = "select * from posts where id = %(id)s;"
    # param = {"id": id}
    # cursor.execute(sql, param)
    # post = cursor.fetchone()
    # return {"data": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    return {'message': 'post was successfully deleted'}

    # sql = "delete from posts where id = %(id)s returning * ;"
    # param = {"id": id}
    # cursor.execute(sql, param)
    # deleted = cursor.fetchone()
    # conn.commit()


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    existing_post = post_query.first()

    if existing_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()

    return {'message': 'post was successfully updated', 'data': post_query.first()}

    # sql = "update posts set title = %(title)s,content = %(content)s,published=%(published)s where id = %(id)s returning * ;"
    # param = {"title": post.title, "content": post.content,
    #          "published": post.published, "id": id}
    # cursor.execute(sql, param)
    # updated = cursor.fetchone()
    # conn.commit()
