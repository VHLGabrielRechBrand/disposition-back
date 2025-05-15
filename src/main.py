from fastapi import FastAPI
from api.file_api import router as file_router
from api.configuration_api import router as configuration_router
from api.auth_api import router as auth_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(  # type: ignore
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(file_router)
app.include_router(configuration_router, prefix="/configuration")
app.include_router(auth_router, prefix="/auth")