import os

from pydantic import BaseModel


class AwsConfig(BaseModel):
    key_id: str
    key: str
    bucket_input_images: str
    bucket_output_images: str
    bucket_output_cvs: str


class AppConfig(BaseModel):
    endpoint: str
    aws: AwsConfig


def load_from_env() -> AppConfig:
    endpoint = os.environ['ENDPOINT']
    aws_bucket_input_images = os.environ['AWS_BUCKET_NAME_INPUT_IMAGES']
    aws_bucket_output_images = os.environ['AWS_BUCKET_NAME_OUTPUT_IMAGES']
    aws_bucket_output_cvs = os.environ['AWS_BUCKET_NAME_OUTPUT_CVS']
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    return AppConfig(
        endpoint=endpoint,
        aws=AwsConfig(
            key_id=aws_access_key_id,
            key=aws_secret_access_key,
            bucket_input_images=aws_bucket_input_images,
            bucket_output_images=aws_bucket_output_images,
            bucket_output_cvs=aws_bucket_output_cvs,
        )
    )


config = load_from_env()
