import streamlit as st
from Managers.productManager import ProductManager

st.set_page_config(page_title="Visualizar Produtos", layout="centered")
st.title("Visualização de Produtos")

pm = ProductManager()

def list_products_screen():
    products = pm.list_products()
    if products:

        cards_por_linha = 3
        cols = st.columns(cards_por_linha)

        for i, product in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.write(f"**Nome:** {product[1]}")
                st.write(f"**Descrição:** {product[2]}")
                st.write(f"**Preço:** R$ {product[3]:.2f}")
                if product[4]:
                    html_image = f'<img src="{product[4]} " width="200" height="200" alt="Imagem do Produto">'
                    st.markdown(html_image, unsafe_allow_html=True)
                st.markdown("---")
            if( i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
                cols = st.columns(cards_por_linha)
    else:
        st.write("Nenhum produto cadastrado.")

list_products_screen()
st.markdown("---")
