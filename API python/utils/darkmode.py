from flask import redirect, url_for, session, Blueprint as bp
from utils.decorators import login_required

bp = bp('darkmode', __name__)


@login_required
@bp.route("/darkmode_on")
def darkmode_on():

  session['darkmode'] = True

  if session['perfil'] == 1:
    return redirect(url_for('padroes.menu_integrante'))
  else:
    return redirect(url_for('padroes.menu_admin'))


@login_required
@bp.route("/darkmode_off")
def darkmode_off():

  session['darkmode'] = False

  if session['perfil'] == 1:
    return redirect(url_for('padroes.menu_integrante'))
  else:
    return redirect(url_for('padroes.menu_admin'))