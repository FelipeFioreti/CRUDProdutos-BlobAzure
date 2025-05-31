import os
import uuid
import pymssql
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

class ProductManager:
    def __init__(self):
        self.blob_connection_string = os.getenv("BLOB_CONNECTION_STRING")
        self.blob_container_name = os.getenv("BLOB_CONTAINER_NAME")
        self.blob_account_name = os.getenv("BLOB_ACCOUNT_NAME")

        self.sql_server = os.getenv("SQL_SERVER")
        self.sql_database = os.getenv("SQL_DATABASE")
        self.sql_user = os.getenv("SQL_USER")
        self.sql_password = os.getenv("SQL_PASSWORD")

    def upload_blob(self, file):
        blob_service_client = BlobServiceClient.from_connection_string(self.blob_connection_string)
        container_client = blob_service_client.get_container_client(self.blob_container_name)
        blob_name = str(uuid.uuid4()) + file.name
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file.read(), overwrite=True)
        return f"https://{self.blob_account_name}.blob.core.windows.net/{self.blob_container_name}/{blob_name}"

    def connect_db(self):
        return pymssql.connect(server=self.sql_server, user=self.sql_user,
                               password=self.sql_password, database=self.sql_database)

    def insert_product(self, name, price, description, image_file):
        try:
            image_url = self.upload_blob(image_file)
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO Produtos (Nome, Descricao, Preco, Imagem_URL) VALUES ('{name}','{description}','{price}','{image_url}') ")
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    def list_products(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Produtos")
            products = cursor.fetchall()
            conn.close()
            return products
        except Exception as e:
            return []

    def update_product(self, product_id, name, price, description, product_image):
        try:

            conn = self.connect_db()
            cursor = conn.cursor()

            if product_image:
                image_url = self.upload_blob(product_image)
                cursor.execute(f"UPDATE Produtos SET Nome = '{name}', Descricao = '{description}', Preco = {price}, Imagem_URL = '{image_url}' WHERE ID = {product_id}")
            else:
                image_url = ''
                cursor.execute(f"UPDATE Produtos SET Nome = '{name}', Descricao = '{description}', Preco = {price} WHERE ID = {product_id}")
    
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    def delete_product(self, product_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM Produtos WHERE ID={product_id}")
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False
