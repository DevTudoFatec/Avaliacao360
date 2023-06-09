from flask import render_template, session, Blueprint as bp, request, redirect, url_for
import json
from utils.decorators import login_required, admin_required

bp = bp('controles', __name__)

@bp.route("/controle_integrantes", methods=["GET", "POST"])
@login_required
@admin_required
def controle_integrantes():
  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
      for user in users:
        if user['email'] == "admin":
          users.remove(user)
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

  editing=False
  editing_time=False
  editing_perfil=False
  confirm_delete=False
  index=None

  edited_turma=None
  edited_time=None
  times_turma=None

  if "edit" in request.form:
    index = int(request.form.get("index"))
    editing=True

  elif "save_turma" in request.form:
    index = int(request.form.get("index"))
    editing_time=True

    times_turma = [time for time in times if time['turma'] == request.form.get("edited_turma")]
    edited_turma = [turma['nome'] for turma in turmas if turma['codigo'] == request.form.get("edited_turma")][0]

    session['edited_turma'] = request.form.get("edited_turma")            

  elif "save_time" in request.form:
    index = int(request.form.get("index"))
    edited_turma = request.form.get("edited_turma")
    editing_perfil=True

    edited_time = [time['nome'] for time in times if time['codigo'] == int(request.form.get("edited_time"))][0]

    session['edited_time'] = request.form.get("edited_time")

  elif "save_perfil" in request.form:
    index = int(request.form.get("index"))
    edited_perfil = request.form.get("edited_perfil")

    with open("data/cadastro.json", "r") as f:  
      userss = json.load(f)

    for user in userss:
      if user['index'] == index:
        user['turma'] = session['edited_turma']
        user['time'] = int(session['edited_time'])
        user['perfil'] = int(edited_perfil)

    with open("data/cadastro.json", "w") as file:
        json.dump(userss, file, indent=2)

    return redirect(url_for('controles.controle_integrantes'))        
  
  elif "delete" in request.form:
    index = int(request.form.get("index"))
    confirm_delete = True
    print(index)

  elif "confirm_del" in request.form:
    index = int(request.form.get("index"))
    editing=False
    
    with open("data/cadastro.json", "r") as f:  
      userss = json.load(f)

    for user in userss:
      if user['index'] == index:
        userss.remove(user)  

    with open("data/cadastro.json", "w") as file:
        json.dump(userss, file, indent=2)

    return redirect(url_for('controles.controle_integrantes'))      
  
  return render_template('admin/controle_integrantes.html', dashboard_check=session['dashboard_check'], nomeUsuario=session['nomeUsuario'], edited_turma=edited_turma, edited_time=edited_time, users=users, turmas=turmas, times=times, editing=editing, editing_time=editing_time, times_turma=times_turma, editing_perfil=editing_perfil, confirm_delete=confirm_delete, index=index, darkmode=session['darkmode'])


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

  return render_template('admin/controle_times.html', dashboard_check=session['dashboard_check'], users=users, turmas=turmas, times=times, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])


@bp.route("/controle_projetos")
@login_required
@admin_required
def controle_projetos():
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

  return render_template('admin/controle_projetos.html', dashboard_check=session['dashboard_check'], turmas_select=turmas_select, users=users, turmas=turmas, times=times, projetos=projetos, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], sprint_index=session['sprint'])
