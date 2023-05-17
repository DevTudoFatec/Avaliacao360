from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import json
import os
import time
import string
import random
import bcrypt
from functools import wraps

app = Flask(__name__)

##  DEFININDO ROTA

def login_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('home'))
        return route_function(*args, **kwargs)
    return decorated_function

def admin_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if session['perfil'] != 2:
            return redirect(url_for('menu_integrante'))
        return route_function(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
  try:  
    del session['email']
  except:
    pass

  return render_template('login.html')

@app.route("/menu_admin")
@login_required
@admin_required
def menu_admin():
  return render_template('menu_admin.html', nomeUsuario=session['nomeUsuario'])

@app.route("/menu_integrante", methods=["GET", "POST"])
@login_required
def menu_integrante():

  with open("data/cadastro.json", "r") as f:
    users = json.load(f)

  if "confirm" in request.form:
    user_time = request.form.get("user_time")
    for user in users:
      if user['email'] == session['email']:
        user['time'] = int(user_time)
        user['acessos'] += 1

    with open("data/cadastro.json", "w") as file:
        json.dump(users, file, indent=2)
  
  for user in users:
    if user['email'] == session['email']:
      if user['acessos'] == 1:
        primeiro_acesso = True
      else:
        primeiro_acesso = False 

  if primeiro_acesso:
    try:
      with open("data/times.json", "r") as f:
        times = json.load(f)
      
      times_turma = []
      for time in times:
        if time['codigo_turma'] == session['turma']:
          times_turma.append(time)
    except:
      times_turma = []     
    return render_template('menu_integrante.html', primeiro_acesso=primeiro_acesso, times=times_turma, nomeUsuario=session['nomeUsuario'])
      
  else:
    return render_template('menu_integrante.html', nomeUsuario=session['nomeUsuario'])

@app.route("/cadastro")
def cadastro():
  return render_template('cadastro.html')

@app.route("/autoavaliacao")
@login_required
def autoavaliacao():
  return render_template('autoavaliacao.html', nomeUsuario=session['nomeUsuario'])

@app.route("/controle_turmas", methods=["GET", "POST"])
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

  page=''

  if "turmas" in request.form:
    page='turmas'
  elif "times" in request.form:
    page='times'

  return render_template('controle_turmas.html', users=users, turmas=turmas, times=times, page=page, nomeUsuario=session['nomeUsuario'])

@app.route("/criar_turma", methods=["POST"])
@login_required
@admin_required
def criar_turma():
  if not os.path.exists('data/turmas.json'):
    if not os.path.exists('data'):
      os.makedirs('data')
      with open('data/turmas.json', 'w') as f:
        f.write('[]')
    else:
      with open('data/turmas.json', 'w') as f:
        f.write('[]')

  nome_turma = request.form.get("nome_turma")
  codigo_turma = request.form.get("codigo_turma")

  with open('data/turmas.json', 'r') as f:
    data = json.load(f)
  if any(turma.get("codigo_turma") == codigo_turma for turma in data):
    flash('Turma já cadastrada')
    return redirect(url_for('controle_turmas'))

  turma_dict = {
    "index": len(data),
    "nome": nome_turma.title(),
    "codigo": codigo_turma
  }

  data.append(turma_dict)
  with open('data/turmas.json', 'w') as f:
    json.dump(data, f, indent=2)

  return redirect(url_for('controle_turmas'))


@app.route("/criar_time", methods=["POST"])
@login_required
@admin_required
def criar_time():
  if not os.path.exists('data/times.json'):
    if not os.path.exists('data'):
      os.makedirs('data')
      with open('data/times.json', 'w') as f:
        f.write('[]')
    else:
      with open('data/times.json', 'w') as f:
        f.write('[]')

  nome_time = request.form.get("nome_time")
  codigo_time_turma = request.form.get("codigo_time_turma")

  with open('data/times.json', 'r') as f:
    data = json.load(f)

  time_dict = {
    "index": len(data),
    "nome": nome_time.title(),
    "codigo_turma": codigo_time_turma,
    "codigo": len(data)+1
  }

  data.append(time_dict)
  with open('data/times.json', 'w') as f:
    json.dump(data, f, indent=2)

  return redirect(url_for('controle_turmas'))


@app.route("/controle_perfil")
@login_required
@admin_required
def controle_perfil():
  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  return render_template('controle_perfil.html', users=users, nomeUsuario=session['nomeUsuario'])

import json
from flask import request, render_template

@app.route("/update_perfil", methods=["POST"])
@login_required
@admin_required
def update_perfil():
    try:
        with open("data/cadastro.json", "r") as f:
            users = json.load(f)
    except:
        users = []
    
    editing=False
    index=int(request.form.get("index"))

    if "edit" in request.form:
        editing=True

    elif "save" in request.form:
        editing=False

        edited_perfil = request.form.get("edited_perfil")

        for user in users:
          if user['index'] == index:
            user['perfil'] = int(edited_perfil)

        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)

    return render_template('controle_perfil.html', users=users, editing=editing, index=index)

