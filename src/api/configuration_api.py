from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enumeration.model_enum import OpenAIModel
from services.configuration_service import ConfigurationService
from functools import lru_cache
from typing import List

router = APIRouter()
service = ConfigurationService()

class ModelUpdateRequest(BaseModel):
    user_id: str
    model: OpenAIModel


@lru_cache()
def get_available_models() -> List[str]:
    return [model.value for model in OpenAIModel]


@router.get("/available-models")
def available_models():
    return {"models": get_available_models()}


@router.post("/set-model")
def set_openai_model(request: ModelUpdateRequest):
    try:
        result = service.update_model_for_user(request.user_id, request.model.value)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating model: {str(e)}")