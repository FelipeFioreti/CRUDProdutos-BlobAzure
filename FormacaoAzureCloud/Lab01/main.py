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

st.title("Casdastro de Produtos")

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

if st.button("Salvar Produto"):
    insert_product(product_name,product_price,product_description,product_image)
    return_message = "Produto salvo com sucesso"

st.header("Produtos Cadastrados")

if(st.button("Listar Produtos")):
    return_message = "Produtos listados com sucesso"

