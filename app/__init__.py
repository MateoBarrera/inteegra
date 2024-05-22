"""INTEGRA 2023 Platform Server Initialization file

this file allows to import all the dependencies for the platform initialization.
"""
import os.path as op
from flask.app import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from .admin import UserModelView, MyAdminIndexView, MyFileAdminView, DataModelView
from .config import Config
from .models import UserModel
from .auth import auth
from .dashboard import dashboard
from flask_admin import Admin
from flask_compress import Compress
from flask_sitemap import Sitemap
from flask_minify import Minify

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
ext = Sitemap()
mail = Mail()
admin = Admin(name='Inteegra', index_view=MyAdminIndexView(),
              template_mode='bootstrap4')
db = SQLAlchemy()


@login_manager.user_loader
def load_user(user_id):
    """Handler for flask server implementation of loginManager.

    Args:
        user_id (str): user identification for the session within the platform.

    Returns:
        UserModel: Information model for the user session
    """
    return UserModel.query(user_id)


def create_app():
    """App implementation
    'Constructor' of the flask app type object and its initialization.

    Returns:
        app: flask server instance
    """
    app = Flask(__name__)
    Compress(app)
    Minify(app=app, html=True, js=True, cssless=True)

    app.config.from_object(Config)
    login_manager.init_app(app)
    db.init_app(app)

    admin.init_app(app)
    with app.app_context():
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)

        try:
            array = Base.classes.keys()
            admin.add_view(UserModelView(Base.classes.get('login'), db.session, name='Login', menu_icon_type='fa',
                                         menu_icon_value='fa-key', menu_class_name='nav-item'))
            admin.add_view(DataModelView(Base.classes.get('users'), db.session, name='Users', menu_icon_type='fa',
                                         menu_icon_value='fa-users', menu_class_name='nav-item'))
            array.remove('login')
            array.remove('users')
            admin.add_category('Source Data', class_name='nav-item', icon_type='fa',
                               icon_value='fa-database')
            for element in array:
                admin.add_view(
                    DataModelView(Base.classes.get(element), db.session, element.replace('_', ' ').capitalize(),
                                  category='Source Data', menu_icon_type='fa', menu_icon_value='fa-table'))

        except AttributeError as e:
            print(e)
        path = op.join(op.dirname(__file__), 'static')
        admin.add_view(MyFileAdminView(path, '/Data/', name='Upload Data'))

    ext.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)

    return app
