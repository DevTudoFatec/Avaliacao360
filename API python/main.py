from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import json
import os
import time
import string
import random

app = Flask(__name__)

##  DEFININDO ROTAS


@app.route("/")
def home():
  return render_template('home.html')


@app.route("/cadastro")
def cadastro():
  return render_template('cadastro.html')


@app.route("/autoavaliacao")
def autoavaliacao():
  return render_template('autoavaliacao.html')


@app.route("/avaliacao")
def avaliacao():
  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  return render_template('avaliacao.html', users=users)


@app.route("/login")
def login():
  return render_template('login.html')


@app.route("/menu_admin")
def menu():
  return render_template('menu_admin.html')

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
    "nome": nome.title(),
    "email": email.lower(),
    "turma": turma,
    "semestre": semestre,
    "senha": senha
  }

  data.append(cadastro_dict)
  with open('data/cadastro.json', 'w') as f:
    json.dump(data, f)

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

  sprint = request.form.get('sprint')
  comunicacao = request.form.get('comunicacao')
  engajamento = request.form.get('engajamento')
  conhecimento = request.form.get('conhecimento')
  entrega = request.form.get('entrega')
  autogestao = request.form.get('autogestao')

  with open('data/autoavaliacao.json', 'r') as f:
    data = json.load(f)

  avaliacao_dict = {
    "sprint": sprint,
    "comunicacao": comunicacao,
    "engajamento": engajamento,
    "conhecimento": conhecimento,
    "entrega": entrega,
    "autogestao": autogestao
  }

  data.append(avaliacao_dict)
  with open('data/autoavaliacao.json', 'w') as f:
    json.dump(data, f)

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

  avaliacao_dict = {
    "integrante": integrante,
    "sprint": sprint,
    "comunicacao": comunicacao,
    "engajamento": engajamento,
    "entrega": entrega,
    "conhecimento": conhecimento,
    "autogestao": autogestao,
    "texto": texto
  }

  data.append(avaliacao_dict)
  with open('data/avaliacao.json', 'w') as f:
    json.dump(data, f)

  flash('Avaliação Registrada com Sucesso!')

  return redirect(url_for('avaliacao'))



app.secret_key = 'wxyz@mtwjer123123%213'

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