@app.route("/update_geral", methods=["POST"])
@login_required
@admin_required
def update_geral():
    try:
        with open("data/cadastro.json", "r") as f:
            users = json.load(f)
    except:
        users = []

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
    index=int(request.form.get("index"))

    if "edit" in request.form:
        editing=True

    elif "save" in request.form:
        editing=False

        edited_turma = request.form.get("edited_turma")
        edited_time = request.form.get("edited_time")        
        edited_perfil = request.form.get("edited_perfil")

        for user in users:
          if user['index'] == index:
            user['turma'] = edited_turma
            user['time'] = int(edited_time)
            user['perfil'] = int(edited_perfil)

        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)
    
    elif "delete" in request.form:
        editing=False

        for user in users:
          if user['index'] == index:
            users.remove(user)  

        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)

    return render_template('controle_geral.html', users=users, turmas=turmas, times=times, editing=editing, index=index)

@app.route("/controle_geral")
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

    

  return render_template('controle_geral.html', times=times, turmas=turmas, users=users, nomeUsuario=session['nomeUsuario'])

@app.route("/pre_devolutiva")
@login_required
def pre_devolutiva():
  return render_template('pre_devolutiva_avaliacao.html', nomeUsuario=session['nomeUsuario'])

@app.route("/pre_devolutiva_submit", methods=["POST"])
@login_required
def pre_devolutiva_submit():
  sprint = request.form.get('sprint')

  try:
    with open("data/avaliacao.json", "r") as f:
      avaliacoes = json.load(f)
  except:
    avaliacoes=[]

  try:      
    rows=0
    comunicacao = engajamento = conhecimento = entrega = autogestao = 0

    for avaliacao in avaliacoes:
      if avaliacao['integrante'] == session['email'] and avaliacao['sprint'] == sprint:
        rows+=1
        comunicacao += avaliacao['comunicacao']
        engajamento += avaliacao['engajamento']
        conhecimento += avaliacao['conhecimento']
        entrega += avaliacao['entrega']
        autogestao += avaliacao['autogestao']

    comunicacao = comunicacao/rows
    engajamento = engajamento/rows
    conhecimento = conhecimento/rows
    entrega = entrega/rows
    autogestao = autogestao/rows

    avgs = [int(comunicacao), int(engajamento), int(conhecimento), int(entrega), int(autogestao)] 
  except:
    avgs = []

  try:
    with open("data/autoavaliacao.json", "r") as g:
      autoavaliacoes = json.load(g)
  except:
    autoavaliacoes=[]

  return render_template('devolutiva_avaliacao.html', nomeUsuario=session['nomeUsuario'], sprint=sprint, avgs=avgs, avaliacoes=avaliacoes, autoavaliacoes=autoavaliacoes, email=session['email'])


