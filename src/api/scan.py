from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.scan_service import process_scan

router = APIRouter()

@router.post("/scan-file")
async def scan_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Only image files (.jpg, .jpeg, .png) are supported.")
    return await process_scan(file)