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
st.write(df_capital["TEMP. MÉDIA MENSAL"].describe())

# 📌 Entendendo o Problema
st.header("📌 Entendendo o Problema")

st.write("A partir dos dados, podemos responder às seguintes perguntas:")

# Pergunta 1: Tendência de Aumento de Temperatura
st.subheader("1️⃣ A temperatura média está aumentando ao longo dos anos?")
st.write("""
🔍 Para responder a essa questão, utilizamos um **gráfico de tendência** que mostra a evolução da temperatura média ao longo do tempo.
Se a curva apresentar um crescimento constante, há evidências de aquecimento.
""")

# 📈 Gráfico de Tendência da Temperatura ao longo do tempo
fig_tendencia = px.line(df_capital, x="DATA MEDIÇÃO", y="TEMP. MÉDIA MENSAL",
                        title=f"Tendência da Temperatura Média - {capital_selecionada}",
                        labels={"TEMP. MÉDIA MENSAL": "Temperatura Média (°C)", "DATA MEDIÇÃO": "Ano"},
                        markers=True)

st.plotly_chart(fig_tendencia)

# Pergunta 2: Variação da Temperatura
st.subheader("2️⃣ Qual capital apresenta a maior variação de temperatura?")
st.write("""
🔍 Para essa análise, utilizamos medidas estatísticas como **desvio padrão** e **variância**.
Quanto maior o desvio padrão, maior a variação da temperatura ao longo do tempo.
""")

# Estatísticas de variação (Desvio padrão e Variância)
variability_stats = df.groupby("CAPITAL")["TEMP. MÉDIA MENSAL"].agg(["var", "std"])
st.write(variability_stats)

# Pergunta 3: Correlação entre temperatura e tempo
st.subheader("3️⃣ Existe correlação entre o aumento da temperatura e o tempo?")
st.write("""
🔍 Utilizamos o **coeficiente de correlação de Pearson** para verificar a relação entre o tempo e a temperatura.
Se o valor da correlação for positivo e próximo de 1, significa que a temperatura está aumentando com o passar dos anos.
""")

# Calcular a correlação para a capital selecionada
correlation, p_value = stats.pearsonr(df_capital["DATA MEDIÇÃO"].dt.year, df_capital["TEMP. MÉDIA MENSAL"].dropna())
st.write(f"**Correlação para {capital_selecionada}:** {correlation:.2f} (p-valor: {p_value:.5f})")

# 📊 Histograma Interativo com Distribuição Normal
st.subheader("📌 Distribuição das Temperaturas")

st.write("""
🔍 O histograma a seguir mostra como as temperaturas estão distribuídas ao longo dos meses. 
Sobre ele, aplicamos uma **curva da Distribuição Normal** para entender a dispersão dos valores.
""")

mu, sigma = df_capital["TEMP. MÉDIA MENSAL"].mean(), df_capital["TEMP. MÉDIA MENSAL"].std()
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
y = stats.norm.pdf(x, mu, sigma)

fig_hist = px.histogram(df_capital, x="TEMP. MÉDIA MENSAL", nbins=15, opacity=0.7, histnorm='probability density',
                        title=f"Distribuição das Temperaturas - {capital_selecionada}")

fig_hist.add_trace(go.Scatter(x=x, y=y, mode='lines', name="Distribuição Normal", line=dict(color="red")))

st.plotly_chart(fig_hist)

# 🚀 Distribuição de Poisson para eventos extremos
st.subheader("📌 Eventos de Temperaturas Extremas")

st.write("""
🔍 Para identificar a frequência de **temperaturas extremas** (valores acima do percentil 90%), 
utilizamos a **Distribuição de Poisson**, que modela a ocorrência desses eventos raros.
""")

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

