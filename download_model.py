import logging
from os import makedirs, path

import boto3

import config

if __name__ == "__main__":
    logger = logging.getLogger()

    if not path.isdir(config.MODEL_LOCAL_FOLDER):
        logger.warning("Creating models folder")
        makedirs(config.MODEL_LOCAL_FOLDER)

    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(config.BUCKET_NAME)

    if not path.isfile(config.MODEL_LOCAL_PATH):
        logger.warning("Downloading model file")
        bucket.download_file(config.MODEL_PATH, config.MODEL_LOCAL_PATH)
