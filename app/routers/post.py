from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut]) # Siin List (from typing lib), sest võttame mitu posti, teistes vaid 1
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
                     ,limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()


    #Lots of query parameter stuff here, kinda testing atm.
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes") ).join(models.Vote,
      models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts #FastAPI converts automaticaly into json types stuff


@router.get("/{id}", response_model=schemas.PostOut) #ID is called "path parameter" , could name it dingdong if wanted. Its just like a argument/variable
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #id: int > Et url ei oleks "afasdfasdfasf" <-- Siis viskab errori. Response imported from FastAPI
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s RETURNING *""", (str(id)))
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes") ).join(models.Vote,
      models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    
    if not post: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                 detail=f"Post with id: {id} was not found")
    return post


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post) # Create puhul default kood 201. Miks mitte lihtsalt "201", miks status.blabblalba
async def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ): # Ekstraktib body read dictiks "pay..
    #cursor.execute(""" INSERT INTO posts(title, content, published) VALUES (%s, %s, %s)
    #RETURNING * """, (post.title, post.content, post.published) )
    #new_post = cursor.fetchone()
    #conn.commit()
    print(current_user.email)
    
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # Sama mis ülal, ilusamini
    

    db.add(new_post)
    db.commit() # not sure why have to add+commit, but hey 
    db.refresh(new_post) # sama mis SQL: "RESPONDING *"
    return new_post

@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    posters = post_query.first()

    if posters == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")


    if posters.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                 detail=f"Not authorized duuud")
    
    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                 detail=f"Post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                 detail=f"Not authorized duuud")

    post_query.delete(synchronize_session=False) # Ei tea mis teeb, fastapi docs ütles et panna, vist ka default
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)
