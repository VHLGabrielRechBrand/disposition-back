from fastapi import FastAPI
from api.scan import router as scan_router

app = FastAPI()
app.include_router(scan_router)