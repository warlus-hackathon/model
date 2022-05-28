from pathlib import Path

from recognizer.aws import s3
from recognizer.config import config


def download_image(filename: str) -> None:

    upload_dir = Path('file_storage')
    upload_dir.mkdir(exist_ok=True, parents=True)
    s3.download_file(config.aws.bucket_input_images, filename, f'file_storage/{filename}')
