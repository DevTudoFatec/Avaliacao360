from flask import render_template, request, session, Blueprint as bp
import json
import os
from utils.decorators import login_required, admin_required, team_required, integrante_required

bp = bp('devolutivas', __name__)

#### ADMINISTRADOR ######

@bp.route("/devolutiva_admin", methods=["GET", "POST"])
@login_required
@admin_required
def devolutiva_admin():
  try:
    with open("data/projetos.json", "r") as f:
      projetos = json.load(f)
  except:
    projetos=[]

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
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  try:
      with open("data/avaliacao.json", "r") as f:
        avaliacoes = json.load(f)
  except:
    avaliacoes=[]

  
  try:
    with open("data/autoavaliacao.json", "r") as g:
      autoavaliacoes = json.load(g)
  except:
    autoavaliacoes=[]

  pre_devolutiva = False
  select_turma = False

  if request.method == 'GET':
    pre_devolutiva = True
    select_turma = True

    turmas_projetos = []

    for turma in turmas:
      for projeto in projetos:
        if projeto['turma'] == turma['codigo']:
          turmas_projetos.append(turma)

    return render_template('admin/devolutiva_admin.html', select_turma=select_turma, pre_devolutiva=pre_devolutiva, 
                           turmas=turmas_projetos, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])
          
  
  elif "confirm_turma" in request.form:
    pre_devolutiva = True

    turma_escolha = request.form.get('turma_escolha')
    times_turma = []

    for time in times:
      if time['turma'] == turma_escolha:
        times_turma.append(time)

    turma_tela = ''

    for turma in turmas:
      if turma['codigo'] == turma_escolha:
        turma_tela = turma['nome']

    turma_sprints = ''
    
    for projeto in projetos:
      if projeto["turma"] == turma_escolha:
        turma_sprints = len(projeto['avaliacoes'])
    
      
    return render_template('admin/devolutiva_admin.html', turma_sprints=turma_sprints, turma_tela=turma_tela, times=times_turma, select_turma=select_turma, 
                           pre_devolutiva=pre_devolutiva,  nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])
  
  elif "confirm_devolutiva" in request.form:
    time_escolha = int(request.form.get('time_escolha'))
    sprint_escolha = int(request.form.get("sprint_escolha"))
    users_time = []

    time_nome = next(time['nome'] for time in times if time['codigo'] == time_escolha)

    for user in users:
      if user['time'] == time_escolha:
        users_time.append(user)

    users_data = {}

    for user in users_time:
      users_data[user['email']] = {}
      rows=0
      comunicacao = engajamento = conhecimento = entrega = autogestao = 0

      textos_comunicacao = []
      textos_engajamento = []
      textos_conhecimento = []
      textos_entrega = []
      textos_autogestao = []
      textos = {}
      avgs = {
        "comunicacao": 0, 
        "engajamento": 0, 
        "conhecimento": 0, 
        "entrega": 0, 
        "autogestao": 0
      }

      for avaliacao in avaliacoes:
        if avaliacao['integrante'] == user['email'] and avaliacao['sprint'] == sprint_escolha:
          rows+=1
          comunicacao += avaliacao['comunicacao']
          engajamento += avaliacao['engajamento']
          conhecimento += avaliacao['conhecimento']
          entrega += avaliacao['entrega']
          autogestao += avaliacao['autogestao']

          if len(avaliacao['texto_comunicacao']) > 0:
            textos_comunicacao.append(avaliacao['texto_comunicacao'])
          if len(avaliacao['texto_engajamento']) > 0:
            textos_engajamento.append(avaliacao['texto_engajamento'])
          if len(avaliacao['texto_conhecimento']) > 0:
            textos_conhecimento.append(avaliacao['texto_conhecimento'])
          if len(avaliacao['texto_entrega']) > 0:
            textos_entrega.append(avaliacao['texto_entrega'])
          if len(avaliacao['texto_autogestao']) > 0:
            textos_autogestao.append(avaliacao['texto_autogestao'])

      textos["comunicacao"] = textos_comunicacao
      textos["engajamento"] = textos_engajamento
      textos["conhecimento"] = textos_conhecimento
      textos["entrega"] = textos_entrega
      textos["autogestao"] = textos_autogestao

      comunicacao = comunicacao/rows
      engajamento = engajamento/rows
      conhecimento = conhecimento/rows
      entrega = entrega/rows
      autogestao = autogestao/rows

      avgs["comunicacao"] = int(comunicacao)
      avgs["engajamento"] = int(engajamento)
      avgs["conhecimento"] = int(conhecimento) 
      avgs["entrega"] = int(entrega)
      avgs["autogestao"] = int(autogestao)

      auto_notas = {
        "comunicacao": 0, 
        "engajamento": 0, 
        "conhecimento": 0, 
        "entrega": 0, 
        "autogestao": 0
      }

      for autoavaliacao in autoavaliacoes:
        if autoavaliacao['email'] == user['email'] and autoavaliacao['sprint'] == sprint_escolha:
          auto_notas["comunicacao"] = int(autoavaliacao["comunicacao"])
          auto_notas["engajamento"] = int(autoavaliacao["engajamento"])
          auto_notas["conhecimento"] = int(autoavaliacao["conhecimento"]) 
          auto_notas["entrega"] = int(autoavaliacao["entrega"])
          auto_notas["autogestao"] = int(autoavaliacao["autogestao"])
      
      desvio_comunicacao = desvio_engajamento = desvio_conhecimento = desvio_entrega = desvio_autogestao = 0

      desvio_comunicacao += (auto_notas["comunicacao"]-avgs["comunicacao"])
      desvio_engajamento += (auto_notas["engajamento"]-avgs["engajamento"])
      desvio_conhecimento += (auto_notas["conhecimento"]-avgs["conhecimento"])
      desvio_entrega += (auto_notas["entrega"]-avgs["entrega"]) 
      desvio_autogestao += (auto_notas["autogestao"]-avgs["autogestao"])

      desvio_medio = (desvio_comunicacao + desvio_engajamento + desvio_conhecimento + desvio_entrega + desvio_autogestao)/5

      users_data[user['email']]['avgs'] = avgs
      users_data[user['email']]['textos'] = textos
      users_data[user['email']]['autoavaliacao'] = auto_notas
      users_data[user['email']]['desvio_medio'] = desvio_medio


      
    return render_template('admin/devolutiva_admin.html', time_nome=time_nome, time_escolha=time_escolha, sprint=sprint_escolha, 
                           users_data=users_data, users=users_time, pre_devolutiva=pre_devolutiva, desvio_medio=desvio_medio,
                           nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])
  



