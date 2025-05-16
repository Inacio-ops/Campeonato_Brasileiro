import streamlit as st
import pandas as pd
import plotly.express as px
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index = False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!', icon="✅")
    time.sleep(5)
    sucesso.empty()


st.title('Dados Brutos')

arquivo = 'C:/Users/Gabriel Inacio/Downloads/Tabela_Clubes.csv'
dados = pd.read_csv(arquivo)
dados = dados.loc[:, ~dados.columns.str.contains('^Unnamed')]

dados[['Gols Feitos', 'Gols Sofridos']] = dados['GolsF/S'].str.split(':', expand=True)
dados['Gols Feitos'] = dados['Gols Feitos'].astype(int)
dados['Gols Sofridos'] = dados['Gols Sofridos'].astype(int)

dados.insert(6, 'Gols Feitos', dados.pop('Gols Feitos'))  # Insere a coluna "Gols Feitos" na posição 7
dados.insert(7, 'Gols Sofridos', dados.pop('Gols Sofridos'))  # Insere a coluna "Gols Sofridos" na posição 8

dados = dados.drop(columns=['GolsF/S'])

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Clube'):
    clubes = st.sidebar.multiselect('Selecione os clubes', dados['Clubes'].unique(), default=[])
with st.sidebar.expander('Ano'):
    ano = st.sidebar.slider('Selecione o ano', 2008, 2017, (2008,2008))


query = '''
Clubes in @clubes and \
@ano[0] <= Ano <= @ano[1]
'''

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]


st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas')

st.markdown('Escreva um nome para o arquivo')
coluna1, coluna2 = st.columns(2)

with coluna1:
    nome_arquivo = st.text_input('', label_visibility= 'collapsed', value='dados')
    nome_arquivo += '.csv'

with coluna2:
    st.download_button('Fazer o download da tabela em csv', data = converte_csv(dados_filtrados), file_name = nome_arquivo, mime = 'text/csv', on_click = mensagem_sucesso)
