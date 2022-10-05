import os
from os import path

from dotenv import load_dotenv


ROOT = path.normpath(path.dirname(__file__))

load_dotenv(path.join(ROOT, ".env"))

BUCKET_NAME = os.environ["BUCKET_NAME"]
MODEL_PATH = os.environ["MODEL_PATH"]
TARGET_ENCODER_PATH = os.environ["TARGET_ENCODER_PATH"]

MODEL_LOCAL_FOLDER = path.join(ROOT, "models")
MODEL_LOCAL_PATH = path.join(MODEL_LOCAL_FOLDER, "lr_model.joblib")
TARGET_ENCODER_LOCAL_PATH = path.join(MODEL_LOCAL_FOLDER, "target_enconder.joblib")
