from .base_service import BaseService

class ConfigurationService(BaseService):
    def update_model_for_user(self, user_id: str, model_name: str):
        config_collection = self.db["user_configuration"]
        result = config_collection.update_one(
            {"user_id": user_id},
            {"$set": {"model": model_name}},
            upsert=True
        )
        return {"status": "success", "model": model_name}
