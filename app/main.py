from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine

import app.models

from .routes import router


app = FastAPI(
    title="CodeVector Assignment"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

Base.metadata.create_all(
    bind=engine
)

app.include_router(router)


@app.get("/")
def home():

    return {

        "message": "CodeVector Backend Running"

    }