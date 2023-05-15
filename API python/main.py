from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import json
import os
import time
import string
import random

app = Flask(__name__)

##  DEFININDO ROTA

@app.route("/")
def home():
  return render_template('login.html')

@app.route("/menu_admin")
def menu_admin():
  return render_template('menu_admin.html', nomeUsuario=session['nomeUsuario'])

@app.route("/menu_integrante")
def menu_integrante():
  return render_template('menu_integrante.html', nomeUsuario=session['nomeUsuario'])

@app.route("/cadastro")
def cadastro():
  return render_template('cadastro.html', nomeUsuario=session['nomeUsuario'])

@app.route("/autoavaliacao")
def autoavaliacao():
  return render_template('autoavaliacao.html', nomeUsuario=session['nomeUsuario'])

@app.route("/controle_perfil")
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
def update_geral():
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

        edited_semestre = request.form.get("edited_semestre")
        edited_turma = request.form.get("edited_turma")
        edited_time = request.form.get("edited_time")

        for user in users:
          if user['index'] == index:
            user['semestre'] = int(edited_semestre)
            user['turma'] = edited_turma
            user['time'] = edited_time

        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)
    
    elif "delete" in request.form:
        editing=False

        for user in users:
          if user['index'] == index:
            users.remove(user)  

        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)

    return render_template('controle_geral.html', users=users, editing=editing, index=index)

@app.route("/controle_geral")
def controle_geral():
  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  return render_template('controle_geral.html', users=users, nomeUsuario=session['nomeUsuario'])

@app.route("/pre_devolutiva")
def pre_devolutiva():
  return render_template('pre_devolutiva_avaliacao.html', nomeUsuario=session['nomeUsuario'])

@app.route("/pre_devolutiva_submit", methods=["POST"])
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
          int_infos = user['semestre'] + 'º Semestre   -   ' + user['turma'] + '   -    ' + user['nome']                   
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
def devolutiva_admin():
  return render_template('devolutiva_admin.html', nomeUsuario=session['nomeUsuario'])

@app.route("/pre_devolutiva_admin")
def pre_devolutiva_admin():
  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  return render_template('pre_devolutiva_admin.html', users=users, nomeUsuario=session['nomeUsuario'])

@app.route("/dashboards_gerenciais")
def dashboards_gerenciais():
  return render_template('dashboards_gerenciais.html', nomeUsuario=session['nomeUsuario'])

@app.route("/dashboards_operacionais")
def dashboards_operacionais():
  return render_template('dashboards_operacionais.html', nomeUsuario=session['nomeUsuario'])

@app.route("/avaliacao")
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
      if email == item['email'] and senha == item['senha']:
        check = True
        session['nomeUsuario'] = item['nome']
        session['email'] = item['email']
        if item['perfil'] == 2:
          return redirect(url_for('menu_admin'))
        else:
          return redirect(url_for('menu_integrante'))
  if not check:
    flash('Usuário ou Senha inválidos')
    return redirect('/')
    

## função para geração de senha aleatoria do usuario

def senha_aleatoria(tamanho, caracteres):
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

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
  turma = request.form.get('turma')
  semestre = request.form.get('semestre')
  senha = senha_aleatoria(10, string.ascii_lowercase + string.ascii_uppercase + string.digits)

  with open('data/cadastro.json', 'r') as f:
    data = json.load(f)
  if any(user.get("email") == email for user in data):
    flash('Email já cadastrado!')
    return redirect(url_for('cadastro'))

  cadastro_dict = {
    "index": len(data),
    "nome": nome.title(),
    "email": email.lower(),
    "turma": turma,
    "semestre": semestre,
    "time": '',
    "senha": senha,
    "perfil": 1
  }

  data.append(cadastro_dict)
  with open('data/cadastro.json', 'w') as f:
    json.dump(data, f, indent=2)

  flash('Cadastrado com sucesso!')

  return redirect(url_for('cadastro'))


@app.route("/autoavaliacao_submit", methods=["POST"])
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
