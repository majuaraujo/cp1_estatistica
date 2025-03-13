import streamlit as st
from PIL import Image
import os

# Caminho da imagem
image_path = os.path.join("assets", "maju.jpg")
image = Image.open(image_path)

# Exibir a imagem com largura de 150 pixels
st.image(image, width=150)

# Título da página
st.title("Skills")

# Habilidades Técnicas
st.write("""
## 🖥️ Habilidades Técnicas
- **Linguagens de Programação**: Java, Python, JavaScript, SQL
- **Banco de Dados**: MySQL, PostgreSQL
- **Frameworks e Ferramentas**: Streamlit, Pandas, NumPy, Scipy, Plotly, OpenPyXL, Plotnine
""")

# Idiomas
st.write("""
## 🌍 Idiomas
- **Inglês**: Fluente
- **Espanhol**: Intermediário
- **Francês**: Intermediário
""")
