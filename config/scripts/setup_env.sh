sudo cp ../nginx/default.conf /etc/nginx/conf.d/default.conf
sudo cp ../../html/* /usr/share/nginx/html

sudo service nginx restart

sudo service docker restart

ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

aws ecr get-login-password  --region sa-east-1 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
docker pull $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/churn_prediction_api:latest