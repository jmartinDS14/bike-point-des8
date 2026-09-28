import os
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME=os.getenv('AWS_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

files_to_upload=os.listdir('data')

for file in files_to_upload:
    file_to_upload = f'data/{file}'
    try:
        s3_client.upload_file(file_to_upload,AWS_BUCKET_NAME,file)
        print(f'{file} uploaded successfully.')
        os.remove(file_to_upload)
    except Exception as e:
        print(f'An error has occurred: {e}')