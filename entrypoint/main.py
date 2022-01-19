import asyncio

from sanic import response
from sanic_session import InMemorySessionInterface, Session

from entrypoint import create_app, settings

app = asyncio.run(create_app(settings.settings_factory()))
app.config.FALLBACK_ERROR_FORMAT = "json"
app.config.DEBUG = True
app.config.AUTO_RELOAD = True

session = Session(app, interface=InMemorySessionInterface())


@app.main_process_start
async def start_db(request, loop):
    await app.ctx.db.connect()
    print("DB Connected")


@app.main_process_stop
async def stop_db(request, loop):
    await app.ctx.db.disconnect()
    print("DB Disconnected")


@app.middleware("request")
async def verify_user(request):
    token = None
    if "sign_in" in request.headers:
        if request.url == settings.settings_factory().SIGN_IN_URL:
            print("matched")
            pass
        else:
            return response.json("Invalid url for login")
    elif "sign_up" in request.headers:
        if request.url == settings.settings_factory().SIGN_UP_URL:
            print("matched")
            pass
        else:
            return response.json("Invalid url for register")
    elif "send_otp" in request.headers:
        if request.url == settings.settings_factory().SEND_OTP:
            print("matched")
            pass
    elif "activate_user" in request.headers:
        if request.url == settings.settings_factory().ACTIVATE_USER:
            print("matched")
            pass
    elif "resend_otp" in request.headers:
        if request.url == settings.settings_factory().RESEND_URL:
            print("matched")
            pass
    else:
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return response.json({"message": "Token is missing !!"}, 401)
        try:
            import jwt

            secret_key = settings.settings_factory().secret_key
            data = jwt.decode(token, secret_key, algorithms="HS256")
            email = data["email"]
            if email:
                if (
                    request.url == settings.settings_factory().POST_FUNDAMENTAL_URL
                    and request.method == "POST"
                ):
                    if data["is_admin"]:
                        pass
                    else:
                        return response.json({"message": "Not Authorized"}, 403)
                pass
            else:
                return response.json({"message": "Please Log in Again!!"}, 403)
        except Exception as e:
            return response.json({"message": f"{e}"}, 403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, auto_reload=True)
