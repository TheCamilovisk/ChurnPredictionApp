sudo cp ${HOME}/ChurnPredictionApp/config/nginx/default.conf /etc/nginx/conf.d/default.conf
sudo cp ${HOME}/ChurnPredictionApp/html/* /usr/share/nginx/html

sudo chmod -R g+x ${HOME}

sudo service nginx restart

sudo service docker restart

aws ecr get-login-password  --region sa-east-1 | docker login --username AWS --password-stdin 877885770422.dkr.ecr.sa-east-1.amazonaws.com
docker pull 877885770422.dkr.ecr.sa-east-1.amazonaws.com/churn_prediction_api:latest