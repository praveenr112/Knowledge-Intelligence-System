import boto3
from botocore.exceptions import ClientError
from config import config

class S3Storage:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=config.AWS_ACCESS_KEY,
            aws_secret_access_key=config.AWS_SECRET_KEY
        )

        self.bucket = config.AWS_BUCKET_NAME


    def upload_file(self, file_obj, filename):
        try:
            self.s3.upload_fileobj(file_obj, self.bucket, filename)
            print(f"File {filename} uploaded successfully to S3 bucket {self.bucket}.")
            return True
        except ClientError as e:
            print(f"Error uploading file {filename} to S3: {e}")
            return False

    def get_file(self, filename):
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=filename)
            print(f"File {filename} retrieved successfully from S3 bucket {self.bucket}.")
            return response['Body'].read()
        except ClientError as e:
            print(f"Error retrieving file {filename} from S3: {e}")
            return None