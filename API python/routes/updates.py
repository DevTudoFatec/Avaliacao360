from flask import render_template, request, redirect, url_for, session, Blueprint as bp
import json
from datetime import datetime, timedelta
from utils.decorators import login_required, admin_required


bp = bp('updates', __name__)

###### ADMINISTRADOR  #############

@bp.route("/update_turmas", methods=["POST"])
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
    
    editing = False
    confirm_delete = False

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

        return redirect(url_for('controles.controle_turmas'))
    
    elif "delete" in request.form:
        confirm_delete = True

    elif "confirm_del" in request.form:

        try:
            with open("data/projetos.json", "r") as f:
                projetos = json.load(f)
        except:
            projetos = []

        

        for turma in turmas:
          if turma['index'] == index:
            turmas.remove(turma)  
            
            for projeto in projetos:
               if projeto['turma'] == turma['codigo']:
                  projetos.remove(projeto)

            for user in users:
               if user['turma'] == turma['codigo']:
                  users.remove(user)

        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)          

        with open("data/projetos.json", "w") as file:
            json.dump(projetos, file, indent=2)

        with open("data/turmas.json", "w") as file:
            json.dump(turmas, file, indent=2)
          
        return redirect(url_for('controles.controle_turmas'))

    return render_template('admin/controle_turmas.html', dashboard_check=session['dashboard_check'], confirm_delete=confirm_delete, page=page, users=users, turmas=turmas, times=times, editing=editing, index=index, darkmode=session['darkmode'])

@bp.route("/update_times", methods=["POST"])
@login_required
@admin_required
def update_times():
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
    
    confirm_delete = False
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

        return redirect(url_for('controles.controle_times'))
    
    elif "delete" in request.form:
        confirm_delete = True

    elif "confirm_del" in request.form:

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
          
        return redirect(url_for('controles.controle_times'))

    return render_template('admin/controle_times.html', dashboard_check=session['dashboard_check'], confirm_delete=confirm_delete, users=users, turmas=turmas, times=times, editing=editing, index=index, darkmode=session['darkmode'])



@bp.route("/update_projetos", methods=["POST"])
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
    confirm_delete = False

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

        return redirect(url_for('controles.controle_projetos'))
    
    elif "delete" in request.form:
        confirm_delete = True

    elif "confirm_del" in request.form:

        for projeto in projetos:
            if projeto['index'] == index:
                for user in users:
                    if user['turma'] == projeto['turma']:
                        user['avaliacoes'] = []
                        user['count_avaliacao'] = 0
                projetos.remove(projeto)

        with open("data/projetos.json", "w") as file:
            json.dump(projetos, file, indent=2)
        
        with open("data/cadastro.json", "w") as file:
            json.dump(users, file, indent=2)

        return redirect(url_for('controles.controle_projetos'))

    return render_template('admin/controle_projetos.html', dashboard_check=session['dashboard_check'], confirm_delete=confirm_delete, index=index, editing=editing, users=users, turmas=turmas, projetos=projetos, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])
