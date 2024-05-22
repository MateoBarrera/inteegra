"""Mail file

This module include methods for send mail from. 

@Author: Mateo Barrera
@Date: 12-07-2022  
"""
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    """_summary_

    Args:
        app (_type_): _description_
        msg (_type_): _description_
    """
    with app.app_context():
        mail.send(msg)


def send_email(to, context):
    """_summary_

    Args:
        to (_type_): _description_
        context (_type_): _description_
    """
    app = current_app._get_current_object()
    msg = Message("Integra: " + context['type_contact'],
                  recipients=[to, app.config["MAIL_ADMIN"]],
                  sender=app.config["MAIL_DEFAULT_SENDER"])
    msg.html = render_template('home/email_template.html', **context)
    print('Ready to send message...')
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
