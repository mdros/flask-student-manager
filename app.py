from flask import Flask


def create_flask_app(config_path: str) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config_path)

    from extensions.database import db

    db.init_app(app)

    from extensions import commands

    commands.init_app(app)

    from apis import api

    api.init_app(app)

    return app


app = create_flask_app("config.Config")

if __name__ == "__main__":
    app.run()
