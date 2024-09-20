from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

try: 
    conn = psycopg2.connect(host='192.168.192.219', database='fastapi', user='postgres', password='Kapitan 7',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Dataset connection was successful")
except Exception as error:
    print("Dataset connection was failed")
    print("Error:",error)



my_posts = []

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        
def find_index(id):
    for i,post in enumerate(my_posts):
        if post["id"] == id:
            return i
        

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)







    
    
    
