from fastapi import APIRouter
from .. import models


router = APIRouter(prefix="/features", tags=["features"])


@router.get("/")
async def get_categorical_features_values() -> dict:
    feature_values = {
        "MultipleLines": [e.value for e in models.PhoneDependentService],
        "InternetService": [e.value for e in models.InternetService],
        "OnlineSecurity": [e.value for e in models.InternetDependentService],
        "OnlineBackup": [e.value for e in models.InternetDependentService],
        "DeviceProtection": [e.value for e in models.InternetDependentService],
        "TechSupport": [e.value for e in models.InternetDependentService],
        "StreamingTV": [e.value for e in models.InternetDependentService],
        "StreamingMovies": [e.value for e in models.InternetDependentService],
        "Contract": [e.value for e in models.Contract],
        "PaymentMethod": [e.value for e in models.PaymentMethod],
    }

    return {"categorical_feature_values": feature_values}
