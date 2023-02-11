from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import oauth2,models,database,schema
from sqlalchemy.orm import Session

router=APIRouter(prefix="/vote",tags=["Vote"])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schema.vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):

    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{vote.post_id}"
                                                                         f"does not exits")

    vote_query=db.query(models.vote).filter(models.vote.post_id==vote.post_id,models.vote.user_id==current_user.id)
    found_vote=vote_query.first()

    if(vote.dir==1):

        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"users{current_user.id} has "
                                                                            f"already voted on post {vote.post_id}")
        new_vote=models.vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully deleted vote"}



