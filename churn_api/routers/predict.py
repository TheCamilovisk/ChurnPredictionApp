from enum import Enum
from typing import List

import pandas as pd
from fastapi import APIRouter
from joblib import load

from ..models import Payload
import config

lr_model = load(config.MODEL_LOCAL_PATH)
target_encoder = load(config.TARGET_ENCODER_LOCAL_PATH)

router = APIRouter(prefix="/predict", tags=["predict"])


def payload_to_input(payload: List[Payload]) -> pd.DataFrame:
    processed_data = []
    for input in payload:
        payload_dict = {
            key: value.value if isinstance(value, Enum) else value
            for key, value in input.dict().items()
        }
        processed_data.append(payload_dict)
    return pd.DataFrame(processed_data)


@router.post("/")
async def predict_churn_list(payload: List[Payload]):
    model_input = payload_to_input(payload)
    predictions = target_encoder.inverse_transform(
        lr_model.predict(model_input)
    ).tolist()
    output = [
        {row.customerID: prediction} for row, prediction in zip(payload, predictions)
    ]
    return {"predictions": output}
