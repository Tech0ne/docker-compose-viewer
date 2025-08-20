from flask import Flask


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .main import main as main_blueprint

        app.register_blueprint(main_blueprint)

    @app.context_processor
    def set_github_url():
        return {"github_url": "https://github.com/tech0ne/docker-compose-viewer"}

    return app
