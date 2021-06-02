import os, uuid
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient

def blob_storage():
            try:
                #To create connection with the Azure storage
                connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
                print(connect_str)


                #To create a instance of BlobserviceClient to use method 
                blob_service_client = BlobServiceClient.from_connection_string(connect_str)
                
                #To create a container with create container method 
                container_name = 'storagecontain'
                container_client = blob_service_client.create_container(container_name)
    
                
                
                #To create Local path to hold blob data
                local_path = "F:\AZURE\Azure Blob Storage"

                #To create a file to upload with the data 
                local_file_name = "stock.txt"
                upload_file_path = os.path.join(local_path, local_file_name)
                file = open(upload_file_path, 'w')
                file.write("This is the data of stock market ")
                file.close()
    
                #To create a blob client using local file name as name of blob
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

                print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

                #To upload the data 
                with open(upload_file_path, "rb") as data:
                    blob_client.upload_blob(data)
                
                #To download the data
                download_file_name = "download.txt"
                download_file_path = os.path.join(local_path,download_file_name)
                with open(download_file_name,"wb") as download_data:
                    download_data.write(blob_client.download_blob().readall())
                        
            except Exception as error:
                print(error)

blob_storage()