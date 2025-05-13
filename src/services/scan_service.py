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

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mongo = MongoClient("mongodb://localhost:27017/")
db = mongo["disposition"]


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
        collection = db[doc_type]
        collection.insert_one({
            "fields": fields,
            "raw_text": extracted_text,
            "filename": file.filename
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
