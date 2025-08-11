import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv(
    "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
)

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

def filtro_multiselect(label, coluna):
    opcoes = sorted(df[coluna].unique())
    return st.sidebar.multiselect(label, opcoes, default=opcoes)

anos_selecionados = filtro_multiselect("Ano", "ano")
senioridades_selecionadas = filtro_multiselect("Senioridade", "senioridade")
contratos_selecionados = filtro_multiselect("Tipo de Contrato", "contrato")
tamanhos_selecionados = filtro_multiselect("Tamanho da Empresa", "tamanho_empresa")

# --- Filtragem do DataFrame ---
df_filtrado = df.query(
    "ano in @anos_selecionados and "
    "senioridade in @senioridades_selecionadas and "
    "contrato in @contratos_selecionados and "
    "tamanho_empresa in @tamanhos_selecionados"
)

# --- Conteúdo Principal ---
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

# --- KPIs ---
st.subheader("Métricas gerais (Salário anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = len(df_filtrado)
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_medio = salario_maximo = total_registros = 0
    cargo_mais_frequente = ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

# --- Função para renderizar gráficos ---
def render_grafico(fig, mensagem_alerta):
    if not df_filtrado.empty:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(mensagem_alerta)

# --- Gráficos ---
st.subheader("Gráficos")
col_graf1, col_graf2 = st.columns(2)

# Top 10 cargos
top_cargos = (
    df_filtrado.groupby("cargo")["usd"]
    .mean()
    .nlargest(10)
    .iloc[::-1]
    .reset_index()
)
grafico_cargos = px.bar(
    top_cargos,
    x="usd",
    y="cargo",
    orientation="h",
    title="Top 10 cargos por salário médio",
    labels={"usd": "Média salarial anual (USD)", "cargo": ""}
)
grafico_cargos.update_layout(title_x=0.1, yaxis={"categoryorder": "total ascending"})
with col_graf1:
    render_grafico(grafico_cargos, "Nenhum dado para exibir no gráfico de cargos.")

# Histograma salários
grafico_hist = px.histogram(
    df_filtrado,
    x="usd",
    nbins=30,
    title="Distribuição de salários anuais",
    labels={"usd": "Faixa salarial (USD)", "count": ""}
)
grafico_hist.update_layout(title_x=0.1)
with col_graf2:
    render_grafico(grafico_hist, "Nenhum dado para exibir no gráfico de distribuição.")

# Gráficos 2ª linha
col_graf3, col_graf4 = st.columns(2)

# Trabalho remoto
remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
grafico_remoto = px.pie(
    remoto_contagem,
    names="tipo_trabalho",
    values="quantidade",
    title="Proporção dos tipos de trabalho",
    hole=0.5
)
grafico_remoto.update_traces(textinfo="percent+label")
grafico_remoto.update_layout(title_x=0.1)
with col_graf3:
    render_grafico(grafico_remoto, "Nenhum dado para exibir no gráfico dos tipos de trabalho.")

# Mapa Cientistas de Dados
df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
media_ds_pais = df_ds.groupby("residencia_iso3")["usd"].mean().reset_index()
grafico_paises = px.choropleth(
    media_ds_pais,
    locations="residencia_iso3",
    color="usd",
    color_continuous_scale="Viridis",
    title="Salário médio de Cientista de Dados por país",
    labels={"usd": "Salário médio (USD)", "residencia_iso3": "País"}
)
grafico_paises.update_layout(title_x=0.1)
with col_graf4:
    render_grafico(grafico_paises, "Nenhum dado para exibir no gráfico de países.")

# --- Tabela ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
