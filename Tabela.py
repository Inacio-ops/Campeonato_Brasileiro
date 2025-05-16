import streamlit as st
import pandas as pd
import plotly.express as px

# Dicionário de cores para os times
cores_times = {
    'Vitoria': '#D32F2F',  # Red
    'Vasco': '#000000',  # Black
    'Sport': '#D32F2F',  # Red
    'Sao Paulo': '#D32F2F',  # Red
    'Santos': '#000000',  # Black
    'Santo Andre': '#FBC02D',  # Yellow
    'Santa Cruz': '#D32F2F',  # Red
    'Prudente': '#FFA500',  # Orange
    'Portuguesa': '#009639',  # Green
    'Ponte Preta': '#000000',  # Black
    'Parana': '#003B5C',  # Blue
    'Palmeiras': '#009639',  # Green
    'Nautico': '#D32F2F',  # Red
    'Internacional': '#E60012',  # Red
    'Guarani': '#8BC34A',  # Light Green
    'Gremio': '#003B5C',  # Blue
    'Fluminense': '#FFA500',  # Orange
    'Flamengo': '#E60012',  # Red
    'Figueirense': '#000000',  # Black
    'Cruzeiro': '#003D7C',  # Blue
    'Criciuma': '#FBC02D',  # Yellow
    'Coritiba': '#006747',  # Green
    'Corinthians': '#000000',  # Black
    'Chapecoense': '#009639',  # Green
    'Ceara': '#1C1C1C',  # Black
    'Botafogo': '#000000',  # Black
    'Bahia': '#003D7C',  # Blue
    'Atletico-MG': '#000000',  # Black
    'Atletico-GO': '#D32F2F',  # Red
    'Athletico-PR': '#D32F2F',  # Red
    'America-MG': '#009639',  # Green
}

st.title('Dashboard Campeonato Brasileiro')

arquivo = 'C:/Users/Gabriel Inacio/Downloads/Tabela_Clubes.csv'
dados = pd.read_csv(arquivo)
dados = dados.loc[:, ~dados.columns.str.contains('^Unnamed')]

clubes = [
    'America-MG', 'Atletico-GO', 'Atletico-MG', 'Athletico-PR', 'Avai', 'Bahia', 'Botafogo',
    'Ceara', 'Chapecoense', 'Corinthians', 'Coritiba', 'Criciuma', 'Cruzeiro', 'Figueirense',
    'Flamengo', 'Fluminense', 'Goias', 'Gremio', 'Guarani', 'Internacional', 'Joinville',
    'Nautico', 'Palmeiras', 'Parana', 'Ponte Preta', 'Portuguesa', 'Prudente', 'Santa Cruz',
    'Santo Andre', 'Santos', 'Sao Paulo', 'Sport', 'Vasco', 'Vitoria']

st.sidebar.title('Filtros')

# — filtro de clubes —
clubes_disponiveis = sorted(dados['Clubes'].unique())
clubes_selecionados = st.sidebar.multiselect(
    'Selecione o(s) clube(s):',
    clubes_disponiveis,
    default= []  # todos por padrão
)

# — prepara Ano como inteiro para o slider —
dados['Ano'] = dados['Ano'].astype(int)
ano_min, ano_max = dados['Ano'].min(), dados['Ano'].max()

# — slider de período —
ano_inicio, ano_fim = st.sidebar.slider(
    'Período de Anos',
    min_value=ano_min,
    max_value=ano_max,
    value=(ano_min, ano_min),  # intervalo inicial
    step=1
)

# — agora converta Ano de volta pra string (se seus gráficos esperam string) —
dados['Ano'] = dados['Ano'].astype(str)

# — aplica os filtros —
dados_filtrados = dados[
    (dados['Clubes'].isin(clubes_selecionados)) &
    (dados['Ano'].astype(int).between(ano_inicio, ano_fim))
].copy()
 

dados['Ano'] = dados['Ano'].astype(int).astype(str)

