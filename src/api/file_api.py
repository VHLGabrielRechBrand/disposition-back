from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from utils.custom_responses import CustomJSONResponse
from services.file_service import FileService

router = APIRouter()
service = FileService()


@router.post("/scan-file")
def scan_file(file: UploadFile = File(...), prompt: str = Form("")):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".pdf")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, JPEG, PNG, and PDF files are allowed.")
    return service.process_scan(file, prompt)


@router.get("/collections")
def list_collections():
    collections = service.get_collections()
    return CustomJSONResponse(content={"collections": collections})


@router.get("/collection/{collection_name}")
def list_documents(collection_name: str):
    documents = service.get_documents_from_collection(collection_name)
    return CustomJSONResponse(content={"documents": documents})


@router.get("/collection/{collection_name}/{document_id}")
def get_document(collection_name: str, document_id: str):
    document = service.get_document_by_id(collection_name, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return CustomJSONResponse(content=document)


@router.delete("/collection/{collection_name}/{document_id}")
def delete_document(collection_name: str, document_id: str):
    return service.delete_document_from_collection(collection_name, document_id)
