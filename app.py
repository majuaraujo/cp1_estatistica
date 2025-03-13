import streamlit as st
from PIL import Image
import os
import pandas as pd
import numpy as np
import plotly.express as px
import scipy.stats as stats

# Definir o caminho da imagem
image_path = os.path.join("assets", "maju.jpg")
image = Image.open(image_path)

# Configuração do layout
st.set_page_config(page_title="Dashboard Climático", layout="wide")

st.sidebar.title("Menu de Navegação")
st.sidebar.page_link("pages/1_Home.py", label="🏠 Home")
st.sidebar.page_link("pages/2_Formacao_Experiencias.py", label="🎓 Formação e Experiências")
st.sidebar.page_link("pages/3_Skills.py", label="🛠 Skills")
st.sidebar.page_link("pages/4_Analise_Dados.py", label="📊 Análise de Dados")

st.title("Dashboard de Variação Climática")
st.image(image, width=150)
st.write("Bem-vindo ao dashboard de análise climática baseado em 10 anos de dados.")

st.write("Selecione uma aba no menu lateral para navegar entre as seções do dashboard.")

# Código para cada aba
if "pages/1_Home.py" in st.session_state:
    st.header("🏠 Home")
    st.image(image, width=150)
    st.write("## Maria Julia")
    st.write("Sou Maria Julia, tenho 22 anos e quero ingressar na área de tecnologia porque gosto dos desafios.")
    st.write("Atualmente, estou desenvolvendo habilidades em ciência de dados e programação para melhorar minha capacidade analítica e resolver problemas do mundo real.")

if "pages/2_Formacao_Experiencias.py" in st.session_state:
    st.header("🎓 Formação e Experiências")
    st.image(image, width=150)
    st.write("## Formação Acadêmica")
    st.write("Sou formada em Análise de Sistemas.")
    st.write("## Experiência Profissional")
    st.write("Atuo como bancária no setor de crédito imobiliário há 7 anos, adquirindo experiência em análise financeira e sistemas de gestão de crédito.")

if "pages/3_Skills.py" in st.session_state:
    st.header("🛠 Skills")
    st.image(image, width=150)
    st.write("## Habilidades Técnicas")
    st.write("- Linguagens de Programação: Java, Python, JavaScript, SQL")
    st.write("- Banco de Dados e Análise de Dados")
    st.write("- Desenvolvimento Web e APIs")
    st.write("- Visualização de Dados")
    st.write("## Idiomas")
    st.write("- Inglês: Fluente")
    st.write("- Espanhol: Intermediário")
    st.write("- Francês: Intermediário")
