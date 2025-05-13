from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.scan_service import process_scan, get_collections, get_documents_from_collection, delete_document_from_collection

router = APIRouter()


@router.post("/scan-file")
async def scan_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".pdf")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, JPEG, PNG, and PDF files are allowed.")
    return await process_scan(file)


@router.get("/collections")
async def list_collections():
    collections = await get_collections()
    return JSONResponse(content={"collections": collections})


@router.get("/collection/{collection_name}")
async def list_documents(collection_name: str):
    documents = await get_documents_from_collection(collection_name)
    return JSONResponse(content={"documents": documents})


@router.delete("/collection/{collection_name}/{document_id}")
async def delete_document(collection_name: str, document_id: str):
    return await delete_document_from_collection(collection_name, document_id)
