from flask import request, flash, redirect, url_for, render_template, Blueprint as bp
import json
import os
from datetime import datetime, timedelta
import bcrypt
from utils.decorators import login_required, admin_required
from utils.email_sender import send_email, email_connect

import asyncio
import threading

bp = bp('criacoes', __name__)

async def send_email_async(smtp_connection, destinatario, assunto, mensagem):
    await send_email(smtp_connection, destinatario, assunto, mensagem)

def run_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

#connection = email_connect()
#########      ACESSO GERAL          ############

@bp.route("/cadastro_submit", methods=["POST"])
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
    return redirect(url_for('padroes.cadastro'))

  check_turma = False

  with open('data/turmas.json', 'r') as f:
    turmas = json.load(f)
  for turma in turmas:
    if codigo_turma == turma['codigo'] :
      check_turma = True

  if not check_turma:
    flash('Codigo de turma não existente!')
    return redirect(url_for('padroes.cadastro'))
  
  try:
    with open("data/projetos.json", "r") as f:
      projetos = json.load(f)
  except:
    projetos=[]

  avaliacoes=[]

  try:
    for projeto in projetos:
      if projeto['turma'] == codigo_turma:
          avaliacoes=projeto['avaliacoes']
  except:
    pass

  cadastro_dict = {
    "index": len(data),
    "nome": nome.title(),
    "email": email.lower(),
    "turma": codigo_turma,
    "time": 0,
    "senha": hashed_password.decode('utf-8'),
    "perfil": 1,
    "acessos": 0,
    "avaliacoes": avaliacoes,
    "count_avaliacao": 0
  }

  data.append(cadastro_dict)
  with open('data/cadastro.json', 'w') as f:
    json.dump(data, f, indent=2)
  
  loop = asyncio.new_event_loop()
  thread = threading.Thread(target=run_async_loop, args=(loop,))
  thread.start()

  # asyncio.run_coroutine_threadsafe(send_email_async(
  #           smtp_connection=connection,
  #           destinatario = email, 
  #           assunto = f"Boas Vindas - Avaliação 360º", 
  #           mensagem = render_template('utils/new_user_body.html', email=email, nome=nome.title(), turma_user=codigo_turma, senha=senha, turmas=turmas)
  #           ), loop)

  flash('Cadastrado com sucesso!')

  return redirect(url_for('padroes.home'))


#######   ADMINISTRADOR   #############

@bp.route("/criar_turma", methods=["POST"])
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
    return redirect(url_for('controles.controle_turmas'))

  turma_dict = {
    "index": len(data),
    "nome": nome_turma.title(),
    "codigo": codigo_turma
  }

  data.append(turma_dict)
  with open('data/turmas.json', 'w') as f:
    json.dump(data, f, indent=2)

  return redirect(url_for('controles.controle_turmas'))

@bp.route("/criar_time", methods=["POST"])
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
    "turma": codigo_time_turma,
    "codigo": len(data)+1
  }

  data.append(time_dict)
  with open('data/times.json', 'w') as f:
    json.dump(data, f, indent=2)

  return redirect(url_for('controles.controle_times'))


@bp.route("/criar_projeto", methods=["POST"])
@login_required
@admin_required
def criar_projeto():
  if not os.path.exists('data/projetos.json'):
    if not os.path.exists('data'):
      os.makedirs('data')
      with open('data/projetos.json', 'w') as f:
        f.write('[]')
    else:
      with open('data/projetos.json', 'w') as f:
        f.write('[]')

  try:
        with open("data/turmas.json", "r") as f:
            turmas = json.load(f)
  except:
      turmas = []

  new_projeto_turma = request.form.get("new_projeto_turma")
  new_projeto_nome = request.form.get("new_projeto_nome")
  new_projeto_sprints = int(request.form.get("new_projeto_sprints"))
  new_projeto_duracao_sprint = int(request.form.get("new_projeto_duracao_sprint"))
  new_projeto_inicio = datetime.strptime(request.form.get("new_projeto_inicio"), '%Y-%m-%d').date()

  dias = (new_projeto_sprints*new_projeto_duracao_sprint)-1

  new_projeto_fim = new_projeto_inicio + timedelta(days=dias)

  periodos_avaliacao = []
  i=0
  delta = new_projeto_inicio
  
  while i<new_projeto_sprints:
    sprint = i+1
    inicio =  delta + timedelta(days=new_projeto_duracao_sprint)
    fim =  inicio + timedelta(days=4)

    periodos_avaliacao.append([sprint,inicio.strftime('%d-%m-%Y'),fim.strftime('%d-%m-%Y')])

    delta += timedelta(days=new_projeto_duracao_sprint)

    i+=1


  with open('data/projetos.json', 'r') as f:
    projetos = json.load(f)

  projeto_dict = {
    "index": len(projetos),
    "turma": new_projeto_turma,
    "nome": new_projeto_nome,
    "sprints": new_projeto_sprints,
    "duracao": new_projeto_duracao_sprint,
    "inicio": new_projeto_inicio.strftime('%d-%m-%Y'),
    "fim": new_projeto_fim.strftime('%d-%m-%Y'),
    "avaliacoes": periodos_avaliacao
  }

  projetos.append(projeto_dict)

  try:
      with open("data/cadastro.json", "r") as f:
        users = json.load(f)
  except:
    users=[]

  for user in users:
     if user['turma'] == new_projeto_turma:
        user['avaliacoes'] = periodos_avaliacao
        user['count_avaliacao'] = 0

        loop = asyncio.new_event_loop()
        thread = threading.Thread(target=run_async_loop, args=(loop,))
        thread.start()

        # asyncio.run_coroutine_threadsafe(send_email_async(
        #           smtp_connection=connection,
        #           destinatario = user['email'], 
        #           assunto = f"Avaliação 360º - Projeto {new_projeto_nome}", 
        #           mensagem = render_template('utils/new_project_body.html', turmas=turmas, user=user, new_projeto_nome=new_projeto_nome, new_projeto_sprints=new_projeto_sprints, new_projeto_duracao_sprint=new_projeto_duracao_sprint, new_projeto_inicio=new_projeto_inicio, new_projeto_fim=new_projeto_fim, periodos_avaliacao=periodos_avaliacao)
        #           ), loop)
        
  with open('data/cadastro.json', 'w') as u:
    json.dump(users, u, indent=2)
  with open('data/projetos.json', 'w') as f:
    json.dump(projetos, f, indent=2)

  return redirect(url_for('controles.controle_projetos'))
