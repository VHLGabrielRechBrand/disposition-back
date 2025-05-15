import os
import json
import pytesseract
from PIL import Image
from tempfile import NamedTemporaryFile
from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from pdf2image import convert_from_bytes
from datetime import datetime

from .base_service import BaseService

class FileService(BaseService):
    def process_scan(self, file: UploadFile, user_prompt: str):
        contents = file.file.read()
        extension = os.path.splitext(file.filename)[1].lower()
        size = len(contents)

        try:
            if extension == ".pdf":
                images = convert_from_bytes(contents)
                extracted_text = ""
                for image in images:
                    extracted_text += pytesseract.image_to_string(image, lang='por') + "\n"
            else:
                with NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
                    temp_file.write(contents)
                    temp_path = temp_file.name
                image = Image.open(temp_path)
                extracted_text = pytesseract.image_to_string(image, lang='por')
                os.remove(temp_path)

            prompt = f"""
            You are a document organization assistant. Your task is to identify the type of document and extract the main structured data in JSON format.
            Focus on the following instructions:
            \"\"\"
            {user_prompt}
            \"\"\"

            Document text:
            \"\"\"
            {extracted_text}
            \"\"\"

            Respond with JSON in the following format:
            {{
              "document_type": "simple_snake_case_name",
              "fields": {{
                "field1": "value1",
                "field2": "value2"
              }}
            }}

            Respond with JSON only, without explanations.
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )

            json_str = response.choices[0].message.content
            document = json.loads(json_str)

            doc_type = document["document_type"]
            fields = document["fields"]

            collection = self.db[doc_type]

            scanned_at = datetime.utcnow()

            collection.insert_one({
                "fields": fields,
                "raw_text": extracted_text,
                "filename": file.filename,
                "size": size,
                "extension": extension,
                "scanned_at": scanned_at,
                "user_prompt": user_prompt
            })

            return JSONResponse(content={
                "status": "success",
                "collection": doc_type,
                "data": fields
            })

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal processing error: {str(e)}")

    def get_collections(self):
        return self.db.list_collection_names()

    def get_documents_from_collection(self, collection_name: str):
        collection = self.db[collection_name]
        documents = collection.find({})
        return [{**doc, "_id": str(doc["_id"])} for doc in documents]

    def get_document_by_id(self, collection_name: str, document_id: str):
        try:
            oid = ObjectId(document_id)
            collection = self.db[collection_name]
            document = collection.find_one({"_id": oid})
            if document:
                document["_id"] = str(document["_id"])
            return document
        except Exception as e:
            print(f"Erro inesperado ao buscar documento: {e}")
            return None

    def delete_document_from_collection(self, collection_name: str, document_id: str):
        try:
            result = self.db[collection_name].delete_one({"_id": ObjectId(document_id)})

            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Document not found")

            return JSONResponse(content={"status": "success", "message": "Document deleted"})

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")
