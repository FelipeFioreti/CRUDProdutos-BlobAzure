import streamlit as st
from Managers.productManager import ProductManager

st.set_page_config(page_title="Atualizar Produto", layout="centered")
st.title("Atualização de Produtos")

pm = ProductManager()

with st.form("put", clear_on_submit=True):
    id = st.text_input("ID do Produto")
    name = st.text_input("Nome do Produto")
    price = st.number_input("Preço", min_value=0.0, format="%.2f")
    description = st.text_area("Descrição")
    image = st.file_uploader("Imagem do Produto", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Cadastrar Produto")

    if submitted:
        if name == "" or description == "" or image == "":
            st.warning("Preencha todos os campos e envie uma imagem.")
        else:
            resultado = pm.update_product(id,name, price, description, image)
            if resultado:
                st.success("Produto atualizado com sucesso!")
            else:
                st.error(f"Erro ao atualizar.")

