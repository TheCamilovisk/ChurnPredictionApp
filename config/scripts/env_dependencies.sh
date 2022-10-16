sudo amazon-linux-extras install -y docker
sudo amazon-linux-extras install -y nginx1

sudo gpasswd -a ec2-user docker
sudo gpasswd -a nginx ec2-user

