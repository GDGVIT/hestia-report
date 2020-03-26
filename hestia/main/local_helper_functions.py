from rest_framework.response import Response
from .handling_jwt_tokens import verifying_and_decoding_token


def authorization(request):
    if 'Authorization' not in request.headers:
        Response.status_code = 403
        return Response({"status": "blocked", 
                        "message": "Authentication credentials not provided",
                        "payload": ""
                        })


def getting_user(request):
    token = request.headers.get('Authorization')
    payload = verifying_and_decoding_token(token)
    return payload
