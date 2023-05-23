from flask import render_template, session, Blueprint as bp
import json
from utils.decorators import login_required, admin_required

bp = bp('controles', __name__)

@bp.route("/controle_geral")
@login_required
@admin_required
def controle_geral():
  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  try:
        with open("data/times.json", "r") as f:
            times = json.load(f)
  except:
      times = []
  
  try:
      with open("data/turmas.json", "r") as f:
          turmas = json.load(f)
  except:
      turmas = []

    

  return render_template('admin/controle_geral.html', times=times, turmas=turmas, users=users, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@bp.route("/controle_turmas", methods=["GET", "POST"])
@login_required
@admin_required
def controle_turmas():
  try:
      with open("data/cadastro.json", "r") as f:
        users = json.load(f)
  except:
    users=[]

  try:
    with open("data/turmas.json", "r") as f:
      turmas = json.load(f)
  except:
    turmas=[]

  try:
    with open("data/times.json", "r") as f:
      times = json.load(f)
  except:
    times=[]

  return render_template('admin/controle_turmas.html', users=users, turmas=turmas, times=times, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@bp.route("/controle_times", methods=["GET", "POST"])
@login_required
@admin_required
def controle_times():
  try:
      with open("data/cadastro.json", "r") as f:
        users = json.load(f)
  except:
    users=[]

  try:
    with open("data/turmas.json", "r") as f:
      turmas = json.load(f)
  except:
    turmas=[]

  try:
    with open("data/times.json", "r") as f:
      times = json.load(f)
  except:
    times=[]

  return render_template('admin/controle_times.html', users=users, turmas=turmas, times=times, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])


@bp.route("/controle_sprints")
def controle_sprints():
  try:
      with open("data/cadastro.json", "r") as f:
        users = json.load(f)
  except:
    users=[]

  try:
    with open("data/turmas.json", "r") as f:
      turmas = json.load(f)
  except:
    turmas=[]

  try:
    with open("data/times.json", "r") as f:
      times = json.load(f)
  except:
    times=[]

  try:
    with open("data/projetos.json", "r") as f:
      projetos = json.load(f)
  except:
    projetos=[]

  turmas_with_projeto = [projeto["turma"] for projeto in projetos]
  turmas_select = [turma for turma in turmas if turma["codigo"] not in turmas_with_projeto]

  return render_template('admin/controle_sprints.html', turmas_select=turmas_select, users=users, turmas=turmas, times=times, projetos=projetos, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], sprint_index=session['sprint'])
