import streamlit as st
from PIL import Image
import os

# Caminho da imagem
image_path = os.path.join("assets", "maju.jpg")
image = Image.open(image_path)

# Exibir a imagem com largura de 150 pixels
st.image(image, width=150)

# Título da página
st.title("Home")

# Introdução Pessoal
st.write("""
## Olá, sou Maria Julia! 👋
Tenho 22 anos e estou em transição de carreira para a área de tecnologia. 
Sempre gostei de desafios e resolver problemas, e encontrei na tecnologia 
uma forma de combinar criatividade e lógica para desenvolver soluções inovadoras.
""")

# Objetivo Profissional
st.write("""
### Objetivo Profissional 🎯
Quero ingressar no setor de tecnologia para aplicar meus conhecimentos em 
desenvolvimento de software e análise de dados. Busco oportunidades que 
me permitam crescer e contribuir para projetos inovadores.
""")
