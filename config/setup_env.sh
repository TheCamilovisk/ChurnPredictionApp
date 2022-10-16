sudo amazon-linux-extras install -y docker
sudo amazon-linux-extras install -y nginx

sudo gpasswd -a ${USER} docker
sudo gpasswd -a nginx ${USER}

sudo cp ${HOME}/ChurPredictionApp/config/nginx/default.conf /etc/nginx/config.d/default.conf

sudo chmod -R g+x ${HOME}

sudo service nginx restart

sudo service docker restart

aws ecr get-login-password  --region sa-east-1 | docker login --username AWS --password-stdin 877885770422.dkr.ecr.sa-east-1.amazonaws.com
docker pull 877885770422.dkr.ecr.sa-east-1.amazonaws.com/churn_prediction_api:latest

