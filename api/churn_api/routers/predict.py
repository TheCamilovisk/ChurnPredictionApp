from enum import Enum
from typing import List

import pandas as pd
from fastapi import APIRouter

from ..models import Payload
from ..utils import load_churn_model

lr_model = load_churn_model()

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
async def predict_churn_list(payload: List[Payload]) -> dict:
    model_input = payload_to_input(payload)
    predictions = ["Yes" if v == 1 else "No" for v in lr_model.predict(model_input)]
    output = [
        {row.customerID: prediction} for row, prediction in zip(payload, predictions)
    ]
    return {"predictions": output}
