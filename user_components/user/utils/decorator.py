from functools import wraps

import jwt
from sanic import response

from entrypoint import settings

secret_key = settings.settings_factory().secret_key


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"]
            if not token:
                return response.json({"message": "Token is missing !!"}, 401)
            try:
                data = jwt.decode(token, secret_key, algorithms="HS256")
                email = data["email"]
                # phone = data["phone_number"]
                # user = request.ctx.session[data["public_id"]]
                if email:
                    responses = await f(request, *args, **kwargs)
                    return responses
                else:
                    return response.json({"message": "Please Log in Again!!"}, 403)

            except Exception as e:
                return response.json({"message": f"{e}"}, 403)

        return decorated_function

    return decorator


def is_admin():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            token = request.headers["Authorization"]
            data = jwt.decode(token, secret_key, algorithms="HS256")
            is_admin = data["is_admin"]
            if is_admin is True:
                responses = await f(request, *args, **kwargs)
                return responses
            else:
                return response.json({"error": "You do not have permission"}, 403)

        return decorated_function

    return decorator


def is_customer():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            token = request.headers["Authorization"]
            data = jwt.decode(token, secret_key, algorithms="HS256")
            is_customer = data["is_customer"]
            if is_customer is True:
                responses = await f(request, *args, **kwargs)
                return responses
            else:
                return response.json({"error": "You do not have permission"}, 403)

        return decorated_function

    return decorator


def is_seller():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            token = request.headers["Authorization"]
            data = jwt.decode(token, secret_key, algorithms="HS256")
            is_seller = data["is_seller"]
            if is_seller is True:
                responses = await f(request, *args, **kwargs)
                return responses
            else:
                return response.json({"error": "You do not have permission"}, 403)

        return decorated_function

    return decorator
