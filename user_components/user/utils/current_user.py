import jwt


async def get_current_user(request):
    try:
        token = request.headers["Authorization"]
        data = jwt.decode(token, request.app.ctx.settings.secret_key)
        user = data["public_id"]
        return str(user["id"])
    except Exception:
        return 0
