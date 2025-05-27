import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

BlobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
BlobContainerName = os.getenv("BLOB_CONTAINER_NAME")
BlobAccountName = os.getenv("BLOB_ACCOUNT_NAME")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

st.title("Cadastro de Produtos")

#Register form product
product_name = st.text_input("Nome do Produto")
product_price = st.number_input("Preço do Produto", min_value= 0.0, format="%.2f")
product_description = st.text_area("Descrição do Produto")
product_image = st.file_uploader("Imagem do Produto", type=["jpg","png", "jpeg"])

#Save image on blob storage
def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
    container_client = blob_service_client.get_container_client(BlobContainerName)
    blob_name = str(uuid.uuid4()) + file.name
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overwrite = True)
    image_url = f"https://{BlobAccountName}.blob.core.windows.net/{BlobContainerName}/{blob_name}"
    return image_url

def insert_product(product_name, product_price, product_description, product_image):
    try:
        image_url = upload_blob(product_image)
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Produtos (Nome, Descricao, Preco, Imagem_URL )VALUES ('{product_name}', '{product_description}', '{product_price}', '{image_url}')")  
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir produto: {e}")
        return False

def list_products():
    try:
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos")
        products = cursor.fetchall()
        conn.close()
        return products
    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return []

def list_products_screen():
    products = list_products()
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

def update_product():
    try:
        if product_id_update is None or product_id_update == "":
            st.error("Por favor, informe o ID do produto a ser atualizado.")
            return

        if product_image_update is None:
            st.error("Por favor, faça o upload de uma nova imagem do produto.")
            return
        
        image_url_update = upload_blob(product_image_update) 
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE Produtos SET Nome = '{product_name_update}', Descricao = '{product_description_update}', Preco = {product_price_update}, Imagem_URL = '{image_url_update}' WHERE ID = {product_id_update}")
        conn.commit()
        conn.close()
        st.success("Produto atualizado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao atualizar produto: {e}")

if st.button("Salvar Produto"):
    insert_product(product_name,product_price,product_description,product_image)
    return_message = "Produto salvo com sucesso"

st.header("Produtos Cadastrados")

if st.button("Listar Produtos"):
    list_products_screen()
    return_message = "Produtos listados com sucesso"

st.header("Atualizar Produto")

# Update form product

product_id_update = st.text_input("ID do Produto a ser atualizado")
product_name_update = st.text_input("Novo Nome do Produto")
product_price_update = st.number_input("Novo Preço do Produto", min_value=0.0, format="%.2f")
product_description_update = st.text_area("Nova Descrição do Produto")
product_image_update = st.file_uploader("Nova Imagem do Produto", type=["jpg","png", "jpeg"])

if st.button("Atualizar Produtos"):
    update_product()
    product_id_update = None
    product_name_update = ""
    product_price_update = 0.0
    product_description_update = ""
    product_image_update = None
    return_message = "Produto atualizado com sucesso"