@app.route("/pre_devolutiva_submit_admin", methods=["POST"])
@login_required
@admin_required
def pre_devolutiva_submit_admin():
  sprint = request.form.get('sprint')
  integrante = request.form.get('integrante')

  try:
    with open("data/avaliacao.json", "r") as f:
      avaliacoes = json.load(f)
  except:
    avaliacoes=[]

  int_infos=''

  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
      for user in users:
        if user['email'] == integrante:
          int_infos = user['turma'] + '   -    ' + user['time'] + '   -    ' + user['nome']                   
  except:
    users=[]

  try:      
    rows=0
    comunicacao = engajamento = conhecimento = entrega = autogestao = 0

    for avaliacao in avaliacoes:
      if avaliacao['integrante'] == integrante and avaliacao['sprint'] == sprint:
        rows+=1
        comunicacao += avaliacao['comunicacao']
        engajamento += avaliacao['engajamento']
        conhecimento += avaliacao['conhecimento']
        entrega += avaliacao['entrega']
        autogestao += avaliacao['autogestao']

    comunicacao = comunicacao/rows
    engajamento = engajamento/rows
    conhecimento = conhecimento/rows
    entrega = entrega/rows
    autogestao = autogestao/rows

    avgs = [int(comunicacao), int(engajamento), int(conhecimento), int(entrega), int(autogestao)] 
  except:
    avgs = []

  try:
    with open("data/autoavaliacao.json", "r") as g:
      autoavaliacoes = json.load(g)
  except:
    autoavaliacoes=[]

  return render_template('devolutiva_admin.html', nomeUsuario=session['nomeUsuario'], sprint=sprint, int_infos = int_infos, integrante=integrante, avgs=avgs, avaliacoes=avaliacoes, autoavaliacoes=autoavaliacoes, email=session['email'])

@app.route("/devolutiva_admin")
@login_required
@admin_required
def devolutiva_admin():
  return render_template('devolutiva_admin.html', nomeUsuario=session['nomeUsuario'])

@app.route("/pre_devolutiva_admin")
@login_required
@admin_required
def pre_devolutiva_admin():
  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  return render_template('pre_devolutiva_admin.html', users=users, nomeUsuario=session['nomeUsuario'])

@app.route("/dashboards_gerenciais")
@login_required
@admin_required
def dashboards_gerenciais():
  return render_template('dashboards_gerenciais.html', nomeUsuario=session['nomeUsuario'])

@app.route("/dashboards_operacionais")
@login_required
@admin_required
def dashboards_operacionais():
  return render_template('dashboards_operacionais.html', nomeUsuario=session['nomeUsuario'])

@app.route("/avaliacao")
@login_required
def avaliacao():
  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  return render_template('avaliacao.html', users=users, nomeUsuario=session['nomeUsuario'], emailUsuario=session['email'])


## Validação login

@app.route("/login", methods=['POST'])
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
        item['acessos'] += 1
        with open("data/cadastro.json", "w") as file:
            json.dump(data, file, indent=2)
        if item['perfil'] == 2:
          return redirect(url_for('menu_admin'))
        else:
          return redirect(url_for('menu_integrante'))
  if not check:
    flash('Usuário ou Senha inválidos')
    return redirect('/')


### ARMAZENA DADOS DE CADASTRO EM UM JSON

@app.route("/cadastro_submit", methods=["POST"])
def cadastro_submit():

  if not os.path.exists('data/cadastro.json'):
    if not os.path.exists('data'):
      os.makedirs('data')
      with open('data/cadastro.json', 'w') as f:
        f.write('[]')
    else:
      with open('data/cadastro.json', 'w') as f:
        f.write('[]')

  nome = request.form.get('nome')
  email = request.form.get('email')
  codigo_turma = request.form.get('turma')
  senha = request.form.get('senha')

  hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

  with open('data/cadastro.json', 'r') as f:
    data = json.load(f)
  if any(user.get("email") == email for user in data):
    flash('Email já cadastrado!')
    return redirect(url_for('cadastro'))

  check_turma = False

  with open('data/turmas.json', 'r') as f:
    turmas = json.load(f)
  for turma in turmas:
    if codigo_turma == turma['codigo'] :
      check_turma = True

  if not check_turma:
    flash('Codigo de turma não existente!')
    return redirect(url_for('cadastro'))

  cadastro_dict = {
    "index": len(data),
    "nome": nome.title(),
    "email": email.lower(),
    "turma": codigo_turma,
    "time": 0,
    "senha": hashed_password.decode('utf-8'),
    "perfil": 1,
    "acessos": 0
  }

  data.append(cadastro_dict)
  with open('data/cadastro.json', 'w') as f:
    json.dump(data, f, indent=2)

  flash('Cadastrado com sucesso!')

  return redirect(url_for('home'))


