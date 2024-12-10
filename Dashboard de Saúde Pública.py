import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Carregar o dataset
df = pd.read_csv('Life-Expectancy-Data-Averaged.csv')

# Gráfico 1: Percentual de vacinação por região
vaccination_data = df.groupby('Region')[['Hepatitis_B', 'Polio', 'Diphtheria']].mean().reset_index()
vaccination_melted = vaccination_data.melt(id_vars='Region',
                                           value_vars=['Hepatitis_B', 'Polio', 'Diphtheria'],
                                           var_name='Vaccine',
                                           value_name='Percentage')
fig_vaccination = px.bar(vaccination_melted,
                         x='Region',
                         y='Percentage',
                         color='Vaccine',
                         barmode='group',
                         title='Percentual de Vacinação por Região',
                         labels={'Percentage': 'Percentual (%)', 'Region': 'Região', 'Vaccine': 'Vacina'})

# Gráfico 2: Mortalidade infantil x Vacinação contra Hepatite B
fig_mortality = px.scatter(df,
                           x='Hepatitis_B',
                           y='Infant_deaths',
                           color='Region',
                           title='Relação entre Mortalidade Infantil e Vacinação contra Hepatite B',
                           labels={'Hepatitis_B': 'Vacinação contra Hepatite B (%)',
                                   'Infant_deaths': 'Mortalidade Infantil'})

# Gráfico 3: Heatmap de correlação
correlation_data = df[['Life_expectancy', 'Infant_deaths', 'Adult_mortality']]
correlation_matrix = correlation_data.corr()
fig_heatmap = px.imshow(correlation_matrix,
                        text_auto=True,
                        color_continuous_scale='Viridis',
                        title='Correlação entre Expectativa de Vida, Mortalidade Infantil e Adultos')

# Gráfico 4: Expectativa de vida ao longo dos anos
fig_life_expectancy = px.line(df,
                              x='Year',
                              y='Life_expectancy',
                              color='Region',
                              title='Expectativa de Vida ao Longo dos Anos por Região',
                              labels={'Life_expectancy': 'Expectativa de Vida', 'Year': 'Ano'})

# Criar o aplicativo Dash
app = Dash(__name__)

# Layout do Dash
app.layout = html.Div([
    html.H1("Dashboard de Saúde Pública", style={'textAlign': 'center', 'marginBottom': '20px'}),
    dcc.Graph(figure=fig_vaccination),  # Gráfico de barras
    dcc.Graph(figure=fig_mortality),    # Scatterplot
    dcc.Graph(figure=fig_heatmap),      # Heatmap
    dcc.Graph(figure=fig_life_expectancy)  # Gráfico de linha
])

# Executar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
