from django.conf import settings

import jwt


def verifying_and_decoding_token(token):
    try:
        return {
            "status": "success",
            "message":jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            }
    except Exception as e:
        return {
            "status": "error", 
            "message":e
            }


