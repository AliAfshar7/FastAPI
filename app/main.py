from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

try: 
    conn = psycopg2.connect(host='192.168.193.31', database='fastapi', user='postgres', password='Kapitan 7',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Dataset connection was successful")
except Exception as error:
    print("Dataset connection was failed")
    print("Error:",error)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

my_posts = []

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        

app = FastAPI()



@app.get("/posts")
async def root(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return {"posts": posts} 

@app.get("/sqlalchemy")
async def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"post":posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post:Post, db: Session = Depends(get_db)):
    # new_post = dict(new_post)
    # new_post["id"] = randrange(1,100000)
    # my_posts.append(new_post)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, 
    #                                                                                         post.published ))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**dict(post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"messages": new_post}

@app.get("/posts/{id}")
async def get_post(id:int, response:Response, db: Session = Depends(get_db) ):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    #post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
        #  response.status_code = status.HTTP_404_NOT_FOUND
        #  return {"message":f"post with id {id} not found"}
    return {"post": post}

def find_index(id):
    for i,post in enumerate(my_posts):
        if post["id"] == id:
            return i

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    # index_post = find_index(id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    #my_posts.pop(index_post)
    # conn.commit()
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id:int, post:Post = Body(...)):
    # index_post = find_index(id)
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if updated_post == None:
        #print(index_post)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    # updated_post = dict(post)
    # updated_post['id'] = id
    # my_posts[index_post] = updated_post
    #return {"message":f"update post with id {id}"}
    conn.commit()
    return {'data':updated_post}
    
    
