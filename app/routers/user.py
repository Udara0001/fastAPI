from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schema,utills
from ..database import get_db



router=APIRouter(
    prefix="/users",
    tags=["Users"]
)







#----------------------users table------------------------------


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.userout)
def userspost(user:schema.usercreate,db: Session = Depends(get_db)):

    hashed_password = utills.hash(user.passwaord)
    user.passwaord = hashed_password

    new_user = models.User(**user.dict())  # (title=post.title,content=post.content,published=post.published)#(**Post.dic())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#-----------------------------------------------------------------------


@router.get("/{id}",response_model=schema.userout)
def user_get(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is not id {id} like that")

    return user
