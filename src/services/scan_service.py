import os
import json
import pytesseract
from PIL import Image
from tempfile import NamedTemporaryFile
from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mongo = MongoClient(os.getenv("DATABASE_URL"))
db = mongo[os.getenv("DATABASE_NAME")]


async def process_scan(file: UploadFile):
    with NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        contents = await file.read()
        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        image = Image.open(temp_path)
        extracted_text = pytesseract.image_to_string(image, lang='por')

        prompt = f"""
        You are a document organization assistant. Your task is to identify the type of document and extract the main structured data in JSON format.

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

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        json_str = response.choices[0].message.content
        document = json.loads(json_str)

        doc_type = document["document_type"]
        fields = document["fields"]

        size = len(contents)  # em bytes
        extension = os.path.splitext(file.filename)[1].lower()

        collection = db[doc_type]
        collection.insert_one({
            "fields": fields,
            "raw_text": extracted_text,
            "filename": file.filename,
            "size": size,
            "extension": extension
        })

        return JSONResponse(content={
            "status": "success",
            "collection": doc_type,
            "data": fields
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal processing error: {str(e)}")

    finally:
        os.remove(temp_path)


async def get_collections():
    return db.list_collection_names()


async def get_documents_from_collection(collection_name: str):
    collection = db[collection_name]
    documents = collection.find({})
    return [{**doc, "_id": str(doc["_id"])} for doc in documents]


async def delete_document_from_collection(collection_name: str, document_id: str):
    try:
        result = db[collection_name].delete_one({"_id": ObjectId(document_id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Document not found")

        return JSONResponse(content={"status": "success", "message": "Document deleted"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")