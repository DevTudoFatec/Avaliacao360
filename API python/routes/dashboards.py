from flask import render_template, request, session, Blueprint as bp
import json
from utils.decorators import login_required, admin_required
import plotly.express as px
import pandas as pd

bp = bp('dashboards', __name__)

@login_required
@admin_required
@bp.route("/dashboards_operacionais", methods=["GET", "POST"])
def dashboards_operacionais():
    # Carregar dados do arquivo JSON
    with open('data/avaliacao.json') as file:
        avaliacoes = json.load(file)

    with open('data/autoavaliacao.json') as file:
        autoavaliacoes = json.load(file)

    with open('data/cadastro.json') as file:
        users = json.load(file)    
    
    with open('data/turmas.json') as file:
        turmas = json.load(file)

    with open('data/times.json') as file:
        times = json.load(file)

    with open('data/projetos.json') as file:
        projetos = json.load(file)

    select_time = False
    turma_escolha = None
    show_dashboards = False

    if "save_turma" in request.form:
        turma_escolha = request.form.get("turma_escolha")
        times = [time for time in times if time['turma'] == turma_escolha]
        select_time = True

    if "filtrar" in request.form:
        show_dashboards = True

        turma_escolha = request.form.get("turma_escolha")
        time_escolha = int(request.form.get("time_escolha"))

        turma_nome = [turma['nome'] for turma in turmas if turma['codigo'] == turma_escolha][0]
        time_nome = [time['nome'] for time in times if time['codigo'] == time_escolha][0]

        turma_figures = []
        time_figures = []
        integrante_figures = []

        notas_medias_time = {}
        notas_medias_turma = {}
        notas_medias_integrante = {}

        for item in avaliacoes:
            if item['turma_codigo'] == turma_escolha:
                sprint = item['sprint']
                integrante = item['integrante']
                comunicacao = item['comunicacao']
                engajamento = item['engajamento']
                conhecimento = item['conhecimento']
                entrega = item['entrega']
                autogestao = item['autogestao']

                notas_medias_turma.setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
                notas_medias_turma.setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
                notas_medias_turma.setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
                notas_medias_turma.setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
                notas_medias_turma.setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)

                if item['time'] == time_escolha:
                    notas_medias_time.setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_time.setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_time.setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_time.setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
                    notas_medias_time.setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)

                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)
        
        turma_merged = pd.DataFrame()

        for sprint, sprint_data in notas_medias_turma.items():
            df = pd.DataFrame(sprint_data)
            df = df.mean().reset_index()
            df.columns = ['critério', 'nota média']
            df['sprint'] = sprint
            turma_merged = pd.concat([turma_merged, df], ignore_index=True)

        time_merged = pd.DataFrame()

        for sprint, sprint_data in notas_medias_time.items():
            df = pd.DataFrame(sprint_data)
            df = df.mean().reset_index()
            df.columns = ['critério', 'nota média']
            df['sprint'] = sprint
            time_merged = pd.concat([time_merged, df], ignore_index=True)


        integrante_merged = pd.DataFrame()

        for integrante, integrante_data in notas_medias_integrante.items():
            for sprint, sprint_data in integrante_data.items():
                df = pd.DataFrame(sprint_data)
                df = df.mean().reset_index()
                df.columns = ['critério', 'nota média']
                df['sprint'] = sprint
                df['integrante'] = integrante
                df['nome_integrante'] = [user['nome'] for user in users if user['email'] == integrante][0]
                integrante_merged = pd.concat([integrante_merged, df], ignore_index=True)

        turma_merged['sprint'] = 'Sprint ' + turma_merged['sprint'].astype(str)
        fig = px.bar(turma_merged, x='critério', y='nota média',color='sprint',
                    title=f'{turma_nome} - Avaliação Média', labels={'sprint': 'Sprint'}, barmode='group'
                    )
        if session['darkmode']:
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )
        turma_figures.append(fig.to_html(full_html=False))

        time_merged['sprint'] = 'Sprint ' + time_merged['sprint'].astype(str)
        fig = px.bar(time_merged, x='critério', y='nota média', color='sprint',
                    title=f'{time_nome} - Avaliação Média', labels={'sprint': 'Sprint'}, barmode='group')
        if session['darkmode']:
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )
        time_figures.append(fig.to_html(full_html=False))

        integrante_merged['sprint'] = 'Sprint ' + integrante_merged['sprint'].astype(str)
        fig = px.bar(integrante_merged, x='critério', y='nota média', color='sprint', facet_col_wrap=2,
                            facet_col='nome_integrante', title='Integrantes - Avaliação Média', 
                            labels={'sprint': 'Sprint', 'nome_integrante': 'Integrante'}, barmode='group')
        if session['darkmode']:
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )
        integrante_figures.append(fig.to_html(full_html=False))

        notas_medias_time = {}
        notas_medias_integrante = {}
        notas_medias_turma = {}

        for item in autoavaliacoes:
            if item['turma_codigo'] == turma_escolha:
                sprint = item['sprint']
                integrante = item['email']
                comunicacao = item['comunicacao']
                engajamento = item['engajamento']
                conhecimento = item['conhecimento']
                entrega = item['entrega']
                autogestao = item['autogestao']

                notas_medias_turma.setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
                notas_medias_turma.setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
                notas_medias_turma.setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
                notas_medias_turma.setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
                notas_medias_turma.setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)

                if item['time'] == time_escolha:
                    notas_medias_time.setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_time.setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_time.setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_time.setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
                    notas_medias_time.setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)

                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)
        
        turma_merged = pd.DataFrame()

        for sprint, sprint_data in notas_medias_turma.items():
            df = pd.DataFrame(sprint_data)
            df = df.mean().reset_index()
            df.columns = ['critério', 'nota média']
            df['sprint'] = sprint
            turma_merged = pd.concat([turma_merged, df], ignore_index=True)

        time_merged = pd.DataFrame()

        for sprint, sprint_data in notas_medias_time.items():
            df = pd.DataFrame(sprint_data)
            df = df.mean().reset_index()
            df.columns = ['critério', 'nota média']
            df['sprint'] = sprint
            time_merged = pd.concat([time_merged, df], ignore_index=True)


        integrante_merged = pd.DataFrame()

        for integrante, integrante_data in notas_medias_integrante.items():
            for sprint, sprint_data in integrante_data.items():
                df = pd.DataFrame(sprint_data)
                df = df.mean().reset_index()
                df.columns = ['critério', 'nota média']
                df['sprint'] = sprint
                df['integrante'] = integrante
                df['nome_integrante'] = [user['nome'] for user in users if user['email'] == integrante][0]
                integrante_merged = pd.concat([integrante_merged, df], ignore_index=True)

        turma_merged['sprint'] = 'Sprint ' + turma_merged['sprint'].astype(str)
        fig = px.bar(turma_merged, x='critério', y='nota média',color='sprint',
                    title=f'{turma_nome} - AutoAvaliação Média', labels={'sprint': 'Sprint'}, barmode='group'
                    )
        if session['darkmode']:
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )
        turma_figures.append(fig.to_html(full_html=False))

        time_merged['sprint'] = 'Sprint ' + time_merged['sprint'].astype(str)
        fig = px.bar(time_merged, x='critério', y='nota média', color='sprint',
                    title=f'{time_nome} - AutoAvaliação Média', labels={'sprint': 'Sprint'}, barmode='group')
        if session['darkmode']:
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )
        time_figures.append(fig.to_html(full_html=False))

        integrante_merged['sprint'] = 'Sprint ' + integrante_merged['sprint'].astype(str)
        fig = px.bar(integrante_merged, x='critério', y='nota média', color='sprint', facet_col_wrap=2,
                            facet_col='nome_integrante', title='Integrantes - AutoAvaliação Média', 
                            labels={'sprint': 'Sprint', 'nome_integrante': 'Integrante'}, barmode='group')
        if session['darkmode']:
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )
        integrante_figures.append(fig.to_html(full_html=False))

        
        return render_template('admin/dashboards_operacionais.html', show_dashboards=show_dashboards, turma_escolha=turma_escolha, time_escolha=time_escolha, select_time=select_time, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], times=times, turmas=turmas, turma_figures=turma_figures, time_figures=time_figures, integrante_figures=integrante_figures)

    return render_template('admin/dashboards_operacionais.html', show_dashboards=show_dashboards, select_time=select_time, turma_escolha=turma_escolha, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], times=times, turmas=turmas)


