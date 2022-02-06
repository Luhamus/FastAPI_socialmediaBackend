from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db)
            , current_user: int = Depends(oauth2.get_current_user) ):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first() # Cheki seda, et ei proovi likeda posti mida ei eksisteeri
    if not post:
        raise HTTPException(status_code=status.HTTP404_NOT_FOUND,
          detail=f"The post with id {vote.id} that you are trying to like doesn't exsits")
    

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
         models.Vote.user_id == current_user.id)
    found_vote=vote_query.first()  # kui oled juba posti likenud, siis filter leiab, kui ei ole, siis ei leia
    
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.email} has alreadey liked the post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)    
        db.add(new_vote)
        db.commit()
        return {"Message":"Successfully liked Post"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user {current_user.email} has not liked the post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"Message":"Succesfulle Unliked the Post"}
        
            

        
             
