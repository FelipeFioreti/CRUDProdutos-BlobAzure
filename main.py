
import streamlit as st
from Managers.productManager import ProductManager

st.set_page_config(page_title="Cadastrar Produto", layout="centered")
st.title("Cadastro de Produtos")

pm = ProductManager()

with st.form("post", clear_on_submit=True):
    name = st.text_input("Nome do Produto")
    price = st.number_input("Preço", min_value=0.0, format="%.2f")
    description = st.text_area("Descrição")
    image = st.file_uploader("Imagem do Produto", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Cadastrar Produto")

    if submitted:
        if name == "" or description == "" or image == "":
            st.warning("Preencha todos os campos e envie uma imagem.")
        else:
            resultado = pm.insert_product(name, price, description, image)
            if resultado:
                st.success("Produto cadastrado com sucesso!")
            else:
                st.error(f"Erro ao cadastrar.")
