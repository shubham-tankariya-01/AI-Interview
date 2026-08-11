from routes.interview import interview_router
from fastapi import FastAPI
#internals
from core.database import engine
from models.base import Base
from routes.interview import interview_router
from routes.webSocket import ws_router


#at starting connecting with db and creating tables if not exists
Base.metadata.create_all(bind=engine)

#application
app = FastAPI(title="AI-Interview")


#applying router
app.include_router(interview_router,prefix="/interview",tags=["interview"])

#ws-routers
app.include_router(ws_router , prefix="/ws/interview" , tags=["ws for interview"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
