from flask import render_template, request, redirect, url_for, session, Blueprint as bp
import json
from utils.decorators import login_required, admin_required


bp = bp('dashboards', __name__)

@login_required
@admin_required
@bp.route("/dashboards_operacionais")
def dashboards_operacionais():
  return render_template('admin/dashboards_operacionais.html')

@login_required
@admin_required
@bp.route("/dashboards_gerenciais")
def dashboards_gerenciais():
  return render_template('admin/dashboards_gerenciais.html')