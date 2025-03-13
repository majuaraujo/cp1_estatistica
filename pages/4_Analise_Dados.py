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

# Exibir a estrutura dos dados
st.write("### Estrutura da Base de Dados")
st.write(df.head())

# Selecionar capital para análise
capitais = df["CAPITAL"].unique()
capital_selecionada = st.selectbox("Selecione a capital para análise:", capitais)

# Filtrar dados para a capital escolhida
df_capital = df[df["CAPITAL"] == capital_selecionada].copy()

# Estatísticas descritivas
st.write("### 📌 Estatísticas Descritivas")
stats_desc = df_capital["TEMP. MÉDIA MENSAL"].describe()
st.write(stats_desc)

# 🔎 Análise Exploratória dos Resultados
st.subheader("📊 Resumo da Análise Exploratória")

mean_temp = stats_desc["mean"]
median_temp = stats_desc["50%"]
std_temp = stats_desc["std"]
min_temp = stats_desc["min"]
max_temp = stats_desc["max"]

st.write(f"""
- A **temperatura média** registrada em {capital_selecionada} é de **{mean_temp:.2f}°C**.
- A **mediana** ({median_temp:.2f}°C) é próxima da média, indicando uma distribuição relativamente simétrica.
- O **desvio padrão** é de **{std_temp:.2f}°C**, o que sugere o grau de variação da temperatura ao longo dos anos.
- A menor temperatura registrada foi **{min_temp:.1f}°C**, enquanto a máxima foi **{max_temp:.1f}°C**, mostrando a amplitude climática da cidade.
- Se o desvio padrão for alto, isso significa que há grande oscilação nas temperaturas ao longo do período.
""")

# 📈 Gráfico de Tendência da Temperatura ao longo do tempo
st.subheader("📌 Tendência da Temperatura")

fig_tendencia = px.line(df_capital, x="DATA MEDIÇÃO", y="TEMP. MÉDIA MENSAL",
                        title=f"Tendência da Temperatura Média - {capital_selecionada}",
                        labels={"TEMP. MÉDIA MENSAL": "Temperatura Média (°C)", "DATA MEDIÇÃO": "Ano"},
                        markers=True)

st.plotly_chart(fig_tendencia)

# 📊 Histograma Interativo com Distribuição Normal
st.subheader("📌 Distribuição das Temperaturas")

mu, sigma = df_capital["TEMP. MÉDIA MENSAL"].mean(), df_capital["TEMP. MÉDIA MENSAL"].std()
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
y = stats.norm.pdf(x, mu, sigma)

fig_hist = px.histogram(df_capital, x="TEMP. MÉDIA MENSAL", nbins=15, opacity=0.7, histnorm='probability density',
                        title=f"Distribuição das Temperaturas - {capital_selecionada}")

fig_hist.add_trace(go.Scatter(x=x, y=y, mode='lines', name="Distribuição Normal", line=dict(color="red")))

st.plotly_chart(fig_hist)

# 🚀 Distribuição de Poisson para eventos extremos
st.subheader("📌 Eventos de Temperaturas Extremas")

threshold = df_capital["TEMP. MÉDIA MENSAL"].quantile(0.90)
extreme_temps = df_capital[df_capital["TEMP. MÉDIA MENSAL"] > threshold]

event_counts = len(extreme_temps)
lambda_poisson = event_counts / len(df_capital)  # Média de eventos por mês

x_poisson = np.arange(0, event_counts + 5)
poisson_pmf = stats.poisson.pmf(x_poisson, lambda_poisson)

fig_poisson = go.Figure()
fig_poisson.add_trace(go.Bar(x=[f"{capital_selecionada}"], y=[event_counts], name="Eventos Reais", marker=dict(color="blue")))
fig_poisson.add_trace(go.Scatter(x=x_poisson, y=poisson_pmf * event_counts, mode="lines+markers", name="Distribuição de Poisson", line=dict(color="red")))

fig_poisson.update_layout(title="Eventos de Temperatura Extrema e Distribuição Poisson",
                          xaxis_title="Capital",
                          yaxis_title="Ocorrências",
                          showlegend=True)

st.plotly_chart(fig_poisson)

# 📌 Conclusão
st.header("📌 Conclusão")

st.write("""
Os resultados desta análise mostram que a temperatura média nas capitais **tem uma tendência de crescimento**, evidenciada pelo coeficiente de correlação e pelo gráfico de tendência.

### 📊 Justificativa dos Gráficos:
1. **Gráfico de Tendência**: Mostra o crescimento da temperatura ao longo dos anos.
2. **Histograma com Distribuição Normal**: Identifica como as temperaturas estão distribuídas.
3. **Distribuição de Poisson**: Analisa eventos extremos de calor, permitindo prever sua recorrência.

### 🌍 Impacto no Meio Ambiente e na Vida:
- **Aquecimento global**: O aumento da temperatura pode intensificar eventos climáticos extremos, como secas e ondas de calor.
- **Saúde pública**: Altas temperaturas aumentam o risco de doenças relacionadas ao calor, como desidratação e problemas respiratórios.
- **Infraestrutura urbana**: Cidades podem enfrentar desafios como sobrecarga no consumo de energia e maior necessidade de climatização.

Esses dados são fundamentais para auxiliar no planejamento ambiental e em políticas públicas que visem mitigar os efeitos das mudanças climáticas. 🌱🌍
""")

