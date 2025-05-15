import json
from datetime import datetime
from src.utils.custom_responses import DateTimeEncoder, CustomJSONResponse

def test_datetime_encoder_serializes_datetime():
    now = datetime(2025, 5, 15, 12, 30, 45)
    encoded = json.dumps({"date": now}, cls=DateTimeEncoder)
    assert '"2025-05-15T12:30:45"' in encoded

def test_custom_json_response_renders_datetime():
    now = datetime(2025, 5, 15, 12, 30, 45)
    content = {"timestamp": now, "message": "test"}
    response = CustomJSONResponse(content=content)
    rendered = response.body.decode("utf-8")

    assert '"timestamp": "2025-05-15T12:30:45"' in rendered
    assert '"message": "test"' in rendered
