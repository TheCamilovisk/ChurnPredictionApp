import boto3
import joblib
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelBinarizer, MinMaxScaler, OneHotEncoder

import config

if __name__ == "__main__":
    churn_df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    churn_df.TotalCharges = pd.to_numeric(churn_df.TotalCharges, errors="coerce")
    churn_df.dropna(axis="rows", inplace=True)

    categorical_features = [
        "gender",
        "Partner",
        "Dependents",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
    ]

    numerical_features = [
        "SeniorCitizen",
        "MonthlyCharges",
        "TotalCharges",
        "tenure",
    ]

    model_pipeline = make_pipeline(
        make_column_transformer(
            (OneHotEncoder(sparse=False), categorical_features),
            (MinMaxScaler(feature_range=(0.0, 0.1)), numerical_features),
        ),
        LogisticRegression(max_iter=500),
    )

    churn_transformer = LabelBinarizer()

    target = churn_transformer.fit_transform(churn_df.Churn).squeeze()

    model_pipeline.fit(churn_df, target)

    joblib.dump(model_pipeline, config.MODEL_LOCAL_PATH)
    joblib.dump(churn_transformer, config.TARGET_ENCODER_LOCAL_PATH)

    s3_resource = boto3.resource("s3")
    s3_bucket = s3_resource.Bucket(config.BUCKET_NAME)

    s3_bucket.upload_file(config.MODEL_LOCAL_PATH, config.MODEL_PATH)
    s3_bucket.upload_file(config.TARGET_ENCODER_LOCAL_PATH, config.TARGET_ENCODER_PATH)
