# ChurnPredictionApp

This project is a simple approach to create a deployment process of a simple but complete Machine Learning App to AWS cloud services.

## Table of contents

1. [Introduction](#introduction)
2. [Original kaggle kernel](#original-kaggle-kernel)
3. [Live demo](#live-demo)
4. [Run locally](#run-locally)
    - [Use the local model file](#use-the-local-model-file)
    - [Use model file in S3 bucket](#use-model-file-in-s3-bucket)
    - [Run the app](#run-the-app)
5. [Deploy the app to an EC2 instance](#deploy-the-app-to-an-ec2-instance)
    - [Create an IAM role](#create-an-iam-role)
    - [Create an ECR image](#create-and-ecr-image)
    - [Create a security group](#create-a-security-group)
    - [Create an EC2 instance](#create-an-ec2-instance)
    - [Copy files to the EC2 instance](#copy-files-to-the-ec2-instance)
    - [Connect to the EC2 instance](#connect-to-the-ec2-instance)
    - [Finish instance setup and running the app](#finish-instance-setup-and-running-the-app)
    - [Access the deployed app](#access-the-deployed-app)
6. [Appendix](#appendix)
    - [What env_dependencies.sh does?](#what-env_dependenciessh-does)
    - [What setup_env.sh does?](#what-setup_envsh-does)
    - [What start.sh does?](#what-startsh-does)

## Introduction

As a Data Scientist, I love to understand the intrinsics of statistical learning and artificial intelligence, and, throughout my professional life, I also became aware of the importance of knowing the _basics of the whole process_, from the modelling of a ML solution to its deployment. This project is my approach to create a deployment process of a simple but complete Machine Learning App to AWS cloud services.

It consists in 2 main components: the [backend][churnprediction-api] written in Python, and the frontend written in simple HTML, CSS and vanilla Javascript.

When deployed to an EC2 instance, it's meant to run behind a [Nginx][nginx] proxy server. But don't worry, as I created scripts to make some basic configurations to make the app up and running.

**Note 1:** This is the complete example solution, meant to be deployed to an AWS EC2 instance. If you want just the REST API backend implementation, it can be found in the [api folder][churnprediction-api] of this repository.

**Note 2:** This project is meant to be for learning purposes, for both readers and myself. So, if you find any problem or are aware of better ways of doing some of the things that I do here, please let me know. And don't forget to be kind.

## Original kaggle kernel

[This kaggle kernel][kaggle-kernel] shows my in-depth analysis about the Churn prediction problem. There you can find my reasonig about the design of the prediction model and a comparision with other classification models.

## Run locally

First of all, before you deploy this solution to an EC2 instance, you can test it locally on you machine. For this, enter the api folder, and follow the instructions on how to [create the model file][create-model-file] used for inference. You can either choose to use the created model file or save it to an S3 bucket.

With the `.joblib` model file create, open the [docker-compose file][docker-compose-file] in the root directory of this repository. Now, you have two options:

### Use the local model file

The model training script will create the `.joblib` file in path `api/models/lr_model.joblib`. So, you just need to uncomment the following lines.

```
# volumes:
#   - ./api/models:/app/models
```

### Use model file in S3 bucket

If you opted to save the model in a S3 bucket and want to use it, you must create the `api/.env` file and place the following environment varibles

<pre><code>BUCKET_NAME=<b>YOUR_BUCKET_NAME</b>
MODEL_ARTIFACT_PATH=<b>NAME_OF_YOUR_JOBLIB_FILE</b>
AWS_ACCESS_KEY_ID=<b>AWS_ACCESS_KEY_ID</b>
AWS_SECRET_ACCESS_KEY=<b>AWS_SECRET_ACCESS_KEY</b></code></pre>

After that, uncomment the following lines in the [docker-compose file][docker-compose-file]:

```
# env_file:
#   - ./api/.env
```

**Note:** The `.env` file that is used by default is just and example. This file can be in any location, just be sure to supply the right path to `env_file` parameter.

### Run the app

After making the required modification according with your choice, in the root folder of the project, run:

```
docker-compose up
```

Wait for the services start up to complete and, in your browser, access `http://localhost`. You should see the app page.

![Churn Prediction App Page][app-screen]

Then you can conclude that:

1. I'm big fan of dark themes 😜️
2. I'm a really bad web designer 😔️

## Deploy the app to an EC2 instance

Let's make the app available to the external world, by deploying it to an [AWS EC2][ec2-site] instance. For this, you'll need to have an AWS account. If you don't have one yet, just follow [these guidelines][aws-create-account], and you'll be good to go.

**Note 1:** Our configuration will be very simple, and, in theory, you won't need to step off the [Free Tier][free-tier] limits (I've tested it myself). **BUT** I garantee nothing, specially if you've used a lot of you quota already. Then, be careful about your limits to not be charged. You've been warned, OK 👍️?

**Note 2:** I strongly suggest you to make some basic **security configuration** to protect your account and enable a billing alarm. Just follow [this video][secure-aws-account] and you're good to go.

### Create an IAM role

After log in the [AWS Management Console][aws-console], search for the **IAM** service in the search bar.

![Search bar][aws-searchbar]

![Access IAM menu][access-iam]

From there, we'll crate a new role.

![IAM menu][iam-menu]

![Create role][create-role-buttom]

Choose **AWS service** in **Trusted entity type** and **EC2** in **Use case**. Click **Next**.

![Trusted entity type][trusted-entity-type]

Add the **AmazonS3ReadOnlyAccess** and the **AWSAppRunnerServicePolicyForECRAccess** permissions. Click Next

![S3 read only access][s3-readonly-acess]

![ECR access][ecr-access]

Name the role and, optionally, give a description and tags to it. Review everything and click in **Create role** at the end of the page.

![Review role][role-review]

![Create role buttom][final-create-role]

### Create an ECR image

The Amazon [ECR][aws-ecr] is a fully managed container registry offering  high-performance hosting, so users can realibly deploy application images and artifacts anywhere. We'll use it to easily deploy our [Churn Prediction API][churnprediction-api] into EC2 instances.

**Note:** This step requires the AWS CLI tool [installed][aws-cli-install] and [configured][aws-cli-setup] in your local machine.

First of all, we must login into ECR service. Open your terminal and execute this command, replacing **AWS_ACCOUNT_ID** and **REGION** with your AWS account ID and the AWS region you want the app to live, respectively.

<pre><code>aws ecr get-login-password  --region <b>REGION</b> | docker login --username AWS --password-stdin <b>AWS_ACCOUNT_ID</b>.dkr.ecr.<b>REGION</b>.amazonaws.com</code></pre>

After that, create the repository your docker image will live in. You can either create it in the [ECR dashboard][ecr-dashboard] or directly in AWS console. Be careful to select the region you've choose.

```
aws ecr create-repository --repository-name churn_prediction_api
```

Next, go to the [api][churnprediction-api] folder of this repository and build the docker image inside.

```
cd api
docker build -t churn_prediction_api:latest .
```

Tag the image, so you can push the image to the ECR repository

<pre><code>docker tag churn_prediction_api:latest <b>AWS_ACCOUNT_ID</b>.dkr.ecr.<b>REGION</b>.amazonaws.com/churn_prediction_api</code></pre>

Finally, push the docker image to the repository:

<pre><code>docker push <b>AWS_ACCOUNT_ID</b>.dkr.ecr.<b>REGION</b>.amazonaws.com/churn_prediction_api</code></pre>

### Create a security group

Now let's create a secure group to define how to handle connections to your EC2 instance.

Search for **EC2** service in AWS Management Console search bar.

![Find the EC2 service][searchbar-ec2]

In EC2 menu, find the **Security Groups** in the right sidebar, under **Network & Security**. There, click in **Create security group**.

![Security Groups Menu][security-groups-menu]

Name your security group and define **3 inbound rules** (click in the **Add rule** buttom) as follows :
- One of type **SSH**, with **your IP** as source. This will enable ssh connections from your IP only (just to be safe).
- One of type **HTTP**, with **anywhere** as source. This will enable to access the app from anywhere using **http protocol**.
- One of type **HTTPS**, with **anywhere** as source. This will enable to access the app from anywhere using **https protocol**.

![Create a security group][security-group-definiton]

Click in **Create security group** buttom at the end of the page to finish the group creation.

### Create an EC2 instance

In the EC2 service dashboard, access the **Instances** menu in the left sidebar. There, click in **Launch instances**.

![Launch EC2 instance][launch-ec2-instance]

In **Launch an instance** menu, name your instance and select the **Amazon Linux 2 AMI** (free tier eligible).

![EC2 naming and AMI selection][ec2-naming-ami]

Make sure that that you **instance type** is **t2.micro** (free tier eligible) and, if you don't have one yet, create a new **key pair**, of type **RSA** and file format as **.perm** (if you're using OpenSSH and you local machine is Linux) or **.ppk** (if you're using PuTTY and your local machine is Windows). You'll use this key pair to access the EC2 instance from your local machine, so download it and keep it safe.

**Note:** DON'T SHARE YOU KEY PAIR.

![Select instance type and key pair][instance-type-keypair]

![Create a key pair][create-key-pair]

Under **Network settings** select your previously created **security group**.

![Select the previously created security group][network-settings]

Under **Advanced details**, in **IAM instance profile**, select the **role** that you've also previously created.

![Select the previously created role and launch the instance][select-role-and-launch]

Back to the **Instances** menu, wait for the **instance state** to become **Running** and all status checks have passed.

![Check the instance status][instance-status]

Now you can proceed to the next step.

### Copy files to the EC2 instance

We'll send to the instance the html and configuration files required by our app to work.

From the repository's root, zip the **html** and **config** folders with the command

```
zip -r package.zip html config
```

We'll need the **public IPv4 DNS** of the instance. Go to the **Instances** dashboard in the AWS management console and get it.

![Retrieve the instance's IPV4 DNS][instance-ipv4-dns]

Now send the zip file to the instance using the this command, replacing **KEY_PAIR_LOCATION** and **INSTANCE_IPV4_DNS** with your key pair and the instance IPv4 DNS, respectively.

<pre><code>scp -i <b>KEY_PAIR_LOCATION</b> package.zip ec2-user@<b>INSTANCE_IPV4_DNS</b>:~/.</code></pre>

The rest of the setup will be made directly to the instance.

### Connect to the EC2 instance

Now, your must stablish a connection between your local machine to the EC2 instance to complete the app configuration.

Execute this command, replacing **KEY_PAIR_LOCATION** and **INSTANCE_IPV4_DNS** with your key pair and the instance IPv4 DNS, respectively.

<pre><code>ssh -i <b>KEY_PAIR_LOCATION</b> ec2-user@<b>INSTANCE_IPV4_DNS</b></code></pre>

If everything went right, your prompt will be connected to the instance

![Prompt connect to the EC2 instance][connected-to-instance]

### Finish instance setup and running the app

Inside the instance, unzip the uploaded package.

```
unzip package.zip
```

Folder **config** and **html** will be expanded to the current directory. Navigate to path **config/scripts**, and run the command:

```
. env_dependencies.sh
```

**Note 1:** See section [What env_dependencies.sh does?](#what-env_dependenciessh-does).

**Press `Ctrl + d` to logout from the instance and login again right after**.

Now you need to define 3 enviroment variables.

**Note 3:** I'm assuming that you've followed the instructions on [how to create the model .joblib file][how-to-create-model-file] and have it stored into a S3 bucket (also included in instructions).

<pre><code>export BUCKET_NAME=<b>YOUR_BUCKET_NAME</b>
export MODEL_ARTIFACT_PATH=<b>NAME_OF_YOUR_JOBLIB_FILE</b>
export REGION=<b>INSTANCE_REGION</b></code></pre>

Navigate again to **config/scripts**, and run:

```
. setup_env.sh
```

**Note 2:** See section [What setup_env.sh does?](#what-setup_envsh-does).

Still inside folder **config/scripts**, run the **start** script.

```
. start.sh
```

**Note 4:** See section [What start.sh does?](#what-startsh-does).

### Access the deployed app

Finally 🙌️, it's time to access the deployed app. Open the [instance IPv4 DNS that you've retrieved early](#copy-files-to-the-ec2-instance) in your browser. If everything was done right, you will see the app page, now accessible for anyone 😃️.

**Note:** I (kind of) tried to make the page responsive. So you may have a better experience in different devices. 📱️

## Appendix

### What env_dependencies.sh does?

This script is responsible for the installation [Docker][docker] and [Nginx][nginx] to EC2 instance. It also adds the default user (ec2-user) to the docker group, so the user doesn't need *super user* previleges when running a docker command.

```
sudo amazon-linux-extras install -y docker
```

This line installs the **docker** package from the oficial Amazon repositories.

```
sudo amazon-linux-extras install -y nginx1
```

In the same way as the last command, this line install Nginx.

```
sudo gpasswd -a ${USER} docker
```

This line adds the **current user** (supplied by the **USER** environment variable) to the **docker** group.

**Note:** User group modifications only take effect in the next login to the host system. This is why I instructed you, after executing this script, to logout and login right after during the [EC2 instance setup](#finish-instance-setup-and-running-the-app). So, don't skip this step.

### What setup_env.sh does?

This script is responsible of:
- Place the static page and configuration files to their right places
- Start the nginx and docker system services.
- Pull the REST API docker image from ECR.

```
sudo cp ../nginx/default.conf /etc/nginx/conf.d/default.conf
```

This line places the NGINX configuration file in it's right place. This file basically tells where to find the **main.html** of the static site, and also serves as **reverse proxy** to our local API endpoint, redirecting the calls to address `http://localhost/api` to `http://localhost:8000/` (the default port configured as our API endpoint).

```
sudo cp ../../html/* /usr/share/nginx/html
```

This line copies the **main.html**, **main.css** and **main.js** to the default NGINX server static files folder. This folder already has all required access permissions for Nginx.

```
sudo service nginx restart
sudo service docker restart
```

These lines restart the docker and nginx system services (and starts them, if they aren't running already).

```
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
```

This retrieves your AWS account ID.

```
aws ecr get-login-password  --region sa-east-1 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
```

This line will login your docker service into ECR.

```
docker pull $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/churn_prediction_api:latest
```

This line pulls the REST API image from ECR.

### What start.sh does?

This script is responsible for starting up the REST API endpoint.

```
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
```
This line was already detailed in section about [setup_env.sh](#what-setup_envsh-does).

```
docker run -d -p 8000:8000 -e BUCKET_NAME=$BUCKET_NAME -e MODEL_ARTIFACT_PATH=$MODEL_ARTIFACT_PATH $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/churn_prediction_api:latest
```
This line runs the API image and exposes it through port 8000.

<!-- Link Definitions -->

[churnprediction-api]: https://github.com/TheCamilovisk/ChurnPredictionApp/tree/main/api
[nginx]: https://www.nginx.com/
[docker]: https://www.docker.com/
[kaggle-kernel]: https://www.kaggle.com/code/thecamilovisk/simple-end-to-end-project
[live-preview]: http://ec2-18-228-8-103.sa-east-1.compute.amazonaws.com
[create-model-file]: https://github.com/TheCamilovisk/ChurnPredictionApp/tree/main/api#creating-the-model-file
[docker-compose-file]: https://github.com/TheCamilovisk/ChurnPredictionApp/blob/main/docker-compose.yml
[app-screen]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/app-screen.png
[ec2-site]: https://aws.amazon.com/ec2/
[aws-create-account]: https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/
[free-tier]: https://aws.amazon.com/free
[secure-aws-account]: https://www.youtube.com/watch?v=FRQ9fE4fd5g
[aws-console]: https://aws.amazon.com/console/
[aws-searchbar]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/aws-searchbar.png
[access-iam]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/searchbar-iam.png
[iam-menu]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/roles-menu.png
[create-role-buttom]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/create-role-buttom.png
[trusted-entity-type]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/trusted-entity-type.png
[s3-readonly-acess]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/s3-readonly-access.png
[ecr-access]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/ecr-access.png
[role-review]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/role-review.png
[final-create-role]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/final-create-role.png
[searchbar-ec2]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/searchbar-ec2.png
[security-groups-menu]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/security-groups-menu.png
[security-group-definiton]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/security-group-definition.png
[aws-ecr]: https://aws.amazon.com/ecr/
[aws-cli-install]: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
[aws-cli-setup]: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html
[ecr-dashboard]: https://console.aws.amazon.com/ecr/repositories
[launch-ec2-instance]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/launch-ec2-instance.png
[ec2-naming-ami]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/ec2-naming-ami.png
[instance-type-keypair]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/instance-type-keypair.png
[create-key-pair]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/create-key-pair.png
[network-settings]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/network-settings.png
[select-role-and-launch]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/select-role-and-launch.png
[instance-status]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/instance-status.png


[instance-ipv4-dns]: imgs/instance-ipv4-dns.png


[connected-to-instance]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/connected-to-instance.png
[how-to-create-model-file]: https://github.com/TheCamilovisk/ChurnPredictionApp/tree/main/api#creating-the-model-file
