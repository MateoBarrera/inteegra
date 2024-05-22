"""INTEGRA 2023 Platform Server Config parameters file

this file contains the configures parameters used by the server.
"""
import os
from datetime import timedelta


class Config:
    """Flask server Setup parameters
    """
    # Session Cookie
    SECRET_KEY = 'SUPER SECRET'
    TIMEZONE = 'US/Eastern'
    # SQLAlchemy config
    DB_URI = os.path.abspath('app/sqlite/TestDB.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS = True

    # MAIL CONFIG
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'web.noreply.app@gmail.com'
    MAIL_ADMIN = 'mateo.barrera@correounivalle.edu.co'
    MAIL_DEFAULT_SENDER = 'INTEEGRA'
    MAIL_PASSWORD = 'schemiuyrgvxzdhm'

    # ADMIN
    FLASK_ADMIN_SWATCH = 'cerulean'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)
