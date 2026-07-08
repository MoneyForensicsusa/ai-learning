import requests
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
client = BlobServiceClient.from_connection_string(connection_string)

container_name = "documents"

def upload_file(loacal_path, blob_name):
    blob_client = client.get_blob_client(
        container=container_name,
        blob=blob_name
    )
    with open(loacal_path, "rb") as f:
        blob_client.upload_blob(f, overwrite=True)

    print(f"Uploaded: {blob_name}")

def download_file(blob_name, local_path):
    blob_client = client.get_blob_client(
        container=container_name,
        blob=blob_name
    )
    with open(local_path, "wb") as f:
        data = blob_client.download_blob()
        f.write(data.readall())
    print(f"Downloaded: {blob_name}")

def list_files():
    container_client = client.get_container_client(container_name)

    blobs = container_client.list_blobs()

    for blob in blobs:
        print(f'{blob.name} - {blob.size} bytes')

def get_sas_url(blob_name, hours=0):
    account_name = client.account_name
    account_key = os.getenv("AZURE_STORAGE_KEY")

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.now(timezone.utc) + timedelta(hours=hours)
    )

    print (f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}")

def delete_files(blob_name):
    blob_client = client.get_blob_client(
        container=container_name,
        blob=blob_name
    )
    blob_client.delete_blob()

    print(f"Deleted: {blob_name}")


def upload_folder(local_folder):
    for filename in os.listdir(local_folder):
        full_path = os.path.join(local_folder, filename)

        upload_file(full_path, filename)

def get_upload_sas_url(blob_name, hours=1):
    account_name = client.account_name
    account_key = os.getenv("AZURE_STORAGE_KEY")

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True, write=True, create=True),
        expiry=datetime.now(timezone.utc) + timedelta(hours=hours)
    )
    return f'https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}'

def test_upload_with_sas():
    sas_url = get_upload_sas_url('sas_uploaded.txt')

    with open('hello.txt', 'rb') as f:
        response = requests.put(
            sas_url,
            data=f,
            headers={'x-ms-blob-type': 'BlockBlob'}
        )
    print(response.status_code)
    print(response.text)

def backup_text_and_pdf_files(local_folder):
    file_count = 0
    total_size = 0

    for filename in os.listdir(local_folder):
        if filename.lower().endswith(".txt") or filename.lower().endswith(".pdf"):
            full_path = os.path.join(local_folder, filename)
            file_size = os.path.getsize(full_path)

            timestamp = datetime.now().strftime("%Y-%m-%d")
            blob_name = f'{timestamp}-{filename}'
            
            upload_file(full_path, blob_name)

            file_count = file_count + 1
            total_size = total_size + file_size
        else:
            print(f'Skipped: {file_count}')

backup_text_and_pdf_files("backup_files")