from fastapi import  APIRouter,Depends,HTTPException,status,Response
from  sqlalchemy.orm import  Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from  .. import database,schema,models,utills,oauth2


router=APIRouter(tags=['Authentication'])

@router.post("/login",response_model=schema.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(database.get_db)):

    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credential")

    if not utills.verify(user_credentials.password,user.passwaord):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credential")

    access_token= oauth2.create_acess_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}