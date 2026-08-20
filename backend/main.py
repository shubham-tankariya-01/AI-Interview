from routes.interview import interview_router
from fastapi import FastAPI
import logging

#internals
from core.database import engine
from models.base import Base
from routes.interview import interview_router
from routes.webSocket import ws_router
import models.transcript


#to also see info logs in terminal or whatever using (python logger by def hides info logs)
logging.basicConfig(level=logging.INFO)

#at starting connecting with db and creating tables if not exists
Base.metadata.create_all(bind=engine)

import asyncio
import contextlib
from faster_whisper import WhisperModel
from services.stt import (
    WHISPER_MODEL, WHISPER_DEVICE, WHISPER_COMPUTE, WHISPER_THREADS,
    load_vad_model, VADProcessor
)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading ML models for local STT pipeline...")
    async def _whisper():
        return await asyncio.to_thread(
            WhisperModel,
            model_size_or_path=WHISPER_MODEL,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE,
            cpu_threads=WHISPER_THREADS,
        )

    async def _vad():
        return VADProcessor(await asyncio.to_thread(load_vad_model))

    whisper, vad = await asyncio.gather(_whisper(), _vad())
    app.state.whisper_model = whisper
    app.state.vad_model = vad
    print("Models loaded successfully.\n")
    yield
    del app.state.whisper_model
    del app.state.vad_model

#application
app = FastAPI(title="AI-Interview", lifespan=lifespan)


#applying router
app.include_router(interview_router,prefix="/interview",tags=["interview"])

#ws-routers
app.include_router(ws_router , prefix="/ws/interview" , tags=["ws for interview"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