dados[['Gols Feitos', 'Gols Sofridos']] = dados['GolsF/S'].str.split(':', expand=True)
dados['Gols Feitos'] = dados['Gols Feitos'].astype(int)
dados['Gols Sofridos'] = dados['Gols Sofridos'].astype(int)

dados.insert(6, 'Gols Feitos', dados.pop('Gols Feitos'))  # Insere a coluna "Gols Feitos" na posição 7
dados.insert(7, 'Gols Sofridos', dados.pop('Gols Sofridos'))  # Insere a coluna "Gols Sofridos" na posição 8

dados = dados.drop(columns=['GolsF/S'])

## Tabelas
### Tabelas campeoes
# Garante que a coluna "Pos." está no formato certo
dados['Pos.'] = dados['Pos.'].astype(str)
# Filtrar apenas os campeões (posição 1)
campeoes = dados[dados['Pos.'] == '1'].reset_index(drop=True)

##Numero de titulos
# Garante que a coluna "Pos." é string (se ainda não for)
dados['Pos.'] = dados['Pos.'].astype(str).str.strip()
# Filtra somente os campeões (posição 1)
campeoes = dados[dados['Pos.'].str.contains('^1\\D*$', na=False)]
# Conta quantas vezes cada clube foi campeão
titulos = campeoes['Clubes'].value_counts().reset_index()
titulos.columns = ['Clubes', 'Titulos']
# Ordena do maior pro menor
titulos = titulos.sort_values(by='Titulos', ascending=False).reset_index(drop=True)

##Numero de Vitorias por compeao
# Garante que 'Pos.' é texto sem espaços e filtra campeões
dados['Pos.'] = dados['Pos.'].astype(str).str.strip()
# Filtra os dados apenas dos campeões (posição 1)
campeoes = dados[dados['Pos.'].str.contains('^1\\D*$', na=False)].copy()
# Seleciona apenas as colunas relevantes
tabela_vitorias = campeoes[['Clubes', 'Ano', 'Vitorias']].copy()
# Renomeia a coluna para clareza
tabela_vitorias.columns = ['Clubes', 'Ano','Vitorias nos Titulos']
# Ordena do maior pro menor
tabela_vitorias = tabela_vitorias.sort_values(by=['Ano', 'Clubes']).reset_index(drop=True)


##Numero de derrotas por compeao
# Garante que 'Pos.' é texto sem espaços e filtra campeões
dados['Pos.'] = dados['Pos.'].astype(str).str.strip()
# Filtra os dados apenas dos campeões (posição 1)
campeoes = dados[dados['Pos.'].str.contains('^1\\D*$', na=False)].copy()
# Seleciona apenas as colunas relevantes
tabela_derrotas = campeoes[['Clubes','Ano', 'Derrotas']].copy()
# Renomeia a coluna para clareza
tabela_derrotas.columns = ['Clubes', 'Ano', 'Derrotas no Titulos']
# Ordena do maior pro menor
tabela_derrotas = tabela_derrotas.sort_values(by=['Derrotas no Titulos'], ascending=False).reset_index(drop=True)

##Numero de empates por compeao
# Garante que 'Pos.' é texto sem espaços e filtra campeões
dados['Pos.'] = dados['Pos.'].astype(str).str.strip()
# Filtra os dados apenas dos campeões (posição 1)
campeoes = dados[dados['Pos.'].str.contains('^1\\D*$', na=False)].copy()
# Seleciona apenas as colunas relevantes
tabela_empates = campeoes[['Ano','Clubes','Empates']]
# Renomeia a coluna para clareza
tabela_empates.columns = ['Ano', 'Clubes', 'Empates no Titulo']


