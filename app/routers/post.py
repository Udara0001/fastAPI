from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schema,oauth2
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func


router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)




#@router.get("/",response_model=List[schema.post])
@router.get("/",response_model=List[schema.Postout])
def get_post(db: Session = Depends(get_db),current_user:int=Depends(oauth2. get_current_user),
             limit:int=10,skip:int=0,search:Optional[str]=""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()#.1.filter(models.Post.owner_id==current_user.id).all()
    #1.print(posts)
    posts =db.query(models.Post,func.count(models.vote.post_id).label("votes")).\
        join(models.vote,models.vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id)\
        .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    return posts



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
#def post_data(post: post):

    #cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *;""",
                   #(post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
def post_data(post:schema.Postcreste,db: Session = Depends(get_db),current_user:int=Depends(oauth2. get_current_user)) :
    print(current_user)
    new_post=models.Post(owner_id=current_user.id,**post.dict())#(title=post.title,content=post.content,published=post.published)#(**Post.dic())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post


#@app.get("/posts/lates")
#def lates_post():
   # post=my_data[len(my_data)-1]
    #return {"details": post}

#@router.get("/{id}",response_model=schema.Post)

@router.get("/{id}",response_model=schema.Postout)
#def get_post(id:int,):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    #post = cursor.fetchone()
    #print(post)

def get_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2. get_current_user)):

    #post=db.query(models.Post).filter(models.Post.id==id).first()

    post = db.query(models.Post, func.count(models.vote.post_id).label("votes")). \
        join(models.vote, models.vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id) \
        .filter(models.Post.id==id).first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is not id {id} like that")
       # respones.status_code =status.HTTP_404_NOT_FOUND
        #return {"Message":f"There is not id {id} like that"}
    return  post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
#def delete_post(id:int):

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)),)
    #delete = cursor.fetchone()
    #conn.commit()
    #index=find_index_id(id)

    #if delete == None:
def delete_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2. get_current_user)):
     post_query = db.query(models.Post).filter(models.Post.id == id)

     post=post_query.first()

     if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"This id:{id} does not exite")

     if post.owner_id !=current_user.id:
         raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                             detail="Not authorized to perform requested")


     post_query.delete(synchronize_session=False)
     db.commit()
     #my_data.pop(index)
     return  Response(status_code=status.HTTP_204_NO_CONTENT)






@router.put("/{id}",response_model=schema.Post)
#def update_posts(id:int,post:post):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s ,published = %s WHERE id = %s RETURNING *""",
                   #(post.title,post.content,post.published,(str(id))))
    #updated_post = cursor.fetchone()
    #conn.commit()
    #index = find_index_id(id)
def update_posts(id:int,update_post:schema.Postcreste,db: Session = Depends(get_db),current_user:int=Depends(oauth2. get_current_user)):
     post_quary = db.query(models.Post).filter(models.Post.id == id)
     post=post_quary.first()
    #if updated_post == None:
     if post == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This id:{id} does not exite")

     if post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Not authorized to perform requested")

     # post_dict=post.dict()
    #post_dict["id"]=id
    #my_data[index]=post_dict
     post_quary.update(update_post.dict(),synchronize_session=False)
     db.commit()
     return post_quary.first()