from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "Check out the beaches in Florida",
             "content": "Beaches in florida are so cool", "id": 1}]


@app.get("/")
def read_root():
    return {"welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your post"}


@app.post("/posts")
def create_posts(new_post: Post):
    print(new_post)
    return {"data": new_post}
