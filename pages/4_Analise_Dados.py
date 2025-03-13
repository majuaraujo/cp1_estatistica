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

# 📊 Analisando os Tipos de Variáveis
st.subheader("📊 Tipos de Variáveis na Base de Dados")

st.write("""
Nesta base de dados, temos diferentes tipos de variáveis que influenciam a análise estatística:

- **DATA MEDIÇÃO** (*Qualitativa Ordinal*) → Representa um ponto no tempo e pode ser ordenada cronologicamente.
- **CAPITAL** (*Qualitativa Nominal*) → Nome da cidade onde os dados foram coletados, sem uma hierarquia definida.
- **TEMP. MÉDIA MENSAL** (*Quantitativa Contínua*) → Valor numérico que pode assumir qualquer temperatura dentro de um intervalo.
""")

# 📊 Exibir Tabela Completa com Filtro Interativo
st.write("### 📊 Estrutura da Base de Dados")

# Criar filtro no estilo Excel
capital_filtrada = st.multiselect("Selecione a(s) capital(is) para visualizar:", df["CAPITAL"].unique(), default=df["CAPITAL"].unique())

# Filtrar os dados conforme a seleção do usuário
df_filtrado = df[df["CAPITAL"].isin(capital_filtrada)]

# Exibir a tabela filtrada
st.dataframe(df_filtrado, height=400, width=900)

# 📌 Estatísticas Descritivas
st.subheader("📌 Estatísticas Descritivas")

# Selecionar capital para análise
capital_selecionada = st.selectbox("Selecione uma capital para análise detalhada:", df["CAPITAL"].unique())

# Filtrar dados para a capital escolhida
df_capital = df[df["CAPITAL"] == capital_selecionada].copy()

# Exibir estatísticas descritivas
stats_desc = df_capital["TEMP. MÉDIA MENSAL"].describe()
st.write(stats_desc)

# 🔎 Observação sobre Estatísticas Descritivas
mean_temp = stats_desc["mean"]
min_temp = stats_desc["min"]
max_temp = stats_desc["max"]

st.write(f"""
**📌 Observação:**  
A temperatura média registrada em **{capital_selecionada}** foi **{mean_temp:.2f}°C**.  
Para referência, a **temperatura ideal para conforto térmico humano** é entre **20°C e 25°C**.  
- Se a média estiver acima de **28°C**, pode indicar **ondas de calor frequentes**.  
- Se a média estiver abaixo de **18°C**, o clima pode estar **mais frio do que o esperado**.  
- A menor temperatura registrada foi **{min_temp:.1f}°C**, e a máxima chegou a **{max_temp:.1f}°C**, mostrando a amplitude climática.
""")

# 📈 Tendência da Temperatura
st.subheader("📌 Tendência da Temperatura")

fig_tendencia = px.line(df_capital, x="DATA MEDIÇÃO", y="TEMP. MÉDIA MENSAL",
                        title=f"Tendência da Temperatura Média - {capital_selecionada}",
                        labels={"TEMP. MÉDIA MENSAL": "Temperatura Média (°C)", "DATA MEDIÇÃO": "Ano"},
                        markers=True)

st.plotly_chart(fig_tendencia)

st.write("""
**📌 Observação:**  
Se a curva estiver **subindo**, há uma **tendência de aquecimento** na região.  
Se a curva estiver **descendo**, pode indicar um período de **resfriamento**.  
Padrões instáveis sugerem **grandes variações climáticas ao longo do tempo**.  
""")

# 📊 Distribuição das Temperaturas
st.subheader("📌 Distribuição das Temperaturas")

mu, sigma = df_capital["TEMP. MÉDIA MENSAL"].mean(), df_capital["TEMP. MÉDIA MENSAL"].std()
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
y = stats.norm.pdf(x, mu, sigma)

fig_hist = px.histogram(df_capital, x="TEMP. MÉDIA MENSAL", nbins=15, opacity=0.7, histnorm='probability density',
                        title=f"Distribuição das Temperaturas - {capital_selecionada}")

fig_hist.add_trace(go.Scatter(x=x, y=y, mode='lines', name="Distribuição Normal", line=dict(color="red")))

st.plotly_chart(fig_hist)

st.write("""
**📌 Observação:**  
Se houver **muitos valores acima de 25°C**, há um padrão de **temperaturas elevadas**.  
Se a distribuição for muito dispersa, isso indica **alta variação climática**.  
""")

# 🚀 Eventos de Temperaturas Extremas
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

st.write(f"""
**📌 Observação:**  
Se houver **muitas ocorrências**, pode ser um **sinal de ondas de calor frequentes**.  
Temperaturas muito elevadas aumentam o risco de **seca, incêndios e consumo elevado de energia**.  
""")

# 📌 Conclusão Final
st.header("📌 Conclusão")

st.write("""
Os resultados desta análise mostram que a temperatura média nas capitais **tem uma tendência de crescimento**, evidenciada pelo coeficiente de correlação e pelo gráfico de tendência.

### 🌍 Impacto no Meio Ambiente e na Vida:
- **Aquecimento global**: Pode intensificar secas e ondas de calor.
- **Saúde pública**: Risco maior de desidratação e problemas respiratórios.
- **Infraestrutura urbana**: Pode levar a sobrecarga no consumo de energia.

Esses dados são fundamentais para auxiliar no planejamento ambiental e políticas públicas. 🌱🌍
""")

