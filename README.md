# ChurnPredictionApp

## Table of contents

1. [Introduction](#introduction)
2. [Run locally](#run-locally)
    - [Use the local model file](#use-the-local-model-file)
    - [Use model file in S3 bucket](#use-model-file-in-s3-bucket)
    - [Run the app](#run-the-app)

## Introduction

As a Data Scientist, I love to understand the intrinsics of statistical learning and artificial intelligence, and, throughout my professional life, I also became aware of the importance of knowing the _basics of the whole process_, from the modelling of a ML solution to its deployment. This project is my approach to create a deployment process of a simple but complete Machine Learning App to AWS cloud services.

It consists in 2 main components: the [backend][churnprediction-api] written in Python, and the frontend written in simple HTML, CSS and vanilla Javascript.

When deployed to an EC2 instance, it's meant to run behind a [Nginx][nginx] proxy server. But don't worry, as I created scripts to make some basic configurations to make the app up and running.

**Note 1:** This is the complete example solution, meant to be deployed to an AWS EC2 instance. If you want just the REST API backend implementation, it can be found in the [api folder][churnprediction-api] of this repository.

**Note 2:** This project is meant to be for learning purposes, for both readers and myself. So, if you find any problem or are aware of better ways of doing some of the things that I do here, please let me know. And don't forget to be kind.

## Run locally

First of all, before you deploy this to solution into an EC2 instance, you can test it locally on you machine. For this, enter the api folder, and follow the instructions on how to [create the model file][create-model-file] used for inference. You can either choose to use the created model file or save it to an S3 bucket.

With the `.joblib` model file create, open the [docker-compose file][docker-compose-file] in the root directory of this repository. Now, you have two options:

### Use the local model file

The model training script will create the `.joblib` file in path `api/models/lr_model.joblib`. So, you just need to make the uncomment the follwoing lines.

```
# volumes:
#   - ./api/models:/app/models
```

### Use model file in S3 bucket

If you opted to save the model in a S3 bucket and want to use it, you must create the `api/.env` file and place the following environment varibles

```
BUCKET_NAME=<YOUR_BUCKET_NAME>
MODEL_ARTIFACT_PATH=<NAME_OF_YOUR_JOBLIB_FILE>
AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
```

After that, uncomment the following lines in the [docker-compose file][docker-compose-file]:

```
# env_file:
#   - ./api/.env
```

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

<!-- Link Definitions -->

[churnprediction-api]: https://github.com/TheCamilovisk/ChurnPredictionApp/tree/main/api
[nginx]: https://www.nginx.com/
[create-model-file]: https://github.com/TheCamilovisk/ChurnPredictionApp/tree/main/api#creating-the-model-file
[docker-compose-file]: https://github.com/TheCamilovisk/ChurnPredictionApp/blob/main/docker-compose.yml
[app-screen]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/app-screen.png