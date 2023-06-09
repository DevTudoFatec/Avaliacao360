from flask import render_template, request, redirect, url_for, session, Blueprint as bp
import json
from utils.decorators import login_required, admin_required
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
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
    qtia_sprints = None

    if "save_turma" in request.form:
        turma_escolha = request.form.get("turma_escolha")
        times = [time for time in times if time['turma'] == turma_escolha]
        qtia_sprints = len([projeto['avaliacoes'] for projeto in projetos if projeto['turma'] == turma_escolha][0])
        select_time = True

    if "filtrar" in request.form:
        turma_escolha = request.form.get("turma_escolha")
        time_escolha = int(request.form.get("time_escolha"))
        sprint_escolha = int(request.form.get("sprint_escolha"))

        notas_medias_time = {}
        notas_medias_integrante = {}
        notas_medias_turma = {}

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
        turma_figures = []

        for sprint, sprint_data in notas_medias_turma.items():
            if sprint_escolha !=0:
                if sprint == sprint_escolha:
                    df = pd.DataFrame(sprint_data)
                    df = df.mean().reset_index()
                    df.columns = ['critério', 'nota média']
                    fig = px.bar(df, x='critério', y='nota média', color="critério", title=f'Avaliação Média - Sprint {sprint}')
                    turma_figures.append(fig.to_html(full_html=False))
            else: 
                df = pd.DataFrame(sprint_data)
                df = df.mean().reset_index()
                df.columns = ['critério', 'nota média']
                df['sprint'] = sprint
                turma_merged = pd.concat([turma_merged, df], ignore_index=True)

        time_merged = pd.DataFrame()
        time_figures = []
        for sprint, sprint_data in notas_medias_time.items():
            if sprint_escolha !=0:
                if sprint == sprint_escolha:
                    df = pd.DataFrame(sprint_data)
                    df = df.mean().reset_index()
                    df.columns = ['critério', 'nota média']
                    fig = px.bar(df, x='critério', y='nota média', color="critério", title=f'Avaliação Média - Sprint {sprint}')
                    time_figures.append(fig.to_html(full_html=False))
            else: 
                df = pd.DataFrame(sprint_data)
                df = df.mean().reset_index()
                df.columns = ['critério', 'nota média']
                df['sprint'] = sprint
                time_merged = pd.concat([time_merged, df], ignore_index=True)


        integrante_merged = pd.DataFrame()
        integrante_figures = []
        for integrante, integrante_data in notas_medias_integrante.items():
            for sprint, sprint_data in integrante_data.items():
                if sprint_escolha !=0:
                    if sprint == sprint_escolha:
                        df = pd.DataFrame(sprint_data)
                        df = df.mean().reset_index()
                        df.columns = ['critério', 'nota média']
                        nome_integrante = [user['nome'] for user in users if user['email'] == integrante][0]
                        fig = px.bar(df, x='critério', y='nota média', color="critério", title=f'Avaliação Média - Sprint {sprint} -  {nome_integrante} ')
                        integrante_figures.append(fig.to_html(full_html=False))
                else: 
                    df = pd.DataFrame(sprint_data)
                    df = df.mean().reset_index()
                    df.columns = ['critério', 'nota média']
                    df['sprint'] = sprint
                    df['integrante'] = [user['nome'] for user in users if user['email'] == integrante][0]
                    integrante_merged = pd.concat([integrante_merged, df], ignore_index=True)

        if sprint_escolha == 0:
            turma_merged['sprint'] = 'Sprint ' + turma_merged['sprint'].astype(str)
            fig = px.bar(turma_merged, x='critério', y='nota média',color='sprint',
                        title='Avaliação Média - Todas Sprints', labels={'sprint': 'Sprint'}, barmode='group')
            turma_figures.append(fig.to_html(full_html=False))
    
            time_merged['sprint'] = 'Sprint ' + time_merged['sprint'].astype(str)
            fig = px.bar(time_merged, x='critério', y='nota média', color='sprint',
                        title='Avaliação Média - Todas Sprints', labels={'sprint': 'Sprint'}, barmode='group')
            time_figures.append(fig.to_html(full_html=False))

            integrante_merged['sprint'] = 'Sprint ' + integrante_merged['sprint'].astype(str)
            fig = px.bar(integrante_merged, x='critério', y='nota média', color='sprint',
                                facet_row='integrante', title='Avaliação Média - Todas Sprints', barmode='group')
            integrante_figures.append(fig.to_html(full_html=False))
        
        return render_template('admin/dashboards_operacionais.html', show_dashboards=show_dashboards, turma_escolha=turma_escolha, time_escolha=time_escolha, select_time=select_time, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], times=times, turmas=turmas, turma_figures=turma_figures, time_figures=time_figures, integrante_figures=integrante_figures)

    return render_template('admin/dashboards_operacionais.html', show_dashboards=show_dashboards, qtia_sprints=qtia_sprints, select_time=select_time, turma_escolha=turma_escolha, nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], times=times, turmas=turmas)


@login_required
@admin_required
@bp.route("/dashboards_gerenciais", methods=['GET', 'POST'])
def dashboards_gerenciais():
    if request.method == 'POST':
        # Capturar os valores selecionados nos campos de seleção
        turma = request.form.get('turma')
        time = request.form.get('time')
        # Carregar o DataFrame completo
        df = pd.read_json('data/cadastro.json')
        
        # Verificar se os campos de seleção foram preenchidos
        if turma and time:
            # Filtrar o DataFrame com base nos valores selecionados
            df_filtered = df[(df['turma'] == turma) & (df['time'] == int(time))]
        elif turma:
            df_filtered = df[df['turma'] == turma]
        elif time:
            df_filtered = df[df['time'] == int(time)]
        else:
            df_filtered = df
    else:
        df_filtered = pd.read_json('data/cadastro.json')

    turmas = df_filtered['turma'].unique()
    times = df_filtered['time'].unique()

    aderencia_avaliacoes_geral = df_filtered['count_avaliacao'].value_counts()
    # aderencia_avaliacoes_geral.index = ['OK', 'Pendente']  # Renomeando os índices
    fig = px.pie(aderencia_avaliacoes_geral, names=aderencia_avaliacoes_geral.index, values=aderencia_avaliacoes_geral.values, color_discrete_sequence=['#41B8D5', '#6CE5E8'])
    fig.update_traces(text=['OK', 'Pendente']) 
    fig.update_layout(showlegend=False)

    # Gráfico por sprints
    df_filtered['avaliacoes'] = df_filtered['avaliacoes'].apply(json.dumps)

    df_respondidas = df_filtered[df_filtered['count_avaliacao'] == 1]
    df_pendentes = df_filtered[df_filtered['count_avaliacao'] == 0]

    df_respondidas['Status'] = 'OK'
    df_pendentes['Status'] = 'Pendente'

    df_combined = pd.concat([df_respondidas, df_pendentes])

    figure = px.bar(df_combined, x='avaliacoes', color='Status', barmode='group', color_discrete_sequence=['#41B8D5', '#6CE5E8'])

    div_grafico = fig.to_html(full_html=False)
    div_grafico_sprint = figure.to_html(full_html=False)

    return render_template('admin/dashboards_gerenciais.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], div_grafico=div_grafico, div_grafico_sprint=div_grafico_sprint, turmas=turmas, times=times)

