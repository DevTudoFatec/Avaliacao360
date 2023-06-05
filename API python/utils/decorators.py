from functools import wraps
from flask import session, redirect, url_for

def login_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('padroes.home'))
        return route_function(*args, **kwargs)
    return decorated_function

def admin_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if session['perfil'] != 2:
            return redirect(url_for('padroes.menu_integrante'))
        return route_function(*args, **kwargs)
    return decorated_function

def integrante_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if session['perfil'] != 1:
            return redirect(url_for('padroes.menu_admin'))
        return route_function(*args, **kwargs)
    return decorated_function

def team_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if session['time'] == 0:
            return redirect(url_for('padroes.menu_integrante'))
        return route_function(*args, **kwargs)
    return decorated_function

def sprint_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if session['sprint'] == session['count_avaliacao']:
            return redirect(url_for('padroes.menu_integrante'))
        return route_function(*args, **kwargs)
    return decorated_function