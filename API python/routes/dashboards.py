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
@bp.route("/dashboards_operacionais")
def dashboards_operacionais():
    # Carregar dados do arquivo JSON
    with open('data/avaliacao.json') as file:
        data = json.load(file)

    # Dicionários para armazenar as notas médias
    notas_medias_turma = {}
    notas_medias_time = {}
    notas_medias_integrante = {}

    # Iterar sobre os dados e calcular as notas médias
    for item in data:
        avaliador = item['avaliador']
        integrante = item['integrante']
        sprint = item['sprint']
        turma_nome = item['turma_nome']
        time_nome = item['time_nome']
        comunicacao = item['comunicacao']
        engajamento = item['engajamento']
        conhecimento = item['conhecimento']
        entrega = item['entrega']
        autogestao = item['autogestao']

        # Adicionar as notas à média da turma
        notas_medias_turma.setdefault(turma_nome, {}).setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
        notas_medias_turma.setdefault(turma_nome, {}).setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
        notas_medias_turma.setdefault(turma_nome, {}).setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
        notas_medias_turma.setdefault(turma_nome, {}).setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
        notas_medias_turma.setdefault(turma_nome, {}).setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)

        # Adicionar as notas à média do time
        notas_medias_time.setdefault(turma_nome, {}).setdefault(time_nome, {}).setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
        notas_medias_time.setdefault(turma_nome, {}).setdefault(time_nome, {}).setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
        notas_medias_time.setdefault(turma_nome, {}).setdefault(time_nome, {}).setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
        notas_medias_time.setdefault(turma_nome, {}).setdefault(time_nome, {}).setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
        notas_medias_time.setdefault(turma_nome, {}).setdefault(time_nome, {}).setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)

        # Adicionar as notas à média do integrante
        notas_medias_integrante.setdefault(turma_nome, {}).setdefault(time_nome, {}).setdefault(integrante, {}).setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
        notas_medias_integrante.setdefault(turma_nome, {}).setdefault(time_nome, {}).setdefault(integrante, {}).setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
        notas_medias_integrante.setdefault(turma_nome, {}).setdefault(time_nome, {}).setdefault(integrante, {}).setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
        notas_medias_integrante.setdefault(turma_nome, {}).setdefault(time_nome, {}).setdefault(integrante, {}).setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
        notas_medias_integrante.setdefault(turma_nome, {}).setdefault(time_nome, {}).setdefault(integrante, {}).setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)

    # Criar gráficos para as médias das turmas
    turma_figures = []
    for turma, turma_data in notas_medias_turma.items():
        for sprint, sprint_data in turma_data.items():
            df = pd.DataFrame(sprint_data)
            df = df.mean().reset_index()
            df.columns = ['critério', 'nota média']
            fig = px.bar(df, x='critério', y='nota média', title=f'Avaliação Média - Turma {turma} - Sprint {sprint}')
            turma_figures.append(fig.to_html(full_html=False))

    # Criar gráficos para as médias dos times
    time_figures = []
    for turma, turma_data in notas_medias_time.items():
        for time, time_data in turma_data.items():
            for sprint, sprint_data in time_data.items():
                df = pd.DataFrame(sprint_data)
                df = df.mean().reset_index()
                df.columns = ['critério', 'nota média']
                fig = px.bar(df, x='critério', y='nota média', title=f'Avaliação Média - Turma {turma} - Time {time} - Sprint {sprint}')
                time_figures.append(fig.to_html(full_html=False))

    # Criar gráficos para as médias dos integrantes
    integrante_figures = []
    for turma, turma_data in notas_medias_integrante.items():
        for time, time_data in turma_data.items():
            for integrante, integrante_data in time_data.items():
                for sprint, sprint_data in integrante_data.items():
                    df = pd.DataFrame(sprint_data)
                    df = df.mean().reset_index()
                    df.columns = ['critério', 'nota média']
                    fig = px.bar(df, x='critério', y='nota média', title=f'Avaliação Média - Turma {turma} - Time {time} - Integrante {integrante} - Sprint {sprint}')
                    integrante_figures.append(fig.to_html(full_html=False))

    # Renderizar o template com os gráficos
    return render_template('admin/dashboards_operacionais.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'], turma_figures=turma_figures, time_figures=time_figures, integrante_figures=integrante_figures)


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

