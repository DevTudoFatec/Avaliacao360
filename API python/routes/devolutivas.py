from flask import render_template, request, session, Blueprint as bp
import json
import os
from utils.decorators import login_required, admin_required, team_required

bp = bp('devolutivas', __name__)

#### ADMINISTRADOR ######

@bp.route("/pre_devolutiva_admin")
@login_required
@admin_required
def pre_devolutiva_admin():
  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  return render_template('admin/pre_devolutiva_admin.html', users=users, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@bp.route("/pre_devolutiva_submit_admin", methods=["POST"])
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

  return render_template('admin/devolutiva_admin.html', nomeUsuario=session['nomeUsuario'], sprint=sprint, int_infos = int_infos, integrante=integrante, avgs=avgs, avaliacoes=avaliacoes, autoavaliacoes=autoavaliacoes, email=session['email'], darkmode=session['darkmode'])

@bp.route("/devolutiva_admin")
@login_required
@admin_required
def devolutiva_admin():
  return render_template('admin/devolutiva_admin.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])


##### INTEGRANTE #######

@bp.route("/pre_devolutiva")
@login_required
@team_required
def pre_devolutiva():

  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  team_sprints=0

  try:
    for user in users:
      if user['email'] == session['email']:
          team_sprints=len(user['avaliacoes'])
  except:
     pass

  return render_template('integrante/pre_devolutiva_avaliacao.html', count=session['count_avaliacao'], sprint_index=session['sprint'], team_sprints=team_sprints, avaliacao_check=session['avaliacao'], nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@bp.route("/pre_devolutiva_submit", methods=["POST"])
@login_required
@team_required
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

  return render_template('integrante/devolutiva_avaliacao.html', count=session['count_avaliacao'], sprint_index=session['sprint'], avaliacao_check=session['avaliacao'], nomeUsuario=session['nomeUsuario'], sprint=sprint, avgs=avgs, avaliacoes=avaliacoes, autoavaliacoes=autoavaliacoes, email=session['email'], darkmode=session['darkmode'])
