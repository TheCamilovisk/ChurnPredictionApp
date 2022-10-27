docker run -d -p 8000:8000 \
    -e BUCKET_NAME=$BUCKET_NAME \
    -e MODEL_ARTIFACT_PATH=$MODEL_ARTIFACT_PATH \
    877885770422.dkr.ecr.sa-east-1.amazonaws.com/churn_prediction_api:latest