@login_required
@admin_required
@bp.route("/dashboards_gerenciais", methods=['GET', 'POST'])
def dashboards_gerenciais():
    with open('data/avaliacao.json') as file:
        avaliacoes = json.load(file)

    with open('data/cadastro.json') as file:
        users = json.load(file)    
    
    with open('data/turmas.json') as file:
        turmas = json.load(file)

    with open('data/times.json') as file:
        times = json.load(file)

    with open('data/projetos.json') as file:
        projetos = json.load(file)
    
    select_time = False
    turma_escolha = None
    show_dashboards = False
    
    turma_nome = None
    time_nome = None

    if "save_turma" in request.form:
        turma_escolha = request.form.get("turma_escolha")
        times = [time for time in times if time['turma'] == turma_escolha]
        select_time = True
        turma_nome = [turma['nome'] for turma in turmas if turma['codigo'] == turma_escolha][0]

    if "filtrar" in request.form:
        show_dashboards = True

        turma_escolha = request.form.get("turma_escolha")
        time_escolha = int(request.form.get("time_escolha"))

        turma_nome = [turma['nome'] for turma in turmas if turma['codigo'] == turma_escolha][0]
        time_nome = [time['nome'] for time in times if time['codigo'] == time_escolha][0]
        

    return render_template('admin/dashboards_gerenciais.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], turma_nome=turma_nome, show_dashboards=show_dashboards, select_time=select_time, turmas=turmas, times=times)

