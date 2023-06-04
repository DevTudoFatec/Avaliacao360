from flask import render_template, request, redirect, url_for, session, Blueprint as bp
import json
from utils.decorators import login_required, admin_required
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd

bp = bp('dashboards', __name__)

@login_required
@admin_required
@bp.route("/dashboards_operacionais")
def dashboards_operacionais():
    return render_template('admin/dashboards_operacionais.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'])

@login_required
@admin_required
@bp.route("/dashboards_gerenciais")
def dashboards_gerenciais():
 # Gráfico geral
    df = pd.read_json('data/cadastro.json')
    aderencia_avaliacoes_geral = df['count_avaliacao'].value_counts()
    aderencia_avaliacoes_geral.index = ['OK', 'Pendente']  # Renomeando os índices
    fig = px.pie(aderencia_avaliacoes_geral, names=aderencia_avaliacoes_geral.index, values=aderencia_avaliacoes_geral.values, color_discrete_sequence=['#41B8D5', '#6CE5E8'])

    #Gráfico por sprints
    df['avaliacoes'] = df['avaliacoes'].apply(json.dumps)

    df_respondidas = df[df['count_avaliacao'] == 1]
    df_pendentes = df[df['count_avaliacao'] == 0]

    df_respondidas['status'] = 'OK'
    df_pendentes['status'] = 'Pendente'

    df_combined = pd.concat([df_respondidas, df_pendentes])

    figure = px.bar(df_combined, x='avaliacoes', color='status', barmode='group', color_discrete_sequence=['#41B8D5', '#6CE5E8'])


    div_grafico = fig.to_html(full_html=False)
    div_grafico_sprint = figure.to_html(full_html=False)

    return render_template('admin/dashboards_gerenciais.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'],div_grafico=div_grafico, div_grafico_sprint=div_grafico_sprint)


