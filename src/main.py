from fastapi import FastAPI
from api.scan import router as scan_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(  # type: ignore
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(scan_router)