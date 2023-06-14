from flask import render_template, request, session, Blueprint as bp
import json
from utils.decorators import login_required, admin_required, data_required
import plotly.express as px
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

bp = bp('dashboards', __name__)

@login_required
@admin_required
@data_required
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

    turmas = [turma for turma in turmas if turma['codigo'] in [avaliacao['turma_codigo'] for avaliacao in avaliacoes]]  

    select_time = False
    turma_escolha = None
    show_dashboards = False

    if "save_turma" in request.form:
        turma_escolha = request.form.get("turma_escolha")
        times = [time for time in times if time['turma'] == turma_escolha and time['codigo'] in [avaliacao['time'] for avaliacao in avaliacoes]]
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
                notas_medias_turma.setdefault('geral', {}).setdefault('comunicacao', []).append(comunicacao)
                notas_medias_turma.setdefault('geral', {}).setdefault('engajamento', []).append(engajamento)
                notas_medias_turma.setdefault('geral', {}).setdefault('conhecimento', []).append(conhecimento)
                notas_medias_turma.setdefault('geral', {}).setdefault('entrega', []).append(entrega)
                notas_medias_turma.setdefault('geral', {}).setdefault('autogestao', []).append(autogestao)

                if item['time'] == time_escolha:
                    notas_medias_time.setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_time.setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_time.setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_time.setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
                    notas_medias_time.setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)
                    notas_medias_time.setdefault('geral', {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_time.setdefault('geral', {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_time.setdefault('geral', {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_time.setdefault('geral', {}).setdefault('entrega', []).append(entrega)
                    notas_medias_time.setdefault('geral', {}).setdefault('autogestao', []).append(autogestao)

                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault('geral', {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault('geral', {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault('geral', {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault('geral', {}).setdefault('entrega', []).append(entrega)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault('geral', {}).setdefault('autogestao', []).append(autogestao)
        
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

        turma_merged['sprint'] = turma_merged['sprint'].apply(lambda x: 'Sprint ' + str(x) if x != 'geral' else 'ZZZ Geral')
        turma_merged = turma_merged.sort_values(by='sprint')
        turma_merged['sprint'] = turma_merged['sprint'].apply(lambda x: 'Geral' if x == 'ZZZ Geral' else x.replace('Sprint ', ''))

        fig = px.bar(turma_merged, x='critério', y='nota média',color='sprint',
                    title=f'{turma_nome} - Avaliação Média', labels={'sprint': 'Sprint'}, barmode='group', 
                    color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                    )
        if session['darkmode']:
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )
        turma_figures.append(fig.to_html(full_html=False))

        time_merged['sprint'] = time_merged['sprint'].apply(lambda x: 'Sprint ' + str(x) if x != 'geral' else 'ZZZ Geral')
        time_merged = time_merged.sort_values(by='sprint')
        time_merged['sprint'] = time_merged['sprint'].apply(lambda x: 'Geral' if x == 'ZZZ Geral' else x.replace('Sprint ', ''))

        fig = px.bar(time_merged, x='critério', y='nota média', color='sprint',
                    title=f'{time_nome} - Avaliação Média', labels={'sprint': 'Sprint'}, barmode='group', 
                    color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
        if session['darkmode']:
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )
        time_figures.append(fig.to_html(full_html=False))
        
        integrante_merged['sprint'] = integrante_merged['sprint'].apply(lambda x: 'Sprint ' + str(x) if x != 'geral' else 'ZZZ Geral')
        integrante_merged = integrante_merged.sort_values(by='sprint')
        integrante_merged['sprint'] = integrante_merged['sprint'].apply(lambda x: 'Geral' if x == 'ZZZ Geral' else x.replace('Sprint ', ''))

        fig = px.bar(integrante_merged, x='critério', y='nota média', color='sprint', facet_col_wrap=2,
                            facet_col='nome_integrante', title='Integrantes - Avaliação Média', 
                            labels={'sprint': 'Sprint', 'nome_integrante': 'Integrante'}, barmode='group', 
                    color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
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
                notas_medias_turma.setdefault('geral', {}).setdefault('comunicacao', []).append(comunicacao)
                notas_medias_turma.setdefault('geral', {}).setdefault('engajamento', []).append(engajamento)
                notas_medias_turma.setdefault('geral', {}).setdefault('conhecimento', []).append(conhecimento)
                notas_medias_turma.setdefault('geral', {}).setdefault('entrega', []).append(entrega)
                notas_medias_turma.setdefault('geral', {}).setdefault('autogestao', []).append(autogestao)

                if item['time'] == time_escolha:
                    notas_medias_time.setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_time.setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_time.setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_time.setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
                    notas_medias_time.setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)
                    notas_medias_time.setdefault('geral', {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_time.setdefault('geral', {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_time.setdefault('geral', {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_time.setdefault('geral', {}).setdefault('entrega', []).append(entrega)
                    notas_medias_time.setdefault('geral', {}).setdefault('autogestao', []).append(autogestao)

                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('entrega', []).append(entrega)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault(sprint, {}).setdefault('autogestao', []).append(autogestao)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault('geral', {}).setdefault('comunicacao', []).append(comunicacao)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault('geral', {}).setdefault('engajamento', []).append(engajamento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault('geral', {}).setdefault('conhecimento', []).append(conhecimento)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault('geral', {}).setdefault('entrega', []).append(entrega)
                    notas_medias_integrante.setdefault(integrante, {}).setdefault('geral', {}).setdefault('autogestao', []).append(autogestao)
        
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

        turma_merged['sprint'] = turma_merged['sprint'].apply(lambda x: 'Sprint ' + str(x) if x != 'geral' else 'ZZZ Geral')
        turma_merged = turma_merged.sort_values(by='sprint')        
        turma_merged['sprint'] = turma_merged['sprint'].apply(lambda x: 'Geral' if x == 'ZZZ Geral' else x.replace('Sprint ', ''))

        fig = px.bar(turma_merged, x='critério', y='nota média',color='sprint',
                    title=f'{turma_nome} - AutoAvaliação Média', labels={'sprint': 'Sprint'}, barmode='group', 
                    color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                    )
        if session['darkmode']:
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )
        turma_figures.append(fig.to_html(full_html=False))

        time_merged['sprint'] = time_merged['sprint'].apply(lambda x: 'Sprint ' + str(x) if x != 'geral' else 'ZZZ Geral')
        time_merged = time_merged.sort_values(by='sprint')
        time_merged['sprint'] = time_merged['sprint'].apply(lambda x: 'Geral' if x == 'ZZZ Geral' else x.replace('Sprint ', ''))

        fig = px.bar(time_merged, x='critério', y='nota média', color='sprint',
                    title=f'{time_nome} - AutoAvaliação Média', labels={'sprint': 'Sprint'}, barmode='group', 
                    color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
        if session['darkmode']:
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )
        time_figures.append(fig.to_html(full_html=False))

        integrante_merged['sprint'] = integrante_merged['sprint'].apply(lambda x: 'Sprint ' + str(x) if x != 'geral' else 'ZZZ Geral')
        integrante_merged = integrante_merged.sort_values(by='sprint')
        integrante_merged['sprint'] = integrante_merged['sprint'].apply(lambda x: 'Geral' if x == 'ZZZ Geral' else x.replace('Sprint ', ''))


        fig = px.bar(integrante_merged, x='critério', y='nota média', color='sprint', facet_col_wrap=2,
                            facet_col='nome_integrante', title='Integrantes - AutoAvaliação Média', 
                            labels={'sprint': 'Sprint', 'nome_integrante': 'Integrante'}, barmode='group', 
                    color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
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
@data_required
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

    turmas = [turma for turma in turmas if turma['codigo'] in [avaliacao['turma_codigo'] for avaliacao in avaliacoes]]
    
    select_time = False
    turma_escolha = None
    show_dashboards = False
    
    turma_nome = None
    time_nome = None

    avaliacoes_check = {}
    div_grafico = None
    div_grafico_sprint = None


    if "save_turma" in request.form:
        turma_escolha = request.form.get("turma_escolha")
        times = [time for time in times if time['turma'] == turma_escolha and time['codigo'] in [avaliacao['time'] for avaliacao in avaliacoes]]
        select_time = True
        turma_nome = [turma['nome'] for turma in turmas if turma['codigo'] == turma_escolha][0]

    if "filtrar" in request.form:
        show_dashboards = True

        turma_escolha = request.form.get("turma_escolha")
        time_escolha = int(request.form.get("time_escolha"))

        avaliacoes_abertas = [date[0] for date in ([projeto['avaliacoes'] for projeto in projetos if projeto['turma'] == turma_escolha][0]) if datetime.strptime(date[1], '%d-%m-%Y').date() <= datetime.now().date()]
        
        turma_nome = [turma['nome'] for turma in turmas if turma['codigo'] == turma_escolha][0]
        time_nome = [time['nome'] for time in times if time['codigo'] == time_escolha][0]

        time_users = [user['email'] for user in users if user['time'] == time_escolha]

        [avaliacoes_check.setdefault(avaliacao['avaliador'], []).append(avaliacao['sprint']) for avaliacao in avaliacoes if avaliacao['sprint'] in avaliacoes_abertas and avaliacao['avaliador'] in time_users ]

        for item in avaliacoes_check:
            avaliacoes_check[item] = list(set(avaliacoes_check[item]))

        max_sprint = max(max(max(avaliacoes_check.values(), key=lambda x: max(x))), 1)
        df_data = {
            'Identifier': list(avaliacoes_check.keys())
        }

        for i in range(1, max_sprint + 1):
            df_data[str(i)] = [i in values for values in avaliacoes_check.values()]

        df = pd.DataFrame(df_data)

        counts_true = df.iloc[:, 1:].sum()
        counts_false = df.iloc[:, 1:].count() - counts_true

        fig_column = go.Figure()
        fig_column.add_trace(go.Bar(x=counts_true.index, y=counts_true, name='Ok', marker={'color': 'rgb(0, 100, 0)'}))
        fig_column.add_trace(go.Bar(x=counts_false.index, y=counts_false, name='Pendente', marker={'color': 'rgb(139, 0, 0)'}))

        fig_column.update_layout(
            barmode='group', 
            xaxis_title='Sprints', 
            yaxis_title='Quantia',
            title=f"{time_nome} - Contagem de Status 'Ok' e 'Pendente' por Sprint"
        )

        traces = []

        for column in df.columns[1:]:
            counts = df[column].value_counts().reindex([True, False], fill_value=0)
            labels = ['Ok', 'Pendente']
            percentages = [count / counts.sum() * 100 for count in counts]
            trace = go.Pie(
                labels=labels, 
                values=percentages, 
                name=column,
                marker={'colors': ['rgb(0, 100, 0)', 'rgb(139, 0, 0)']})
            traces.append(trace)

        layout = go.Layout(
            title=f"{time_nome} - Porcentagem de Status 'Ok' e 'Pendente' por Sprint",
            updatemenus=[
                dict(
                    active=0,
                    buttons=[
                        dict(
                            label=f"Sprint {column}",
                            method='update',
                            args=[{'visible': [column == trace.name for trace in traces]}],
                        )
                        for column in df.columns[1:]
                    ],
                )
            ]
        )

        fig_pie = go.Figure(data=traces, layout=layout)

        
        if session['darkmode']:
            fig_column.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )

            fig_pie.update_layout(
                template="plotly_dark",
                plot_bgcolor='lightgray'
            )

        div_grafico = fig_pie.to_html(full_html=False)
        div_grafico_sprint = fig_column.to_html(full_html=False)
        
        

    return render_template('admin/dashboards_gerenciais.html', nomeUsuario=session['nomeUsuario'], 
                           darkmode=session['darkmode'], turma_nome=turma_nome, time_nome=time_nome,
                           show_dashboards=show_dashboards, select_time=select_time,  
                           times=times, turma_escolha=turma_escolha, turmas=turmas,
                           div_grafico_sprint=div_grafico_sprint, div_grafico=div_grafico)

