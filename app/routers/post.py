from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import List, Optional
from fastapi.params import Body

router = APIRouter(prefix="/posts", tags=['posts'])

@router.get("/", response_model=List[schemas.Post])
async def root(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,
               skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    return posts 



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post:schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = dict(new_post)
    # new_post["id"] = randrange(1,100000)
    # my_posts.append(new_post)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, 
    #                                                                                         post.published ))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.ID)
    new_post = models.Post(user_id = current_user.ID, **dict(post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
async def get_post(id:int, response:Response, db: Session = Depends(get_db) ):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    #post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
        #  response.status_code = status.HTTP_404_NOT_FOUND
        #  return {"message":f"post with id {id} not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # index_post = find_index(id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    #my_posts.pop(index_post)
    # conn.commit()
    if deleted_post.user_id != current_user.ID:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id:int, post:schemas.Post = Body(...), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # index_post = find_index(id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        #print(index_post)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    if updated_post.user_id != current_user.ID:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(dict(post), synchronize_session=False)
    db.commit()
    # updated_post = dict(post)
    # updated_post['id'] = id
    # my_posts[index_post] = updated_post
    #return {"message":f"update post with id {id}"}
    # conn.commit()
    return post_query.first()