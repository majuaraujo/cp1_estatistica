import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stats
import os

# Carregar os dados
file_path = os.path.join("data", "BASE_DADOS_10ANOS.xlsx")
df = pd.read_excel(file_path)

# Título da página
st.title("📊 Análise de Dados: Temperaturas Médias (2015 - 2025)")

# 📌 Entendendo os Dados
st.header("📌 Entendendo os Dados")
st.write("""
Os dados utilizados nesta análise foram obtidos do **Instituto Nacional de Meteorologia (INMET)** e representam 
a temperatura média mensal de três capitais brasileiras no período de **2015 a 2025**. 

Cada linha da base de dados contém:
- **Data da Medição**: Último dia do mês em que a temperatura foi registrada.
- **Capital**: Cidade onde foi realizada a medição.
- **Temperatura Média Mensal**: Valor médio da temperatura do mês.

A análise a seguir busca identificar tendências de aumento de temperatura e possíveis impactos climáticos.
""")

# 📊 Exibir Tabela Completa com Filtro Interativo
st.write("### 📊 Estrutura da Base de Dados")
capital_filtrada = st.multiselect("Selecione a(s) capital(is) para visualizar:", df["CAPITAL"].unique(), default=df["CAPITAL"].unique())
df_filtrado = df[df["CAPITAL"].isin(capital_filtrada)]
st.dataframe(df_filtrado, height=400, width=900)

# 📌 Estatísticas Descritivas
st.subheader("📌 Estatísticas Descritivas")
capital_selecionada = st.selectbox("Selecione uma capital para análise detalhada:", df["CAPITAL"].unique())
df_capital = df[df["CAPITAL"] == capital_selecionada].copy()
st.write(df_capital["TEMP. MÉDIA MENSAL"].describe())
st.info("""
📌 **Interpretação:**
- A média indica a temperatura média típica.
- A mediana é menos influenciada por valores extremos.
- O desvio padrão revela variabilidade climática.
- Valores extremos indicam eventos climáticos excepcionais.

**Pergunta para reflexão:**
- Qual estatística descritiva melhor descreve a temperatura média mensal?

**Justificativa:**
A mediana é ideal pois é menos sensível a valores extremos, refletindo melhor a tendência central em dados ambientais.
""")

# 📈 Tendência da Temperatura
st.subheader("📌 Tendência da Temperatura")
fig_tendencia = px.line(df_capital, x="DATA MEDIÇÃO", y="TEMP. MÉDIA MENSAL", markers=True,
                        title=f"Tendência da Temperatura Média - {capital_selecionada}",
                        labels={"TEMP. MÉDIA MENSAL": "Temperatura Média (°C)", "DATA MEDIÇÃO": "Ano"})
st.plotly_chart(fig_tendencia)
st.info("""
📌 **Interpretação:**
- Observe se existe uma tendência crescente, indicando aquecimento, ou decrescente, indicando resfriamento.
- Avalie se há padrões sazonais ou variações consistentes ao longo dos anos.

**Pergunta para reflexão:**
- Existe uma tendência clara de aumento das temperaturas ao longo do período analisado?

**Justificativa:**
- Identificar tendências de aquecimento é essencial para planejar ações mitigatórias frente às mudanças climáticas.
""")

# 🚀 Análise Binomial
st.subheader("📌 Análise Binomial")
thresh_high = st.slider("Defina o limiar para temperaturas altas (°C):",
                        float(df_capital["TEMP. MÉDIA MENSAL"].min()),
                        float(df_capital["TEMP. MÉDIA MENSAL"].max()),
                        float(df_capital["TEMP. MÉDIA MENSAL"].quantile(0.75)))

total_meses = len(df_capital)
meses_altas = sum(df_capital["TEMP. MÉDIA MENSAL"] > thresh_high)
p = meses_altas / total_meses

x_binomial = np.arange(0, total_meses + 1)
y_binomial = stats.binom.pmf(x_binomial, total_meses, p)

fig_binomial = go.Figure()
fig_binomial.add_trace(go.Bar(x=x_binomial, y=y_binomial, name="Distribuição Binomial", marker=dict(color="green")))
fig_binomial.update_layout(title="Distribuição Binomial de Meses com Temperaturas Altas",
                           xaxis_title="Número de Meses com Temperaturas Altas",
                           yaxis_title="Probabilidade",
                           showlegend=True)
st.plotly_chart(fig_binomial)
st.info("""
📌 **Interpretação:**
- Avalie a frequência provável dos meses mais quentes.

**Pergunta para reflexão:**
- O risco de meses com temperaturas elevadas é significativo para esta capital?

**Justificativa:**
- Compreender a frequência desses eventos permite avaliar impactos na saúde pública e ambiental, direcionando políticas públicas.
""")

# 🚀 Análise de Poisson
st.subheader("📌 Análise de Poisson")
thresh_extreme = st.slider("Defina o limiar para temperaturas extremas (°C):",
                           float(df_capital["TEMP. MÉDIA MENSAL"].min()),
                           float(df_capital["TEMP. MÉDIA MENSAL"].max()),
                           float(df_capital["TEMP. MÉDIA MENSAL"].quantile(0.90)))

eventos_extremos = sum(df_capital["TEMP. MÉDIA MENSAL"] > thresh_extreme)
taxa_eventos = eventos_extremos / total_meses

x_poisson = np.arange(0, eventos_extremos + 5)
y_poisson = stats.poisson.pmf(x_poisson, taxa_eventos * total_meses)

fig_poisson = go.Figure()
fig_poisson.add_trace(go.Bar(x=x_poisson, y=y_poisson, name="Distribuição de Poisson", marker=dict(color="blue")))
st.plotly_chart(fig_poisson)
st.info("""
📌 **Interpretação:**
- A frequência esperada de eventos extremos ajuda a avaliar o risco climático.

**Pergunta para reflexão:**
- Eventos extremos são frequentes o suficiente para justificar ações preventivas imediatas?

**Justificativa:**
- Se houver aumento na frequência, é preciso considerar estratégias de adaptação climática.
""")

# 📌 Tabela de Variáveis
st.subheader("📌 Classificação das Variáveis")
st.table(pd.DataFrame({
    "Variável": ["Data da Medição", "Capital", "Temperatura Média Mensal"],
    "Tipo": ["Quantitativa - Temporal", "Qualitativa Nominal", "Quantitativa Contínua"]
}))

# 📌 Conclusão
st.header("📌 Conclusão da Análise")
st.write("""
Os dados indicam possíveis tendências de aquecimento ao longo do período analisado, com um aumento na frequência de meses e eventos extremos de altas temperaturas. Tais resultados reforçam a necessidade de políticas públicas voltadas para mitigação e adaptação às mudanças climáticas nas capitais estudadas.
""")
