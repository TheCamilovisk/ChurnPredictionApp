import logging
from io import BytesIO

import boto3
import config
import joblib
from sklearn.base import BaseEstimator


def load_churn_model() -> BaseEstimator:
    logger = logging.getLogger()
    logger.warning("Loading model")

    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(config.BUCKET_NAME)
    with BytesIO() as data:
        bucket.download_fileobj(config.MODEL_ARTIFACT_PATH, data)
        data.seek(0)
        model = joblib.load(data)
    return model
