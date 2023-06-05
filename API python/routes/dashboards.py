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
@bp.route("/dashboards_gerenciais")
def dashboards_gerenciais():

    df = pd.read_json('data/cadastro.json')
    aderencia_avaliacoes = df['count_avaliacao'].value_counts()

    fig = px.pie(aderencia_avaliacoes, names=aderencia_avaliacoes.index, values=aderencia_avaliacoes.values)
    figure = px.bar(df, x='turma', y='count_avaliacao', barmode='group', color='time')

    div_grafico = fig.to_html(full_html=False)
    div_grafico_sprint = figure.to_html(full_html=False)

    return render_template('admin/dashboards_gerenciais.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'],div_grafico=div_grafico)


    # with open("data/avaliacao.json", "r") as file:
    #     data = json.load(file)
    #     df = pd.DataFrame(data)

    # def calculo_sprint(competencia):
    #     soma_comu = 0 
    #     qtd_comu = 0

    #     for i in data:
    #         soma_comu += i[competencia] 
    #         qtd_comu += 1
        
    #     return (soma_comu / qtd_comu)

    # fig = go.Figure()

    # fig.add_trace(go.Bar(
    #     x=['sprint'],
    #     y=[calculo_sprint('comunicacao')]
    # ))

    # fig.update_layout(
    #     autosize=False,
    #     width=500,
    #     height=500,
    #     yaxis=dict(
    #         title_text="Média das notas",
    #         tickvals=[1, 2, 3, 4],
    #         tickmode="array",
    #         titlefont=dict(size=30),
    #     )
    # )
    # fig.add_trace(go.Bar(
    #         x=['sprint'],
    #         y=[calculo_sprint('engajamento')]
    #     ))

    # fig.update_layout(
    #     autosize=False,
    #     width=500,
    #     height=500,
    #     yaxis=dict(
    #         title_text="Média das notas",
    #         tickvals=[1, 2, 3, 4],
    #         tickmode="array",
    #         titlefont=dict(size=30),
    #     )
    # )

    # fig.add_trace(go.Bar(
    #         x=['sprint'],
    #         y=[calculo_sprint('conhecimento')]
    #     ))

    # fig.update_layout(
    #     autosize=False,
    #     width=500,
    #     height=500,
    #     yaxis=dict(
    #         title_text="Média das notas",
    #         tickvals=[1, 2, 3, 4],
    #         tickmode="array",
    #         titlefont=dict(size=30),
    #     )
    # )

    # fig.add_trace(go.Bar(
    #         x=['sprint'],
    #         y=[calculo_sprint('entrega')]
    #     ))

    # fig.update_layout(
    #     autosize=False,
    #     width=500,
    #     height=500,
    #     yaxis=dict(
    #         title_text="Média das notas",
    #         tickvals=[1, 2, 3, 4],
    #         tickmode="array",
    #         titlefont=dict(size=30),
    #     )
    # )

    # fig.add_trace(go.Bar(
    #         x=['sprint'],
    #         y=[calculo_sprint('autogestao')]
    #     ))

    # fig.update_layout(
    #     autosize=False,
    #     width=500,
    #     height=500,
    #     yaxis=dict(
    #         title_text="Média das notas",
    #         tickvals=[1, 2, 3, 4],
    #         tickmode="array",
    #         titlefont=dict(size=30),
    #     )
    # )

    # fig.update_yaxes(automargin=True)

    
    # div_grafico = fig.to_html(full_html=False)

    # return render_template('admin/dashboards_gerenciais.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'],div_grafico=div_grafico)
