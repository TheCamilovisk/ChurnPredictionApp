import os
from os import path

from dotenv import load_dotenv

ROOT = path.normpath(path.dirname(__file__))

load_dotenv(path.join(ROOT, ".env"))

BUCKET_NAME = os.environ.get("BUCKET_NAME")
MODEL_ARTIFACT_PATH = os.environ.get("MODEL_ARTIFACT_PATH")
