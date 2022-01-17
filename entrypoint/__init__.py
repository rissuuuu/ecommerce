from sanic import Sanic

app = Sanic("Sharemarket", register=True)

from entrypoint.bootstrap import init_database
from user_components.user.entrypoints.routes import user


async def create_app(settings):
    app.blueprint(user)
    db = init_database(settings)
    app.ctx.settings = settings
    app.ctx.db = db
    return app
