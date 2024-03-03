import jwt
from datetime import datetime, timedelta
from functools import wraps

secret_key = "1234"  # Cambia esto a una cadena segura y única en tu aplicación

def generate_token(user_id, expiration=10000):
    expiration_time = datetime.utcnow() + timedelta(minutes=expiration)
    payload = {
        "user_id": user_id,
        "exp": expiration_time
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def verify_token(func):
    @wraps(func)
    def wrapper(obj, info, *args, **kwargs):
        

        try:
            authorization_header = info.context['request'].headers.get('Authorization', '').split(' ')[1]
            print(authorization_header)
            payload = jwt.decode(authorization_header, secret_key, algorithms=["HS256"])
            info.context["user_id"] = payload["user_id"]
            return func(obj, info, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            ValueError("token expirado")
        except Exception as e:
            raise ValueError(f"Error al verificar el token: {str(e)}") 

    return wrapper
