import os


from flask import Flask

from views.user import user
from App.models import db


def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)

    app.register_blueprint(blueprint=user, url_prefix='/user')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@127.0.0.1:3306/flask6'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 设置session密钥
    app.config['SECRET_KEY'] = 'secret_key'

    db.init_app(app=app)

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

    return app
