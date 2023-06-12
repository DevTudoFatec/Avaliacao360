from flask import render_template, request, session, Blueprint as bp
import json
import pandas as pd
from utils.decorators import login_required, admin_required, team_required, integrante_required, data_required

bp = bp('devolutivas', __name__)

#### ADMINISTRADOR ######

@bp.route("/devolutiva_admin", methods=["GET", "POST"])
@login_required
@admin_required
@data_required
def devolutiva_admin():

  with open("data/projetos.json", "r") as f:
    projetos = json.load(f)

  with open("data/turmas.json", "r") as f:
    turmas = json.load(f)

  with open("data/times.json", "r") as f:
    times = json.load(f)

  with open("data/cadastro.json", "r") as f:
    users = json.load(f)

  with open("data/avaliacao.json", "r") as f:
    avaliacoes = json.load(f)

  with open("data/autoavaliacao.json", "r") as g:
    autoavaliacoes = json.load(g)

  turmas = [turma for turma in turmas if turma['codigo'] in [avaliacao['turma_codigo'] for avaliacao in avaliacoes]]  

  select_time = False
  show_table = False          
  
  if "save_turma" in request.form:
    select_time = True
    turma_escolha = request.form.get('turma_escolha')
    nome_turma = [turma['nome'] for turma in turmas if turma['codigo'] == turma_escolha][0]
    times = [time for time in times if time['turma'] == turma_escolha and time['codigo'] in [avaliacao['time'] for avaliacao in avaliacoes]]
    qtia_sprints = len([projeto['avaliacoes'] for projeto in projetos if projeto['turma'] == turma_escolha][0])

    return render_template('admin/devolutiva_admin.html', nome_turma=nome_turma, qtia_sprints=qtia_sprints, 
                           select_time=select_time, show_table=show_table, nomeUsuario=session['nomeUsuario'], 
                           darkmode=session['darkmode'], times=times,turma_escolha=turma_escolha)
  
  elif "filtrar" in request.form:
    turma_escolha = request.form.get("turma_escolha")
    nome_turma = [turma['nome'] for turma in turmas if turma['codigo'] == turma_escolha][0]
    time_escolha = int(request.form.get('time_escolha'))
    nome_time = [time['nome'] for time in times if time['codigo'] == time_escolha][0]
    sprint_escolha = [int(request.form.get("sprint_escolha"))] if int(request.form.get("sprint_escolha")) != 0 else [i for i in range(1,len([projeto['avaliacoes'] for projeto in projetos if projeto['turma'] == turma_escolha][0])+1)]
    sprint_string = ', '.join(str(x) for x in sprint_escolha) if len(sprint_escolha) > 1 else str(sprint_escolha[0])

    notas_medias_turma = {}
    notas_medias_time = {}
    notas_medias_integrante = {}
    feedbacks_integrante = {}

    for item in avaliacoes:
      if item['turma_codigo'] == turma_escolha and item['sprint'] in sprint_escolha:
        integrante = item['integrante']
        comunicacao = item['comunicacao']
        engajamento = item['engajamento']
        conhecimento = item['conhecimento']
        entrega = item['entrega']
        autogestao = item['autogestao']
        texto_comunicacao = item['texto_comunicacao']
        texto_engajamento = item['texto_engajamento']
        texto_conhecimento = item['texto_conhecimento']
        texto_entrega = item['texto_entrega']
        texto_autogestao = item['texto_autogestao']

        notas_medias_turma.setdefault('comunicacao', []).append(comunicacao)
        notas_medias_turma.setdefault('engajamento', []).append(engajamento)
        notas_medias_turma.setdefault('conhecimento', []).append(conhecimento)
        notas_medias_turma.setdefault('entrega', []).append(entrega)
        notas_medias_turma.setdefault('autogestao', []).append(autogestao)

        if item['time'] == time_escolha:
          notas_medias_time.setdefault('comunicacao', []).append(comunicacao)
          notas_medias_time.setdefault('engajamento', []).append(engajamento)
          notas_medias_time.setdefault('conhecimento', []).append(conhecimento)
          notas_medias_time.setdefault('entrega', []).append(entrega)
          notas_medias_time.setdefault('autogestao', []).append(autogestao)

          notas_medias_integrante.setdefault(integrante, {}).setdefault('comunicacao', []).append(comunicacao)
          notas_medias_integrante.setdefault(integrante, {}).setdefault('engajamento', []).append(engajamento)
          notas_medias_integrante.setdefault(integrante, {}).setdefault('conhecimento', []).append(conhecimento)
          notas_medias_integrante.setdefault(integrante, {}).setdefault('entrega', []).append(entrega)
          notas_medias_integrante.setdefault(integrante, {}).setdefault('autogestao', []).append(autogestao)

          feedbacks_integrante.setdefault(integrante, {}).setdefault('comunicacao', []).append(texto_comunicacao) if len(texto_comunicacao) > 0 else None
          feedbacks_integrante.setdefault(integrante, {}).setdefault('engajamento', []).append(texto_engajamento) if len(texto_engajamento) > 0 else None
          feedbacks_integrante.setdefault(integrante, {}).setdefault('conhecimento', []).append(texto_conhecimento) if len(texto_conhecimento) > 0 else None
          feedbacks_integrante.setdefault(integrante, {}).setdefault('entrega', []).append(texto_entrega) if len(texto_entrega) > 0 else None
          feedbacks_integrante.setdefault(integrante, {}).setdefault('autogestao', []).append(texto_autogestao) if len(texto_autogestao) > 0 else None

    df = pd.DataFrame(notas_medias_turma)
    df = df.mean()
    notas_medias_turma = {key: float(f"{value:,.2f}") for key, value in df.to_dict().items()}

    df = pd.DataFrame(notas_medias_time)
    df = df.mean()
    notas_medias_time = {key: float(f"{value:,.2f}") for key, value in df.to_dict().items()}

    for integrante in notas_medias_integrante:
      df = pd.DataFrame(notas_medias_integrante[integrante])
      df = df.mean()
      notas_medias_integrante[integrante] = {key: float(f"{value:,.2f}") for key, value in df.to_dict().items()}
      notas_medias_integrante[integrante]['nome'] = [user['nome'] for user in users if user['email'] == integrante][0]

    for integrante in feedbacks_integrante:
      feedbacks_integrante[integrante]['nome'] = [user['nome'] for user in users if user['email'] == integrante][0]

    auto_notas_medias_time = {}
    auto_notas_medias_turma = {}
    auto_notas_medias_integrante = {}

    for item in autoavaliacoes:
      if item['turma_codigo'] == turma_escolha and item['sprint'] in sprint_escolha:
        integrante = item['email']
        comunicacao = item['comunicacao']
        engajamento = item['engajamento']
        conhecimento = item['conhecimento']
        entrega = item['entrega']
        autogestao = item['autogestao']

        auto_notas_medias_turma.setdefault('auto_comunicacao', []).append(comunicacao)
        auto_notas_medias_turma.setdefault('auto_engajamento', []).append(engajamento)
        auto_notas_medias_turma.setdefault('auto_conhecimento', []).append(conhecimento)
        auto_notas_medias_turma.setdefault('auto_entrega', []).append(entrega)
        auto_notas_medias_turma.setdefault('auto_autogestao', []).append(autogestao)

        if item['time'] == time_escolha:
          auto_notas_medias_time.setdefault('auto_comunicacao', []).append(comunicacao)
          auto_notas_medias_time.setdefault('auto_engajamento', []).append(engajamento)
          auto_notas_medias_time.setdefault('auto_conhecimento', []).append(conhecimento)
          auto_notas_medias_time.setdefault('auto_entrega', []).append(entrega)
          auto_notas_medias_time.setdefault('auto_autogestao', []).append(autogestao)

          auto_notas_medias_integrante.setdefault(integrante, {}).setdefault('comunicacao', []).append(comunicacao)
          auto_notas_medias_integrante.setdefault(integrante, {}).setdefault('engajamento', []).append(engajamento)
          auto_notas_medias_integrante.setdefault(integrante, {}).setdefault('conhecimento', []).append(conhecimento)
          auto_notas_medias_integrante.setdefault(integrante, {}).setdefault('entrega', []).append(entrega)
          auto_notas_medias_integrante.setdefault(integrante, {}).setdefault('autogestao', []).append(autogestao)

      
    df = pd.DataFrame(auto_notas_medias_turma)
    df = df.mean()
    auto_notas_medias_turma = {key: float(f"{value:,.2f}") for key, value in df.to_dict().items()}

    df = pd.DataFrame(auto_notas_medias_time)
    df = df.mean()
    auto_notas_medias_time = {key: float(f"{value:,.2f}") for key, value in df.to_dict().items()}

    for integrante in auto_notas_medias_integrante:
      df = pd.DataFrame(auto_notas_medias_integrante[integrante])
      df = df.mean()
      auto_notas_medias_integrante[integrante] = {key: float(f"{value:,.2f}") for key, value in df.to_dict().items()}
      auto_notas_medias_integrante[integrante]['nome'] = [user['nome'] for user in users if user['email'] == integrante][0]


    show_table = True
        
    return render_template('admin/devolutiva_admin.html', turmas=turmas, select_time=select_time,
                          notas_medias_turma=notas_medias_turma, notas_medias_time=notas_medias_time, sprint_string=sprint_string,
                          notas_medias_integrante=notas_medias_integrante, auto_notas_medias_turma=auto_notas_medias_turma, 
                          auto_notas_medias_time=auto_notas_medias_time, auto_notas_medias_integrante=auto_notas_medias_integrante,
                          nome_turma=nome_turma, nome_time=nome_time, sprint_escolha=sprint_escolha, feedbacks_integrante=feedbacks_integrante,
                         show_table=show_table, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])
  
  
  return render_template('admin/devolutiva_admin.html', turmas=turmas, select_time=select_time, 
                         show_table=show_table, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])
  



