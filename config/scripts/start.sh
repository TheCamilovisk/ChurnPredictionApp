ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

docker run -d -p 8000:8000 \
    -e BUCKET_NAME=$BUCKET_NAME \
    -e MODEL_ARTIFACT_PATH=$MODEL_ARTIFACT_PATH \
    $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/churn_prediction_api:latest