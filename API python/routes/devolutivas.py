from flask import render_template, request, session, Blueprint as bp
import json
import os
from utils.decorators import login_required, admin_required, team_required

bp = bp('devolutivas', __name__)

#### ADMINISTRADOR ######

@bp.route("/devolutiva_admin", methods=["GET", "POST"])
@login_required
@admin_required
def devolutiva_admin():
  return render_template('admin/devolutiva_admin.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])


##### INTEGRANTE #######

@bp.route("/devolutiva_integrante", methods=["GET", "POST"])
@login_required
@team_required
def devolutiva_integrante():

  pre_devolutiva = False

  if request.method == 'GET':
    pre_devolutiva = True
    team_sprints = len(session['avaliacoes'])
  

    return render_template('integrante/devolutiva_avaliacao.html', pre_devolutiva=pre_devolutiva, team_sprints=team_sprints,
                              nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

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

          textos_comunicacao.append(avaliacao['texto_comunicacao'])
          textos_engajamento.append(avaliacao['texto_engajamento'])
          textos_conhecimento.append(avaliacao['texto_conhecimento'])
          textos_entrega.append(avaliacao['texto_entrega'])
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
      avgs = {}

    try:
      with open("data/autoavaliacao.json", "r") as g:
        autoavaliacoes = json.load(g)
    except:
      autoavaliacoes=[]

    user_autoavaliacao = {}

    for autoavaliacao in autoavaliacoes:
      if autoavaliacao['email'] == session['email'] and autoavaliacao['sprint'] == sprint_escolha:
        user_autoavaliacao = autoavaliacao

    return render_template('integrante/devolutiva_avaliacao.html', pre_devolutiva=pre_devolutiva,
                           avgs=avgs, user_autoavaliacao=user_autoavaliacao, textos=textos, sprint=sprint_escolha, 
                           nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])
