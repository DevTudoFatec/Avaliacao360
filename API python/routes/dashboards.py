from flask import render_template, request, redirect, url_for, session, Blueprint as bp
import json
from utils.decorators import login_required, admin_required
import plotly.graph_objects as go
from dash import Dash, html, dcc
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
    with open("data/avaliacao.json", "r") as file:
        data = json.load(file)
        df = pd.DataFrame(data)

    def calculo_sprint(competencia):
        soma_comu = 0 
        qtd_comu = 0

        for i in data:
            soma_comu += i[competencia] 
            qtd_comu += 1
        
        return (soma_comu / qtd_comu)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=['sprint'],
        y=[calculo_sprint('comunicacao')]
    ))

    fig.update_layout(
        autosize=False,
        width=500,
        height=500,
        yaxis=dict(
            title_text="Média das notas",
            tickvals=[1, 2, 3, 4],
            tickmode="array",
            titlefont=dict(size=30),
        )
    )
    fig.add_trace(go.Bar(
            x=['sprint'],
            y=[calculo_sprint('engajamento')]
        ))

    fig.update_layout(
        autosize=False,
        width=500,
        height=500,
        yaxis=dict(
            tickvals=[1, 2, 3, 4],
            tickmode="array",
            titlefont=dict(size=30),
            )
        )
    fig.update_yaxes(automargin=True)

    
    div_grafico = fig.to_html(full_html=False)

    return render_template('admin/dashboards_gerenciais.html', nomeUsuario=session['nomeUsuario'], darkmode=session['darkmode'],div_grafico=div_grafico)
