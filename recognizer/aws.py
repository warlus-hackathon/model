import boto3

from recognizer.config import config

session = boto3.session.Session()

s3 = session.client(
    service_name='s3',
    endpoint_url=config.aws.endpoint,
    aws_access_key_id=config.aws.key_id,
    aws_secret_access_key=config.aws.key,
)
