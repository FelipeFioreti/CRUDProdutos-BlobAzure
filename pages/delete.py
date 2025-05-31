import streamlit as st
from Managers.productManager import ProductManager

st.set_page_config(page_title="Remover Produtos", layout="centered")
st.title("Remoção de Produto")

pm = ProductManager()

id = st.text_input("Id do Produto")

if st.button("Remover Produto"):
    resultado = pm.delete_product(id)
    if resultado:
        st.success("Produto removido com sucesso!")
    else:
        st.error(f"Erro ao remover o produto com ID {id}.")
