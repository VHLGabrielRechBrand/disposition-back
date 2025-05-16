import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.file_api import router as file_router
from api.configuration_api import router as configuration_router
from api.auth_api import router as auth_router

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

allowed_origins = os.getenv("ALLOW_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(  # type: ignore
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_router)
app.include_router(configuration_router, prefix="/configuration")
app.include_router(auth_router, prefix="/auth")