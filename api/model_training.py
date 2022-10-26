import os
import typing
from argparse import ArgumentParser

import boto3
import joblib
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelBinarizer, MinMaxScaler, OneHotEncoder


def write_model_to_bucket(output_bucket_name: str) -> None:
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(output_bucket_name)
    bucket.upload_file(Filename="models/lr_model.joblib", Key="models/lr_model.joblib")


def main(output_bucket_name: typing.Optional[str]) -> None:
    churn_df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    churn_df.TotalCharges = pd.to_numeric(churn_df.TotalCharges, errors="coerce")
    churn_df.dropna(axis="rows", inplace=True)
    churn_df.SeniorCitizen = churn_df.SeniorCitizen.apply(
        lambda val: "Yes" if val else "No"
    )

    categorical_features = [
        "gender",
        "SeniorCitizen",
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

    if not os.path.isdir("models"):
        os.makedirs("models")

    joblib.dump(model_pipeline, "models/lr_model.joblib")

    if output_bucket_name:
        write_model_to_bucket(output_bucket_name)


if __name__ == "__main__":
    ap = ArgumentParser()
    ap.add_argument(
        "-b",
        "--bucket-name",
        type=str,
        required=False,
        help="S3 bucket where the model will be uploaded to. It assumed that the bucket exists.",
    )
    args = ap.parse_args()

    bucket_name = args.bucket_name
    main(bucket_name)
