from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import json
import os
from datetime import datetime, timedelta
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

def team_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if session['time'] == 0:
            return redirect(url_for('menu_integrante'))
        return route_function(*args, **kwargs)
    return decorated_function

@app.route("/darkmode_on")
def darkmode_on():

  session['darkmode'] = True

  if session['perfil'] == 1:
    return redirect(url_for('menu_integrante'))
  else:
    return redirect(url_for('menu_admin'))

@app.route("/darkmode_off")
def darkmode_off():

  session['darkmode'] = False

  if session['perfil'] == 1:
    return redirect(url_for('menu_integrante'))
  else:
    return redirect(url_for('menu_admin'))

@app.route("/")
def home():
  try:  
    for key in list(session.keys()):
      del session[key]
  except:
    pass

  return render_template('login.html')

@app.route("/menu_admin")
@login_required
@admin_required
def menu_admin():
  return render_template('menu_admin.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

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
        session['time'] = user['time']
        user['acessos'] += 1

    with open("data/cadastro.json", "w") as file:
        json.dump(users, file, indent=2)
  
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
    return render_template('menu_integrante.html', nomeUsuario=session['nomeUsuario'], sprint_index=session['sprint'], avaliacao_check=session['avaliacao'], darkmode=session['darkmode'])

@app.route("/cadastro")
def cadastro():
  return render_template('cadastro.html')

@app.route("/autoavaliacao")
@login_required
@team_required
def autoavaliacao():
  return render_template('autoavaliacao.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@app.route("/controle_sprints")
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

  return render_template('controle_sprints.html', turmas_select=turmas_select, users=users, turmas=turmas, times=times, projetos=projetos, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@app.route("/criar_projeto", methods=["POST"])
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

  new_projeto_turma = request.form.get("new_projeto_turma")
  new_projeto_nome = request.form.get("new_projeto_nome")
  new_projeto_sprints = int(request.form.get("new_projeto_sprints"))
  new_projeto_duracao_sprint = int(request.form.get("new_projeto_duracao_sprint"))
  new_projeto_inicio = datetime.strptime(request.form.get("new_projeto_inicio"), '%Y-%m-%d').date()

  dias = (new_projeto_sprints*new_projeto_duracao_sprint)-1

  new_projeto_fim = new_projeto_inicio + timedelta(days=dias)


  with open('data/projetos.json', 'r') as f:
    data = json.load(f)

  projeto_dict = {
    "index": len(data),
    "turma": new_projeto_turma,
    "nome": new_projeto_nome,
    "sprints": new_projeto_sprints,
    "duracao": new_projeto_duracao_sprint,
    "inicio": str(new_projeto_inicio),
    "fim": str(new_projeto_fim)
  }

  data.append(projeto_dict)
  with open('data/projetos.json', 'w') as f:
    json.dump(data, f, indent=2)

  periodos_avaliacao = []
  i=0
  delta = new_projeto_inicio
  
  while i<new_projeto_sprints:
    sprint = i+1
    inicio =  delta + timedelta(days=new_projeto_duracao_sprint)
    fim =  inicio + timedelta(days=2)

    periodos_avaliacao.append([sprint,str(inicio),str(fim)])

    delta += timedelta(days=new_projeto_duracao_sprint)

    i+=1

  try:
      with open("data/cadastro.json", "r") as f:
        users = json.load(f)
  except:
    users=[]

  for user in users:
     if user['turma'] == new_projeto_turma:
        user['avaliacoes'] = periodos_avaliacao

  with open('data/cadastro.json', 'w') as u:
    json.dump(users, u, indent=2)

  return redirect(url_for('controle_sprints'))


@app.route("/update_projetos", methods=["POST"])
@login_required
@admin_required
def update_projetos():

    try:
        with open("data/cadastro.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    try:
        with open("data/turmas.json", "r") as f:
            turmas = json.load(f)
    except:
        turmas = []

    try:
        with open("data/projetos.json", "r") as f:
            projetos = json.load(f)
    except:
        projetos = []
    
    editing=False

    index = int(request.form.get("index"))

    if "edit" in request.form:
        editing=True

    elif "save" in request.form:
        edit_projeto_turma = request.form.get("edit_projeto_turma")
        edit_projeto_nome = request.form.get("edit_projeto_nome")
        edit_projeto_sprints = int(request.form.get("edit_projeto_sprints"))
        edit_projeto_duracao_sprint = int(request.form.get("edit_projeto_duracao_sprint"))
        edit_projeto_inicio = datetime.strptime(request.form.get("edit_projeto_inicio"), '%Y-%m-%d').date()

        dias = (edit_projeto_sprints*edit_projeto_duracao_sprint)-1

        edit_projeto_fim = edit_projeto_inicio + timedelta(days=dias)

        for projeto in projetos:
          if projeto['index'] == index:
            projeto['nome'] = edit_projeto_nome
            projeto['sprints'] = edit_projeto_sprints
            projeto['duracao'] = edit_projeto_duracao_sprint
            projeto['inicio'] = str(edit_projeto_inicio)
            projeto['fim'] = str(edit_projeto_fim)

        with open("data/projetos.json", "w") as file:
            json.dump(projetos, file, indent=2)


        edit_periodos_avaliacao = []
        i=0
        delta = edit_projeto_inicio
        
        while i<edit_projeto_sprints:
          sprint = i+1
          inicio =  delta + timedelta(days=edit_projeto_duracao_sprint)
          fim =  inicio + timedelta(days=2)

          edit_periodos_avaliacao.append([sprint,str(inicio),str(fim)])

          delta += timedelta(days=edit_projeto_duracao_sprint)

          i+=1

        try:
            with open("data/cadastro.json", "r") as f:
              users = json.load(f)
        except:
          users=[]

        for user in users:
          if user['turma'] == edit_projeto_turma:
              user['avaliacoes'] = edit_periodos_avaliacao

        with open('data/cadastro.json', 'w') as u:
          json.dump(users, u, indent=2)

        return redirect(url_for('controle_sprints'))
    
    elif "delete" in request.form:
        editing=False

        for projeto in projetos:
          if projeto['index'] == index:
            for user in users:
               if user['turma'] == projeto['turma']:
                  del user['avaliacoes']
            projetos.remove(projeto)

        with open("data/projetos.json", "w") as file:
            json.dump(projetos, file, indent=2)
        
        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)

        return redirect(url_for('controle_sprints'))

    return render_template('controle_sprints.html', index=index, editing=editing, users=users, turmas=turmas, projetos=projetos, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])


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

  return render_template('controle_turmas.html', users=users, turmas=turmas, times=times, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@app.route("/controle_times", methods=["GET", "POST"])
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
    "turma": codigo_time_turma,
    "codigo": len(data)+1
  }

  data.append(time_dict)
  with open('data/times.json', 'w') as f:
    json.dump(data, f, indent=2)

  return redirect(url_for('controle_times'))


@app.route("/update_turmas", methods=["POST"])
@login_required
@admin_required
def update_turmas():
    page='turmas'

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

    index = int(request.form.get("index"))

    if "edit" in request.form:
        editing=True

    elif "save" in request.form:
        old_codigo = request.form.get("old_codigo")
        new_nome = request.form.get("new_nome")
        new_codigo = request.form.get("new_codigo")

        for turma in turmas:
          if turma['index'] == index:
            turma['nome'] = new_nome
            turma['codigo'] = new_codigo

        for user in users:
          if user['turma'] == old_codigo:
            user['turma'] = new_codigo

        for time in times:
           if time['turma'] == old_codigo:
            time['turma'] = new_codigo

        with open("data/turmas.json", "w") as file:
            json.dump(turmas, file, indent=2)

        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)

        with open("data/times.json", "w") as file:
            json.dump(times, file, indent=2)

        return redirect(url_for('controle_turmas'))
    
    elif "delete" in request.form:
        editing=False

        for turma in turmas:
          if turma['index'] == index:
            turmas.remove(turma)  

        with open("data/turmas.json", "w") as file:
            json.dump(turmas, file, indent=2)
          
        return redirect(url_for('controle_turmas'))

    return render_template('controle_turmas.html', page=page, users=users, turmas=turmas, times=times, editing=editing, index=index, darkmode=session['darkmode'])

@app.route("/update_times", methods=["POST"])
@login_required
@admin_required
def update_times():
    page='times'

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

    index = int(request.form.get("index"))

    if "edit" in request.form:
        editing=True

    elif "save" in request.form:
        edited_nome = request.form.get("edited_nome")
        edited_turma = request.form.get("edited_turma")

        for time in times:
           if time['index'] == index:
            time['nome'] = edited_nome
            time['turma'] = edited_turma

        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)

        with open("data/times.json", "w") as file:
            json.dump(times, file, indent=2)

        return redirect(url_for('controle_times'))
    
    elif "delete" in request.form:
        editing=False

        for time in times:
          if time['index'] == index:
            for user in users:
              if user['time'] == time['codigo']:
                 user['time'] = 0
            times.remove(time)

        with open("data/times.json", "w") as file:
            json.dump(times, file, indent=2)
        
        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)
          
        return redirect(url_for('controle_times'))

    return render_template('controle_times.html', page=page, users=users, turmas=turmas, times=times, editing=editing, index=index, darkmode=session['darkmode'])


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
    editing_time=False
    editing_perfil=False

    index = int(request.form.get("index"))

    if "edit" in request.form:
        editing=True

    elif "save_turma" in request.form:
        editing_time=True

        session['edited_turma'] = request.form.get("edited_turma")            

    elif "save_time" in request.form:
        editing_perfil=True

        session['edited_time'] = request.form.get("edited_time")

    elif "save_perfil" in request.form:        
        edited_perfil = request.form.get("edited_perfil")

        for user in users:
          if user['index'] == index:
            user['turma'] = session['edited_turma']
            user['time'] = int(session['edited_time'])
            user['perfil'] = int(edited_perfil)

        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)

        return redirect(url_for('controle_geral'))        
    
    elif "delete" in request.form:
        editing=False

        for user in users:
          if user['index'] == index:
            users.remove(user)  

        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)

        return redirect(url_for('controle_geral'))        

    return render_template('controle_geral.html', users=users, turmas=turmas, times=times, editing=editing, editing_time=editing_time, editing_perfil=editing_perfil, index=index, darkmode=session['darkmode'])


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

    

  return render_template('controle_geral.html', times=times, turmas=turmas, users=users, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@app.route("/pre_devolutiva")
@login_required
def pre_devolutiva():
  return render_template('pre_devolutiva_avaliacao.html', avaliacao_check=session['avaliacao'], nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

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

  return render_template('devolutiva_avaliacao.html', avaliacao_check=session['avaliacao'], nomeUsuario=session['nomeUsuario'], sprint=sprint, avgs=avgs, avaliacoes=avaliacoes, autoavaliacoes=autoavaliacoes, email=session['email'], darkmode=session['darkmode'])


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

  return render_template('devolutiva_admin.html', nomeUsuario=session['nomeUsuario'], sprint=sprint, int_infos = int_infos, integrante=integrante, avgs=avgs, avaliacoes=avaliacoes, autoavaliacoes=autoavaliacoes, email=session['email'], darkmode=session['darkmode'])

@app.route("/devolutiva_admin")
@login_required
@admin_required
def devolutiva_admin():
  return render_template('devolutiva_admin.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@app.route("/pre_devolutiva_admin")
@login_required
@admin_required
def pre_devolutiva_admin():
  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  return render_template('pre_devolutiva_admin.html', users=users, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@app.route("/dashboards_gerenciais")
@login_required
@admin_required
def dashboards_gerenciais():
  return render_template('dashboards_gerenciais.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@app.route("/dashboards_operacionais")
@login_required
@admin_required
def dashboards_operacionais():
  return render_template('dashboards_operacionais.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@app.route("/avaliacao")
@login_required
@team_required
def avaliacao():
  try:
    with open("data/cadastro.json", "r") as f:
      users = json.load(f)
  except:
    users=[]

  return render_template('avaliacao.html', users=users, nomeUsuario=session['nomeUsuario'], emailUsuario=session['email'], darkmode=session['darkmode'])


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
        session['time'] = item['time']

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
@team_required
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
@team_required
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
  texto_comunicacao = request.form.get('texto_comunicacao')
  engajamento = request.form.get('engajamento')
  texto_engajamento = request.form.get('texto_engajamento')
  entrega = request.form.get('entrega')
  texto_entrega = request.form.get('texto_entrega')
  conhecimento = request.form.get('conhecimento')
  texto_conhecimento = request.form.get('texto_conhecimento')
  autogestao = request.form.get('autogestao')
  texto_autogestao = request.form.get('texto_autogestao')

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
    "texto_comunicacao": texto_comunicacao,
    "engajamento": int(engajamento),
    "texto_engajamento": texto_engajamento,
    "conhecimento": int(conhecimento),
    "texto_conhecimento": texto_conhecimento,
    "entrega": int(entrega),
    "texto_entrega": texto_entrega,
    "autogestao": int(autogestao),
    "texto_autogestao": texto_autogestao
  }

  data.append(avaliacao_dict)
  with open('data/avaliacao.json', 'w') as f:
    json.dump(data, f, indent=2)

  flash('Avaliação Registrada com Sucesso!')

  return redirect(url_for('avaliacao'))



app.secret_key = 'wxyz@mtwjer123123%213'

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
