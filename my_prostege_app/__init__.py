import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from my_prostege_app import web_student_curses_app


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object('config.Config')
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(web_student_curses_app.bp)

    return app


# Initialize SQLAlchemy
db = SQLAlchemy()

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
