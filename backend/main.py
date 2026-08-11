from fastapi import FastAPI

app = FastAPI(title="AI-Interview")

app.include_router()

@app.get("/")
def read_root():
    return {"Hello": "World"}

