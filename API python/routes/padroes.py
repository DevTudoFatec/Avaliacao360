from flask import render_template, request, flash, redirect, url_for, session, Blueprint as bp
import json
import os
from datetime import datetime
import bcrypt
from utils.decorators import login_required, admin_required


bp = bp('padroes', __name__)

######  LIVRE ACESSO  ##########

@bp.route("/")
def home():
  try:  
    for key in list(session.keys()):
      del session[key]
  except:
    pass

  return render_template('login.html')

@bp.route("/cadastro")
def cadastro():
  return render_template('cadastro.html')


@bp.route("/login", methods=['POST'])
def login(): 
  email = request.form.get('email')
  senha = request.form.get('senha')
  check = False
  with open('data/cadastro.json', 'r') as f:
    data = json.load(f)
    for item in data:
      if email == item['email'] and bcrypt.checkpw(senha.encode('utf-8'), item['senha'].encode('utf-8')):
        check = True
        session['nomeUsuario'] = item['nome']
        session['email'] = item['email']
        session['perfil'] = item['perfil']
        session['turma'] = item['turma']
        session['time'] = item['time']
        try:
          session['count_avaliacao'] = item['count_avaliacao']
        except:
           pass

        session['avaliacao'] = False
        session['sprint'] = 'None'

        session['darkmode'] = False

        try:
          avaliacoes = item['avaliacoes']
          
          current_date = datetime.now().date()        
          for avaliacao in avaliacoes:
            inicio = datetime.strptime(avaliacao[1], '%Y-%m-%d').date()
            fim = datetime.strptime(avaliacao[2], '%Y-%m-%d').date()

            if inicio <= current_date <= fim:
              session['avaliacao'] = True
              session['sprint'] = avaliacao[0]
        except:
           pass
           
        if item['perfil'] == 2:
          return redirect(url_for('padroes.menu_admin'))
        else:
          return redirect(url_for('padroes.menu_integrante'))
  if not check:
    flash('Usuário ou Senha inválidos')
    return redirect('/')

###### ADMINISTRADOR  #############

@bp.route("/menu_admin")
@login_required
@admin_required
def menu_admin():
  return render_template('menu_admin.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

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

    

  return render_template('controle_geral.html', times=times, turmas=turmas, users=users, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

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

  return render_template('controle_turmas.html', users=users, turmas=turmas, times=times, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

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

  return render_template('controle_times.html', users=users, turmas=turmas, times=times, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])


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

  return render_template('controle_sprints.html', turmas_select=turmas_select, users=users, turmas=turmas, times=times, projetos=projetos, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], sprint_index=session['sprint'])


###### INTEGRANTE  #############

@bp.route("/menu_integrante", methods=["GET", "POST"])
@login_required
def menu_integrante():

  with open("data/cadastro.json", "r") as f:
    users = json.load(f)

  if "confirm" in request.form:
    user_time = request.form.get("user_time")
    for user in users:
      if user['email'] == session['email']:
        user['time'] = int(user_time)
        session['time'] = user['time']
        user['acessos'] += 1

    with open("data/cadastro.json", "w") as file:
        json.dump(users, file, indent=2)  

    return redirect(url_for('padroes.menu_integrante'))

  elif request.method == 'GET':

    for user in users:
      if user['email'] == session['email']:
        if user['acessos'] == 0 or session['time'] == 0:
          primeiro_acesso = True
        else:
          primeiro_acesso = False

    if primeiro_acesso:
      try:
        with open("data/times.json", "r") as f:
          times = json.load(f)
        
        times_turma = []
        for time in times:
          if time['turma'] == session['turma']:
            times_turma.append(time)
      except:
        times_turma = []     
      return render_template('menu_integrante.html', primeiro_acesso=primeiro_acesso, times=times_turma, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])
    
    else:
      return render_template('menu_integrante.html', nomeUsuario=session['nomeUsuario'], sprint_index=session['sprint'], count=session['count_avaliacao'], avaliacao_check=session['avaliacao'], darkmode=session['darkmode'])

