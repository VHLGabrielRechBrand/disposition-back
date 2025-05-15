import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header, APIRouter
from google.oauth2 import id_token
from google.auth.transport import requests

load_dotenv()

router = APIRouter()
app = FastAPI()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

def verify_google_token(token: str):
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        user_id = id_info['sub']
        email = id_info.get('email')
        return id_info
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")

@router.post("/google")
async def google_auth(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization[len("Bearer "):]
    user_info = verify_google_token(token)
    return {"message": "User authenticated", "user": user_info}
