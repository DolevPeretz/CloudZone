import json

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "Access-Control-Allow-Methods": "GET,PUT,DELETE,OPTIONS",
}

def resp(status: int, payload: dict):
    return {
        "statusCode": status,
        "headers": CORS_HEADERS,
        "body": json.dumps(payload),
    }
