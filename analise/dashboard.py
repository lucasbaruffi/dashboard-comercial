import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px

# Carrega as variáveis do .env
load_dotenv()
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# Cria a conexão com o MySQL
connection_string = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
engine = create_engine(connection_string)

# Consulta: Reuniões por dia (utilizando a data de início)
query_meetings_day = """
SELECT DATE(startTime) AS meeting_date, COUNT(*) AS total
FROM meetings
GROUP BY meeting_date
ORDER BY meeting_date;
"""
meetings_day_df = pd.read_sql(query_meetings_day, engine)

# Consulta: Reuniões por pessoa (usuário atribuído)
query_meetings_assigned = """
SELECT assignedUserId, COUNT(*) AS total
FROM meetings
GROUP BY assignedUserId
ORDER BY total DESC;
"""
meetings_assigned_df = pd.read_sql(query_meetings_assigned, engine)

# Consulta: Reuniões por quem criou (usando o nome do usuário)
query_meetings_created = """
SELECT u.name AS createdByName, COUNT(*) AS total
FROM meetings m
JOIN users u ON m.createdBy = u.id
GROUP BY u.name
ORDER BY total DESC;
"""
meetings_created_df = pd.read_sql(query_meetings_created, engine)

# Cria os gráficos com Plotly Express utilizando o template "plotly_white"
fig_day = px.bar(meetings_day_df, x="meeting_date", y="total", title="Reuniões por Dia",
                 labels={"meeting_date": "Data", "total": "Número de Reuniões"},
                 template="plotly_white")
fig_assigned = px.bar(meetings_assigned_df, x="assignedUserId", y="total", title="Reuniões por Pessoa (Atribuído)",
                      labels={"assignedUserId": "ID do Usuário", "total": "Número de Reuniões"},
                      template="plotly_white")
fig_created = px.bar(meetings_created_df, x="createdByName", y="total", title="Reuniões por Quem Criou",
                     labels={"createdByName": "Criado Por", "total": "Número de Reuniões"},
                     template="plotly_white")

# Configura o aplicativo Dash com um tema do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard de Reuniões - Agenciavfx"

# Layout utilizando componentes do Dash Bootstrap Components para um design mais limpo
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Dashboard de Reuniões - Agenciavfx", className="text-center my-4"))
        ),
        dbc.Row(
            dbc.Col(html.P("Visualização das reuniões com base em diferentes critérios:"), className="mb-4")
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="meetings-per-day", figure=fig_day), md=12)
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="meetings-per-assigned", figure=fig_assigned), md=6),
                dbc.Col(dcc.Graph(id="meetings-per-created", figure=fig_created), md=6),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)

if __name__ == '__main__':
    app.run(debug=True)