### Tabelas Rebaixamento
#Times Rebaixados
## Garante que a coluna 'Pos.' está limpa e convertida para número
dados['Pos.'] = dados['Pos.'].astype(str).str.extract('(\d+)')[0].astype(int)
## Filtra clubes com posição maior ou igual a 17 (rebaixados)
rebaixados = dados[dados['Pos.'] >= 17].copy()
## Seleciona colunas relevantes
tabela_rebaixados = rebaixados[['Ano', 'Clubes', 'Pos.']].sort_values(by=['Ano', 'Pos.']).reset_index(drop=True)
## Renomeia colunas para clareza
tabela_rebaixados.columns = ['Ano', 'Clube', 'Posição']


##Numero de derrotas no rebaixamento
# Garante que a coluna 'Pos.' está limpa e convertida para número
dados['Pos.'] = dados['Pos.'].astype(str).str.extract('(\d+)')[0].astype(int)
# Filtra os dados apenas dos rebaixados 
rebaixados = dados[dados['Pos.'] >= 17].copy()
# Seleciona apenas as colunas relevantes
tabela_derrotas_rebaixados = rebaixados[['Ano', 'Clubes', 'Derrotas']]
# Renomeia a coluna para clareza
tabela_derrotas_rebaixados.columns = ['Ano', 'Clube', 'Derrotas no Rebaixamento']

##Numero de vitorias no rebaixamento
# Garante que a coluna 'Pos.' está limpa e convertida para número
dados['Pos.'] = dados['Pos.'].astype(str).str.extract('(\d+)')[0].astype(int)
# Filtra os dados apenas dos rebaixados
rebaixados = dados[dados['Pos.'] >= 17].copy()
# Seleciona apenas as colunas relevantes
tabela_vitorias_rebaixamento = rebaixados[['Ano', 'Clubes', 'Vitorias']]
# Renomeia a coluna para clareza
tabela_vitorias_rebaixamento.columns = ['Ano', 'Clube', 'Vitorias no Rebaixamento']

##Numero de empates no rebaixamento
# Garante que a coluna 'Pos.' está limpa e convertida para número
dados['Pos.'] = dados['Pos.'].astype(str).str.extract('(\d+)')[0].astype(int)
# Filtra os dados apenas dos rebaixados
rebaixados = dados[dados['Pos.'] >= 17].copy()
# Seleciona apenas as colunas relevantes
tabela_empates_rebaixamento = rebaixados[['Ano', 'Clubes', 'Empates']]
# Renomeia a coluna para clareza
tabela_empates_rebaixamento.columns = ['Ano', 'Clube', 'Empates no Rebaixamento']

### Tabelas dados do campeonato
# Garante que o ano está como string ou inteiro, se necessário
dados['Ano'] = dados['Ano'].astype(int).astype(str)
# Agrupa por ano e calcula a média de gols feitos
media_gols_por_ano = dados.groupby('Ano')['Gols Feitos'].mean().reset_index()
# Renomeia as colunas para clareza
media_gols_por_ano.columns = ['Ano', 'Média de Gols Feitos']


#Numero de estrangeiros
dados['Ano'] = dados['Ano'].astype(int).astype(str)
estrangeiros_por_ano = dados.groupby('Ano')['Estrangeiros'].sum().reset_index()
estrangeiros_por_ano.columns = ['Ano', 'Numero de estrangeiros']

#Quantidade de jogadores por clube
dados['Ano'] = dados['Ano'].astype(int).astype(str)
jogadores_clube_ano = dados.groupby(['Ano','Clubes'])['Qtd_Jogadores'].sum().reset_index()
jogadores_clube_ano.columns = ['Ano', 'Clube', 'Quantidade de Jogadores']

##Média idade ano
# Converter para string e depois para float
dados['Idade_Media'] = dados['Idade_Media'].astype(str).str.replace(',', '.').astype(float)
# Garantir que 'Ano' esteja como string formatada corretamente
dados['Ano'] = dados['Ano'].astype(int).astype(str)
# Calcular a média da idade por ano
idade_media = dados.groupby('Ano')['Idade_Media'].mean().reset_index()
idade_media.columns = ['Ano', 'Media idade']

