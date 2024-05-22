"""INTEGRA 2023 Platform Server Main File

This file is part of the INTEGRA 2023 platform flask server. It integrates the configuration and initialization
classes of the server, additionally it attends the HTTP requests for the root address and the home module.

:Author: Mateo Barrera
:Co-author: Alex Pinchao

:Date: 12-07-2022
"""

from datetime import datetime
import unittest

from flask import (
    request,
    make_response,
    render_template,
    redirect,
    session,
    Response,
    flash,
)
from app import create_app
from app.email import send_email
from flask_login import current_user
from app.database import SQLConnector

app = create_app()
app.db_object = SQLConnector()


# users = db.table('users', db.metadata, autoload=True, autoload_with=db.engine)


@app.cli.command()
def test():
    """OPTIONAL
    Construction of automatic integration tests
    """
    tests = unittest.TestLoader().discover("test")
    unittest.TextTestRunner().run(tests)


# Si se require inicializar datos de cookies se pueden establecer desde este punto
""" @app.before_first_request
def initialize():
    session.clear() """


@app.context_processor
def inject_template_scope():
    """
    The inject_template_scope function is used to inject variables into the template scope.
    This allows us to use these variables in our templates without having to pass them through
    the view function.
    This is useful for things like global settings, or functions that are
    used across multiple views.

    :return: A dictionary of functions that are available in the template scope
    """
    injections = dict()

    def cookies_check():
        value = request.cookies.get("cookie_consent")
        return value == "true"

    injections.update(cookies_check=cookies_check)
    return injections


@app.route("/")
def index():
    """
    The index function is the first function that runs when a user visits the website.
    It redirects them to /home, which is where they will be able to see all of their
    current and past orders.

    :return: A response object that redirects the user to the home page
    """
    user_ip = request.remote_addr
    response = make_response(redirect("/home"))
    session["user_ip"] = user_ip
    return response


# Desarrollo frontend para la vista de error
# Integración y respuesta a otros errores HTTP
@app.errorhandler(404)
def not_found(error):
    """
    The not_found function is a flask error handler that renders the 404.html template when a resource does not exist
    and never existed.

    :param error: Pass the error message to the template
    :return: The 400 html template
    """
    return render_template("404.html", error=error)


@app.errorhandler(500)
def server_error(error):
    """
    The server_error function is a Flask error handler that renders the 500.html template when an internal server error
    occurs.

    :param error: Pass the error message to the template
    :return: The 500 html template
    """
    return render_template("500.html", error=error)


@app.route("/home", methods=["GET", "POST"])
def home():
    """
    The home function is the first function that will be called when a user visits the home page.
    It will render the home template, which contains all of our static content for this page.

    :return: The home page
    """
    text_module_db = (
        "En este módulo se recopila la información de las variables y los indicadores de "
        "eficiencia energética asociados a los procesos de generación, distribución y uso final de la "
        "energía eléctrica en Colombia, visualizando su tendencia histórica."
    )
    text_module_calc = (
        "En este módulo se presenta la especificación del modelo de proyección para las variables, "
        "empleadas en la evaluación de estrategias de eficiencia energética del sector eléctrico "
        "en Colombia. También se incluye la visualización de los resultados de proyección con la "
        "tendencia histórica de las variables hasta el 2030."
    )
    text_module_anl = (
        "En este módulo se construyen y evalúan las estrategias de eficiencia energética asociadas al "
        "sector eléctrico colombiano, mediante criterios económicos, ambientales y energéticos, "
        "permitiendo definir las estrategias más viables para el país, según el año de análisis."
    )

    if current_user.is_authenticated:
        user_ip = session.get("user_ip")
        username = current_user.id
        context = {
            "user_ip": user_ip,
            "username": username,
            "anonymous": False,
            "text_module_db": text_module_db,
            "text_module_calc": text_module_calc,
            "text_module_anl": text_module_anl,
        }
        return render_template("module/main.html", **context)
    context = {
        "anonymous": True,
        "user_ip": "UserIp",
        "text_module_db": text_module_db,
        "text_module_calc": text_module_calc,
        "text_module_anl": text_module_anl,
    }
    if request.cookies.get("cookie_consent"):
        pass
    return render_template("home/home.html", **context)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact Form method

    Returns:
        server response: platform contact form
    """
    context = {
        "anonymous": True,
        "user_ip": "UserIp",
    }
    if request.method == "POST":
        contact_data = request.form.to_dict()
        contact_context = {
            "mail": contact_data.get("mail"),
            "name": contact_data.get("name"),
            "identifier": contact_data.get("identifier", "+57"),
            "number": contact_data.get("number"),
            "organization": contact_data.get("organization", "NA"),
            "message": contact_data.get("message", "NA"),
            "type_contact": "contacto",
            "date": datetime.now().strftime("%x"),
            "hour": datetime.now().strftime("%X"),
        }
        send_email(contact_data.get("mail"), contact_context)
        flash("Mensaje enviado")

    if current_user.is_authenticated:
        user_ip = session.get("user_ip")
        username = current_user.id
        context = {
            "user_ip": user_ip,
            "username": username,
            "anonymous": False,
        }
    return render_template("home/contact.html", **context)


@app.route("/email", methods=["GET"])
def email():
    """
    The email function is used to email the admin of the website.
    It uses a template for the body of the email, and it sends it using Flask-Mail.
    The function takes no arguments, but uses data from contact_data (a global variable).

    :return: The html template to be sent by email
    """

    context = {
        "mail": "contact_data.get('mail')",
        "name": "contact_data.get('name')",
        "identifier": "contact_data.get('identifier', '+57')",
        "number": "contact_data.get('number')",
        "organization": "contact_data.get('organization', 'NA')",
        "message": "contact_data.get('message', 'NA')",
        "type_contact": "contacto",
        "date": datetime.now().strftime("%x"),
        "hour": datetime.now().strftime("%X"),
    }

    return render_template("home/email_template.html", **context)


# DONE
@app.route("/robots.txt")
def noindex():
    """
    The noindex function is used to restrict the activity of search engine crawlers and stop their access to app.

    :return: A text plain response
    """
    r = Response(
        response="User-Agent: *\nAllow: /\nAllow: /dashboard/",
        status=200,
        mimetype="text/plain",
    )
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