##### INTEGRANTE #######

@bp.route("/devolutiva_integrante", methods=["GET", "POST"])
@login_required
@team_required
@integrante_required
@data_required
def devolutiva_integrante():

  with open("data/cadastro.json", "r") as f:
    users = json.load(f)

  with open("data/avaliacao.json", "r") as f:
    avaliacoes = json.load(f)

  with open("data/autoavaliacao.json", "r") as g:
    autoavaliacoes = json.load(g)

  pre_devolutiva = False

  if request.method == 'GET':
    pre_devolutiva = True
    team_sprints = len(session['avaliacoes'])  

    return render_template('integrante/devolutiva_avaliacao.html', pre_devolutiva=pre_devolutiva, team_sprints=team_sprints,
                              nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], avaliacao_check=session['avaliacao'],
                              sprint_index=session['sprint'], count=session['count_avaliacao'])

  elif "confirm_devolutiva" in request.form:

    sprint_escolha = int(request.form.get("sprint_escolha"))

    notas_medias_integrante = {}
    feedbacks_integrante = {}
    auto_notas_medias_integrante = {}

    for item in avaliacoes:
      if item['integrante'] == session['email'] and item['sprint'] == sprint_escolha:
        comunicacao = item['comunicacao']
        engajamento = item['engajamento']
        conhecimento = item['conhecimento']
        entrega = item['entrega']
        autogestao = item['autogestao']
        texto_comunicacao = item['texto_comunicacao']
        texto_engajamento = item['texto_engajamento']
        texto_conhecimento = item['texto_conhecimento']
        texto_entrega = item['texto_entrega']
        texto_autogestao = item['texto_autogestao']

        notas_medias_integrante.setdefault('comunicacao', []).append(comunicacao)
        notas_medias_integrante.setdefault('engajamento', []).append(engajamento)
        notas_medias_integrante.setdefault('conhecimento', []).append(conhecimento)
        notas_medias_integrante.setdefault('entrega', []).append(entrega)
        notas_medias_integrante.setdefault('autogestao', []).append(autogestao)

        feedbacks_integrante.setdefault('comunicacao', []).append(texto_comunicacao) if len(texto_comunicacao) > 0 else None
        feedbacks_integrante.setdefault('engajamento', []).append(texto_engajamento) if len(texto_engajamento) > 0 else None
        feedbacks_integrante.setdefault('conhecimento', []).append(texto_conhecimento) if len(texto_conhecimento) > 0 else None
        feedbacks_integrante.setdefault('entrega', []).append(texto_entrega) if len(texto_entrega) > 0 else None
        feedbacks_integrante.setdefault('autogestao', []).append(texto_autogestao) if len(texto_autogestao) > 0 else None


    df = pd.DataFrame(notas_medias_integrante)
    df = df.mean()
    notas_medias_integrante = {key: float(f"{value:,.2f}") for key, value in df.to_dict().items()}

    for item in autoavaliacoes:
      if item['email'] == session['email'] and item['sprint'] == sprint_escolha:
        comunicacao = item['comunicacao']
        engajamento = item['engajamento']
        conhecimento = item['conhecimento']
        entrega = item['entrega']
        autogestao = item['autogestao']

        auto_notas_medias_integrante.setdefault('comunicacao', []).append(comunicacao)
        auto_notas_medias_integrante.setdefault('engajamento', []).append(engajamento)
        auto_notas_medias_integrante.setdefault('conhecimento', []).append(conhecimento)
        auto_notas_medias_integrante.setdefault('entrega', []).append(entrega)
        auto_notas_medias_integrante.setdefault('autogestao', []).append(autogestao)

    df = pd.DataFrame(auto_notas_medias_integrante)
    df = df.mean()
    auto_notas_medias_integrante = {key: float(f"{value:,.2f}") for key, value in df.to_dict().items()}

    return render_template('integrante/devolutiva_avaliacao.html', pre_devolutiva=pre_devolutiva, 
                           sprint=sprint_escolha, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], 
                           avaliacao_check=session['avaliacao'], sprint_index=session['sprint'], count=session['count_avaliacao'],
                           notas_medias_integrante=notas_medias_integrante, auto_notas_medias_integrante=auto_notas_medias_integrante, feedbacks_integrante=feedbacks_integrante
                          )
