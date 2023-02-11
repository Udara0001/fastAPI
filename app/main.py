from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
print(settings.database_username)





#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]#"https://www.google.com"



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "welcome to my first API dddd "}


#class post(BaseModel):
   # title :str
    #content: str
    #published : bool=True



#my_data=[{"title":"udara","content":"methruwan","id":1},
         #{"title":"Minidu","content":"nilupul","id":2}]


#def find_post(id):
    #for p in my_data:
        #if p["id"]==id:
            #return p


#def find_index_id(id):
    #for i,p in enumerate(my_data):
        #if p["id"]== id:
            #return i





#@app.get("/sqlalcamy")  ------ get the post from ORM ------
#def test_post(db: Session = Depends(get_db)):
    #posts=db.query(models.Post).all()
    #return {'data':posts}