### Graficos
#Graficos Campeoes
# Contagem de títulos por clube
campeoes_contagem = campeoes['Clubes'].value_counts().reset_index()
campeoes_contagem.columns = ['Clube', 'Títulos']
# Adicionar coluna de cores com base no dicionário
campeoes_contagem['Cor'] = campeoes_contagem['Clube'].map(cores_times)
# Gráfico de barras
fig_campeoes = px.bar(campeoes_contagem, x='Clube', y='Títulos',
             title='Número de Títulos por Clube',
             labels={'Clube': 'Clube', 'Títulos': 'Número de Títulos'},
             color='Clube', 
             color_discrete_map=cores_times)


## grafico para visualizar a campanha
campanhas = campeoes[['Ano', 'Clubes', 'Vitorias', 'Empates', 'Derrotas']]
campanhas = campanhas.rename(columns={'Clubes': 'Clube'})

# Converte para formato "long" para usar no gráfico
campanhas_long = campanhas.melt(id_vars=['Ano', 'Clube'], 
                                 value_vars=['Vitorias', 'Empates', 'Derrotas'],
                                 var_name='Resultado', 
                                 value_name='Quantidade')

# Cria o gráfico
# Mapeamento de cores
cores_resultado = {
    'Vitorias': '#2ecc71',   # verde
    'Empates': '#f1c40f',    # amarelo
    'Derrotas': '#e74c3c'    # vermelho
}

# Pega os clubes únicos
clubes = campanhas_long['Clube'].unique()

# Gera um gráfico por clube
for clube in sorted(clubes):
    dados_clube = campanhas_long[campanhas_long['Clube'] == clube]
    fig_campanha = px.bar(
        dados_clube,
        x='Ano',
        y='Quantidade',
        color='Resultado',
        barmode='group',
        hover_data= ['Clube'],
        title=f'Campanha do {clube} nos Títulos Brasileiros',
        color_discrete_map=cores_resultado
    )
    #st.plotly_chart(fig, use_container_width=True)


#Graficos Rebaixados
# Junta os dados de rebaixamento com vitórias, empates e derrotas
tabela_rebaixamento_completa = tabela_rebaixados \
    .merge(tabela_vitorias_rebaixamento, on=['Ano', 'Clube']) \
    .merge(tabela_empates_rebaixamento, on=['Ano', 'Clube']) \
    .merge(tabela_derrotas_rebaixados, on=['Ano', 'Clube'])
# Cria uma nova coluna com a posição ordinal (ex: 17º)
tabela_rebaixamento_completa['Posição_Tabela'] = tabela_rebaixamento_completa['Posição'].astype(str) + 'º'


anos = tabela_rebaixamento_completa['Ano'].unique()

