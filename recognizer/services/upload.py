from pathlib import Path

from recognizer.aws import s3
from recognizer.config import config


def upload_image(filename: str) -> None:

    upload_dir = Path('recognizer/file_storage')
    s3.upload_file(str(upload_dir / filename), config.aws.bucket_output_images, filename)
