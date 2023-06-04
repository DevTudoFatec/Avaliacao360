from flask import render_template, request, redirect, url_for, session, Blueprint as bp
import json
from utils.decorators import login_required, team_required, sprint_required, integrante_required


bp = bp('avaliacao', __name__)

@bp.route("/avaliacao", methods=['GET', 'POST'])
@login_required
@team_required
@sprint_required
@integrante_required
def avaliacao():
    try:
      with open("data/times.json", "r") as f:
        times = json.load(f)
        for time in times:
          if time['codigo'] == session['time']:
            user_time = time['nome']
    except:
      user_time = ''

    try:
        with open("data/cadastro.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    try:
        with open("data/turmas.json", "r") as f:
            turmas = json.load(f)
            turmas_dict = {turma['codigo']: turma['nome'] for turma in turmas}
    except:
        turmas = []

    try:
        with open("data/times.json", "r") as f:
            times = json.load(f)
            times_dict = {time['codigo']: time['nome'] for time in times}
    except:
        times = []

    filtered_users = []
    for user in users:
        if user['time'] == session['time'] and user['email'] != session['email']:
            filtered_users.append(user)


    if request.method == 'GET':

      return render_template('integrante/avaliacao.html', time=user_time, users=filtered_users, avaliacao_check=session['avaliacao'],nomeUsuario=session['nomeUsuario'],emailUsuario=session['email'], darkmode=session['darkmode'],sprint_index=session['sprint'])

    elif request.method == 'POST':

      email = session['email']
      sprint = session['sprint']
      turma_codigo = session['turma']
      nome_turma = turmas_dict.get(turma_codigo, '')
      time = session['time']
      nome_time = times_dict.get(time, '')
      comunicacao = request.form.get('auto_comunicacao')
      engajamento = request.form.get('auto_engajamento')
      conhecimento = request.form.get('auto_conhecimento')
      entrega = request.form.get('auto_entrega')
      autogestao = request.form.get('auto_autogestao')
      
      autovaliacao_dict = {
        "email": email,
        "sprint": sprint,
        "turma_codigo": turma_codigo,
        "turma_nome": nome_turma,
        "time": time,
        "time_nome": nome_time,
        "comunicacao": int(comunicacao),
        "engajamento": int(engajamento),
        "conhecimento": int(conhecimento),
        "entrega": int(entrega),
        "autogestao": int(autogestao)
      }

      try:
        with open('data/autoavaliacao.json', 'r') as f:
          data = json.load(f)

          data.append(autovaliacao_dict)
          
          with open('data/autoavaliacao.json', 'w') as f:
            json.dump(data, f, indent=2)   
      except:
          autovaliacoes=[]

          autovaliacoes.append(autovaliacao_dict)

          with open('data/autoavaliacao.json', 'w') as f:
            json.dump(autovaliacoes, f, indent=2)

        

      for user in filtered_users:  
        avaliador = session['email']
        integrante = request.form.get(f"user_email_{user['email']}")
        sprint = session['sprint']
        turma_codigo = session['turma']
        nome_turma = turmas_dict.get(turma_codigo, '')
        time = session['time']
        nome_time = times_dict.get(time, 'nome')
        comunicacao = request.form.get(f"comunicacao_{user['email']}")
        texto_comunicacao = request.form.get(f"texto_comunicacao_{user['email']}")
        engajamento = request.form.get(f"engajamento_{user['email']}")
        texto_engajamento = request.form.get(f"texto_engajamento_{user['email']}")
        entrega = request.form.get(f"entrega_{user['email']}")
        texto_entrega = request.form.get(f"texto_entrega_{user['email']}")
        conhecimento = request.form.get(f"conhecimento_{user['email']}")
        texto_conhecimento = request.form.get(f"texto_conhecimento_{user['email']}")
        autogestao = request.form.get(f"autogestao_{user['email']}")
        texto_autogestao = request.form.get(f"texto_autogestao_{user['email']}")

        avaliacao_dict = {
          "avaliador": avaliador,
          "integrante": integrante,
          "sprint": sprint,
          "turma_codigo": turma_codigo,
          "turma_nome": nome_turma,
          "time": time,
          "time_nome": nome_time,
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

        try:
          with open('data/avaliacao.json', 'r') as f:
            avaliacoes = json.load(f)
          
            avaliacoes.append(avaliacao_dict)
          
            with open('data/avaliacao.json', 'w') as f:
              json.dump(avaliacoes, f, indent=2)
        except:
           avaliacoes=[]

           avaliacoes.append(avaliacao_dict)

           with open('data/avaliacao.json', 'w') as f:
              json.dump(avaliacoes, f, indent=2)

      session['count_avaliacao'] += 1

      with open("data/cadastro.json", "r") as f:
        users = json.load(f)

      for user in users:
        if user['email'] == session['email']:
            user['count_avaliacao'] += 1

      with open('data/cadastro.json', 'w') as u:
        json.dump(users, u, indent=2)

      return redirect(url_for('padroes.menu_integrante'))