for ano in sorted(anos):
    dados_ano = tabela_rebaixamento_completa[tabela_rebaixamento_completa['Ano'] == ano]

    fig_rebaixamento = px.bar(
    dados_ano,
    x='Clube',
    y='Posição',
    color='Clube',
    title=f'Times Rebaixados - {ano}',
    labels={'Clube': 'Time', 'Posição': 'Posição Final'},
    text='Posição_Tabela',  # <- aqui usamos a versão com "º"
    color_discrete_map=cores_times,
    hover_data={
        'Vitorias no Rebaixamento': True,
        'Empates no Rebaixamento': True,
        'Derrotas no Rebaixamento': True,
        'Posição': False,
        'Clube': False
    },
    height=400
)

    fig_rebaixamento.update_layout(
        yaxis=dict(autorange='reversed'),  # Posição 17 no topo
        xaxis_tickangle=-45,
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    #st.plotly_chart(fig_rebaixamento, use_container_width=True)

# Grafico dados do campeonato
##Média de gols
fig_media_gols = px.line(
    media_gols_por_ano,
    x='Ano',
    y='Média de Gols Feitos',
    markers=True,
    title='Média de Gols Feitos',
    labels={'Ano': 'Ano', 'Média de Gols Feitos': 'Gols por Clube'},
    line_shape='linear',
    hover_data={'Ano': False}  # Esconde "Ano" no hover
)

# Ajuste de layout (opcional)
fig_media_gols.update_layout(
    xaxis_title='Ano',
    yaxis_title='Média de Gols Feitos',
    title_x=0.5,
    hovermode='x unified'
)

#st.plotly_chart(fig_media_gols, use_container_width=True)


##quantidade jogadores e estrangeiros por ano
#gerar total de jogadores por ano
jogadores_por_ano = jogadores_clube_ano.groupby('Ano')['Quantidade de Jogadores'].sum().reset_index()
# juntar com estrangeiros
comparativo_jogadores = jogadores_por_ano.merge(
    estrangeiros_por_ano,
    on='Ano'
)
#transformar para formato longo (necessário para gráfico comparativo)
comparativo_long = comparativo_jogadores.melt(
    id_vars='Ano',
    value_vars=['Quantidade de Jogadores', 'Numero de estrangeiros'],
    var_name='Tipo',
    value_name='Quantidade'
)
#gráfico de barras agrupadas
fig_numero_jogadores = px.bar(
    comparativo_long,
    x='Ano',
    y='Quantidade',
    color='Tipo',
    barmode='group',
    title='Total de Jogadores e Estrangeiros por Ano',
    labels={'Quantidade' : 'Número de Jogadores'},
    height=500
)
#st.plotly_chart(fig_numero_jogadores, use_container_width=True)


## Grafico media de idade 
fig_media_idade = px.line(
    idade_media,
    x='Ano',
    y='Media idade',
    markers=True,
    title='Média de Idade',
    labels={'Ano' : 'Ano', 'Media idade' : 'Média de Idade'},
    hover_data={'Ano' : False}
)

fig_media_idade.update_layout(
    xaxis_title='Ano',
    yaxis_title='Média de Idade',
    title_x=0.5,
    hovermode='x unified'
)

#st.plotly_chart(fig_media_idade, use_container_width=True)

## Visualizacao no streamlit
aba1, aba2, aba3 = st.tabs(['Campeoes', 'Raibaxamento', 'Dados do campeonato'])

# === ABA 1: CAMPEÕES ===
with aba1:
    st.subheader("Títulos por Clube")

    # Garante que a coluna 'Pos.' seja string para comparar com '1'
    dados_filtrados['Pos.'] = dados_filtrados['Pos.'].astype(str)

    # Filtra apenas os campeões com base nos dados filtrados
    campeoes_filtrados = dados_filtrados[dados_filtrados['Pos.'] == '1']

    if not campeoes_filtrados.empty:
        # Conta os títulos por clube
        campeoes_contagem = campeoes_filtrados['Clubes'].value_counts().reset_index()
        campeoes_contagem.columns = ['Clube', 'Títulos']
        campeoes_contagem['Cor'] = campeoes_contagem['Clube'].map(cores_times)

        # Gráfico de títulos
        fig_campeoes = px.bar(
            campeoes_contagem,
            x='Clube',
            y='Títulos',
            title='Número de Títulos por Clube (Filtrado)',
            color='Clube',
            color_discrete_map=cores_times
        )
        st.plotly_chart(fig_campeoes, use_container_width=True)

        st.divider()
        st.subheader("Campanhas dos Campeões")

        # Reconstrói campanhas com os dados filtrados
        campanhas = campeoes_filtrados[['Ano', 'Clubes', 'Vitorias', 'Empates', 'Derrotas']]
        #st.write("Campeões filtrados:", campeoes_filtrados)
        campanhas = campanhas.rename(columns={'Clubes': 'Clube'})

        campanhas_long = campanhas.melt(
            id_vars=['Ano', 'Clube'],
            value_vars=['Vitorias', 'Empates', 'Derrotas'],
            var_name='Resultado',
            value_name='Quantidade'
        )

        # Exibe em duas colunas alternadas
        col1, col2 = st.columns(2)

        for i, clube in enumerate(sorted(campanhas_long['Clube'].unique())):
            dados_clube = campanhas_long[campanhas_long['Clube'] == clube]
            fig_campanha = px.bar(
                dados_clube,
                x='Ano',
                y='Quantidade',
                color='Resultado',
                barmode='group',
                title=f'Campanha do {clube}',
                color_discrete_map=cores_resultado
            )
            if i % 2 == 0:
                col1.plotly_chart(fig_campanha, use_container_width=True)
            else:
                col2.plotly_chart(fig_campanha, use_container_width=True)

    else:
        st.warning("Nenhum clube campeão encontrado com os filtros selecionados.")



# === ABA 2: REBAIXAMENTO ===
with aba2:
    st.subheader("Resumo dos Rebaixamentos por Ano")

    # Cria duas colunas
    col1, col2 = st.columns(2)

    # Loop pelos anos rebaixados
    for i, ano in enumerate(sorted(anos)):
        dados_ano = tabela_rebaixamento_completa[tabela_rebaixamento_completa['Ano'] == ano]

        fig_rebaixamento = px.bar(
            dados_ano,
            x='Clube',
            y='Posição',
            color='Clube',
            title=f'Times Rebaixados - {ano}',
            labels={'Clube': ' ', 'Posição': ' '},
            text= 'Posição_Tabela',
            color_discrete_map=cores_times,
            hover_data={
                'Vitorias no Rebaixamento': True,
                'Empates no Rebaixamento': True,
                'Derrotas no Rebaixamento': True,
                'Posição': False,
                'Clube': False
            },
            height=400
        )

        fig_rebaixamento.update_layout(
            yaxis=dict(autorange='reversed'),
            xaxis_tickangle=-45,
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )
          
        fig_rebaixamento.update_yaxes(
            showgrid=False,        # esconde as linhas de grade horizontais
            showticklabels=False,  # esconde os números do eixo Y
            showline=False         # esconde a linha do eixo Y
        )


        # Alterna entre as duas colunas
        if i % 2 == 0:
            col1.plotly_chart(fig_rebaixamento, use_container_width=True)
        else:
            col2.plotly_chart(fig_rebaixamento, use_container_width=True)

# === ABA 3: DADOS DO CAMPEONATO ===
with aba3:
    st.subheader("Média de Gols e Idade por Ano")
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_media_gols, use_container_width=True)

    with col2:
        st.plotly_chart(fig_media_idade, use_container_width=True)

    st.divider()
    st.subheader("Quantidade de Jogadores por Clube")

    # Selectbox dentro da aba, não na sidebar
    anos_disponiveis = sorted(jogadores_clube_ano['Ano'].unique())
    ano_selecionado = st.selectbox(
        'Selecione o ano:',
        anos_disponiveis,
        key='ano_grafico_jogadores'  # evita conflito com outros filtros
    )

    dados_ano = jogadores_clube_ano[jogadores_clube_ano['Ano'] == ano_selecionado]

    fig = px.bar(
        dados_ano,
        x='Clube',
        y='Quantidade de Jogadores',
        color='Clube',
        text='Quantidade de Jogadores',
        title=f'Quantidade de Jogadores por Clube - {ano_selecionado}',
        color_discrete_map=cores_times,
        height=600
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)


#if clubes_selecionados and todos_anos:
    #dados_filtrados = dados[
        #(dados['Clubes'].isin(clubes_selecionados)) &
        #(dados['Ano'].isin(todos_anos))
    #]
    #dados_filtrados = dados_filtrados.reset_index(drop=True)
    #st.dataframe(dados_filtrados)
#else:
    ## Exibir o DataFrame completo se nenhum filtro for selecionado
    #st.dataframe(dados)
