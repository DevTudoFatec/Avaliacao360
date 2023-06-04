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
@bp.route("/dashboards_gerenciais", methods=['GET', 'POST'])
def dashboards_gerenciais():
    df = pd.read_json('data/cadastro.json')
    aderencia_avaliacoes = df['count_avaliacao'].value_counts()

    fig = px.pie(aderencia_avaliacoes, names=aderencia_avaliacoes.index, values=aderencia_avaliacoes.values)
    figure = px.bar(df, x='turma', y='count_avaliacao', barmode='group', color='time')

    div_grafico = fig.to_html(full_html=False)
    div_grafico_sprint = figure.to_html(full_html=False)

    return render_template('admin/dashboards_gerenciais.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'],div_grafico=div_grafico)


