from flask import render_template, redirect, flash, url_for, request,jsonify, session, current_app as app
from app.forms import LoginForm, SignupForm, RecoveryForm
from . import auth
from app.models import UserData, UserModel
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import secure

secure_headers = secure.Secure()


@auth.after_request
def set_secure_headers(response):
    secure_headers.framework.flask(response)
    return response


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # return redirect(url_for('dashboard.main'))
    login_form = LoginForm()
    val_name = False
    val_cont = False
    context = {
        'login_form': login_form,
        'val_name': val_name,
        'val_cont': val_cont,
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = app.db_object.get_user(username)
        if user:
            user = user[0]
            password_from_db = user['password']
            if check_password_hash(password_from_db, password):
                user_data_db = app.db_object.get_user_data(user['idlogin'])[0]
                if user_data_db['validated'] == 'False':
                    flash('Su usuario aun no ha sido validado en el sistema')
                    flash('El proceso de validación se efectuara por parte de un administrador de INTEEGRA')
                    return redirect(url_for('home'))
                user_data = UserData(username, password, username)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo ' + str(user_data_db['name']).split()[0])
                session['username'] = username
                session['admin_session'] = False
                return redirect(url_for('dashboard.main'))
            else:
                context['val_cont'] = False
                flash('La información no coincide')
        else:
            flash('El usuario es incorrecto')
            context['val_name'] = True
    return render_template('auth/login.html', **context)


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form,
    }
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        users_db = app.db_object.get_user(username)

        if not users_db:
            print('aqui va')
            password_hash = generate_password_hash(password)
            user_new = app.db_object.set_user(username, password_hash)
            if user_new:
                user_new = user_new[0]
                print("////////////////////////////")
                print(user_new)
                app.db_object.set_user_data(
                    user_new['idlogin'], name=username, organization="Univalle")
                user_data = UserData(username, password_hash, username)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido!')
                return redirect(url_for('dashboard.main'))
        else:
            flash('El usuario ya existe.')

    return render_template('auth/signup.html', **context)


@auth.route('account-recovery', methods=['GET', 'POST'])
def recovery():
    recovery_form = RecoveryForm()
    context = {
        'recovery_form': recovery_form,
    }
    return render_template('auth/account_recovery.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa Pronto.')
    return redirect(url_for('auth.login'))

@auth.route('/saveData', methods=['GET', 'POST'])
def saveData():
    strategy_name = request.form.get("strategy_name")
    chain_type = request.form.get("type")
    id_user = request.form.get("user")
    anio= request.form.get("año")
    all_data= request.form.get("all_data")
    data_indicators= request.form.get("data_indicators")

    print(f"id_user:  {id_user} , strategy_name: {strategy_name}, anio: {anio}, chain_type: {chain_type}, all_data: {all_data} , data_indicators: {data_indicators}")
    resultado = app.db_object.set_save_strategy(strategy_name, id_user, chain_type, anio, all_data, data_indicators)
    if resultado:
        flash("Scenary add successfully")
        print("succes")
        return jsonify({"mensaje": "success"})
    else:
        print("failure")
        return jsonify({"mensaje": "failure"})