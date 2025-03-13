import streamlit as st
from PIL import Image
import os

# Caminho da imagem
image_path = os.path.join("assets", "maju.jpg")
image = Image.open(image_path)

# Exibir a imagem com largura de 150 pixels
st.image(image, width=150)

# Título da página
st.title("Formação e Experiências")

# Formação Acadêmica
st.write("""
## 🎓 Formação Acadêmica
Sou formada em **Análise de Sistemas**, onde desenvolvi habilidades em desenvolvimento de software, 
bancos de dados, redes e engenharia de software.
""")

# Experiência Profissional
st.write("""
## 💼 Experiência Profissional
Atuo há **7 anos no setor bancário**, especificamente na área de **crédito imobiliário**. 
Durante esse período, adquiri conhecimentos sólidos sobre análise de crédito, gestão de processos e atendimento ao cliente.
""")


