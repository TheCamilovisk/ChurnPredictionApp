import logging
import os

import boto3
import config
import joblib
from sklearn.base import BaseEstimator


def load_churn_model() -> BaseEstimator:
    logger = logging.getLogger()

    download_path = "models/lr_model.joblib"

    if not os.path.isfile(download_path):
        if not os.path.isdir("models"):
            os.makedirs("models")

        logger.warning("Downloading model")
        s3_resource = boto3.resource("s3")
        bucket = s3_resource.Bucket(config.BUCKET_NAME)
        bucket.download_file(Key=config.MODEL_ARTIFACT_PATH, Filename=download_path)

    logger.warning("Loading model")
    model = joblib.load(download_path)
    return model