@app.route("/autoavaliacao_submit", methods=["POST"])
@login_required
def autoavaliacao_submit():

  if not os.path.exists('data/autoavaliacao.json'):
    if not os.path.exists('data'):
      os.makedirs('data')
      with open('data/autoavaliacao.json', 'w') as f:
        f.write('[]')
    else:
      with open('data/autoavaliacao.json', 'w') as f:
        f.write('[]')

  email = session['email']
  sprint = request.form.get('sprint')
  comunicacao = request.form.get('comunicacao')
  engajamento = request.form.get('engajamento')
  conhecimento = request.form.get('conhecimento')
  entrega = request.form.get('entrega')
  autogestao = request.form.get('autogestao')

  with open('data/autoavaliacao.json', 'r') as f:
    data = json.load(f)
  if any(user.get("email") == email and user.get("sprint") == sprint for user in data):
    flash(f'Auto Avaliação da Sprint {sprint} já foi realizada!')
    return redirect(url_for('autoavaliacao'))
  
  avaliacao_dict = {
    "email": email,
    "sprint": sprint,
    "comunicacao": int(comunicacao),
    "engajamento": int(engajamento),
    "conhecimento": int(conhecimento),
    "entrega": int(entrega),
    "autogestao": int(autogestao)
  }

  data.append(avaliacao_dict)
  with open('data/autoavaliacao.json', 'w') as f:
    json.dump(data, f, indent=2)

  flash('Autoavaliação Registrada com Sucesso!')

  return redirect(url_for('autoavaliacao'))

@app.route("/avaliacao_submit", methods=["POST"])
@login_required
def avaliacao_submit():

  if not os.path.exists('data/avaliacao.json'):
    if not os.path.exists('data'):
      os.makedirs('data')
      with open('data/avaliacao.json', 'w') as f:
        f.write('[]')
    else:
      with open('data/avaliacao.json', 'w') as f:
        f.write('[]')
  
  avaliador = session['email']
  integrante = request.form.get('integrante')
  sprint = request.form.get('sprint')
  comunicacao = request.form.get('comunicacao')
  engajamento = request.form.get('engajamento')
  entrega = request.form.get('entrega')
  conhecimento = request.form.get('conhecimento')
  autogestao = request.form.get('autogestao')
  texto = request.form.get('texto')

  with open('data/avaliacao.json', 'r') as f:
    data = json.load(f)
  if any(user.get("avaliador") == avaliador and user.get("integrante") == integrante and user.get("sprint") == sprint for user in data):
    flash(f'Avaliação do integrante selecionado na Sprint {sprint} já foi realizada!')
    return redirect(url_for('avaliacao'))

  avaliacao_dict = {
    "avaliador": avaliador,
    "integrante": integrante,
    "sprint": sprint,
    "comunicacao": int(comunicacao),
    "engajamento": int(engajamento),
    "conhecimento": int(conhecimento),
    "entrega": int(entrega),
    "autogestao": int(autogestao),
    "texto": texto
  }

  data.append(avaliacao_dict)
  with open('data/avaliacao.json', 'w') as f:
    json.dump(data, f, indent=2)

  flash('Avaliação Registrada com Sucesso!')

  return redirect(url_for('avaliacao'))



app.secret_key = 'wxyz@mtwjer123123%213'

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