##### INTEGRANTE #######

@bp.route("/devolutiva_integrante", methods=["GET", "POST"])
@login_required
@team_required
@integrante_required
def devolutiva_integrante():

  pre_devolutiva = False

  if request.method == 'GET':
    pre_devolutiva = True
    team_sprints = len(session['avaliacoes'])
  

    return render_template('integrante/devolutiva_avaliacao.html', pre_devolutiva=pre_devolutiva, team_sprints=team_sprints,
                              nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], avaliacao_check=session['avaliacao'],
                              sprint_index=session['sprint'], count=session['count_avaliacao'])

  elif "confirm_devolutiva" in request.form:

    sprint_escolha = int(request.form.get("sprint_escolha"))

    try:
      with open("data/avaliacao.json", "r") as f:
        avaliacoes = json.load(f)
    except:
      avaliacoes=[]

    try:      
      rows=0
      comunicacao = engajamento = conhecimento = entrega = autogestao = 0
      
      textos_comunicacao = []
      textos_engajamento = []
      textos_conhecimento = []
      textos_entrega = []
      textos_autogestao = []

      for avaliacao in avaliacoes:
        if avaliacao['integrante'] == session['email'] and avaliacao['sprint'] == sprint_escolha:
          rows+=1
          comunicacao += avaliacao['comunicacao']
          engajamento += avaliacao['engajamento']
          conhecimento += avaliacao['conhecimento']
          entrega += avaliacao['entrega']
          autogestao += avaliacao['autogestao']

          if len(avaliacao['texto_comunicacao']) > 0:
            textos_comunicacao.append(avaliacao['texto_comunicacao'])
          if len(avaliacao['texto_engajamento']) > 0:
            textos_engajamento.append(avaliacao['texto_engajamento'])
          if len(avaliacao['texto_conhecimento']) > 0:
            textos_conhecimento.append(avaliacao['texto_conhecimento'])
          if len(avaliacao['texto_entrega']) > 0:
            textos_entrega.append(avaliacao['texto_entrega'])
          if len(avaliacao['texto_autogestao']) > 0:
            textos_autogestao.append(avaliacao['texto_autogestao'])

      textos = {
        "comunicacao": textos_comunicacao,
        "engajamento": textos_engajamento,
        "conhecimento": textos_conhecimento,
        "entrega": textos_entrega,
        "autogestao": textos_autogestao
      }

      comunicacao = comunicacao/rows
      engajamento = engajamento/rows
      conhecimento = conhecimento/rows
      entrega = entrega/rows
      autogestao = autogestao/rows

      avgs = {
        "comunicacao": int(comunicacao), 
        "engajamento": int(engajamento), 
        "conhecimento": int(conhecimento), 
        "entrega": int(entrega), 
        "autogestao": int(autogestao)
      }
    except:
      avgs = {
        "comunicacao": 0, 
        "engajamento": 0, 
        "conhecimento": 0, 
        "entrega": 0, 
        "autogestao": 0
      }
      textos = {}

    try:
      with open("data/autoavaliacao.json", "r") as g:
        autoavaliacoes = json.load(g)
    except:
      autoavaliacoes=[]

    user_autoavaliacao = {}
    for autoavaliacao in autoavaliacoes:
      if autoavaliacao['email'] == session['email'] and autoavaliacao['sprint'] == sprint_escolha:
        user_autoavaliacao = autoavaliacao
      
    if len(user_autoavaliacao) == 0:
      user_autoavaliacao = {
        "comunicacao": 0, 
        "engajamento": 0, 
        "conhecimento": 0, 
        "entrega": 0, 
        "autogestao": 0
      }

    return render_template('integrante/devolutiva_avaliacao.html', pre_devolutiva=pre_devolutiva, 
                           avgs=avgs, user_autoavaliacao=user_autoavaliacao, textos=textos, sprint=sprint_escolha,
                           nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], avaliacao_check=session['avaliacao'], 
                           sprint_index=session['sprint'], count=session['count_avaliacao'])
