# ChurnPredictionAPP Rest API

## Table of contents

1. [Description](#description)
2. [Requirements](#requirements)
3. [Installing the dependencies](#installing-the-dependecies)
4. [How to run the server](#how-to-run-the-server)
   - [Setting environment variables](#setting-environment-variables)
   - [Install directly in the host machine](#install-directly-in-the-host-machine)
   - [Run via Docker](#run-via-docker)
5. [Solution Architeture](#solution-architecture)
6. [Machine Learning model overview](#machine-learning-model-overview)
7. [Creating the model file](#creating-the-model-file)
   - [Running without using AWS](#running-without-using-aws)

## Description

This folder contains the isolated code for the ChurnPredictionAPP Rest API. You can choose to run this server independently of the web page UI. This way, the provided API endpoints can be used by any client (e.g.: a Mobile App).

The server was built using [FastAPI][fastapi], a modern, fast (high-performance) web framework for building APIs with Python. The model used to make inferences through the API endpoint was built using the [Scikit-Learn][sklearn] and [Numpy][numpy] libraries, with help of [Pandas][pandas] library to load the required dataset.

Also, I used the [Telco Customer Churn][dataset] dataset to train the model.

## Requirements

- [Pipenv][pipenv] to install the Python project;
- [FastAPI][fastapi] and [Uvicorn][uvicorn] for the API server;
- [Pandas][pandas] (to optionally train the model), [Scikit-Learn][sklearn] and [Numpy][numpy];
- [Boto3][boto3] to interact with AWS services (optional);
- [Docker][docker] to run the containerized project (optional).

## Installing the dependecies

I used [Pipenv][pipenv] to manage this project dependencies. There are 3 ways to install this project:

- `pipenv install` - install only dependencies required to run the standalone server;
- `pipenv install --dev` or `pipenv install -d` - install development packages (i.e: linter and fommater) that I used during developoment (they work great with VSCode);
- Using **Docker** - section below.

**Note:** If you choose to install the project using _Pipenv_, don't forget to **activate your virtual environment** to execute the commands that I'll mention later.

## How to run the server

### Setting environment variables

First of all, you can set some environment variables if you plan to use an S3 bucket to store the prediction model, you'll need to have a accessable _S3 bucket_, where the model `.joblib` file will be stored. Then, set the following environment variables:

<pre><code>BUCKET_NAME=<b>YOUR_BUCKET_NAME</b>
MODEL_ARTIFACT_PATH=<b>NAME_OF_YOUR_JOBLIB_FILE</b>
AWS_ACCESS_KEY_ID=<b>AWS_ACCESS_KEY_ID</b>           (necessary only if you haven't set your AWS credentials file)
AWS_SECRET_ACCESS_KEY=<b>AWS_SECRET_ACCESS_KEY</b>   (necessary only if you haven't set your AWS credentials file)</code></pre>

If you want to know more about how to setup your AWS credentials file, check [this link][aws_credentials].

Now, to run the server, you have 2 options:

### Install directly in the host machine

This option easily gives freedom to customize and test the code, and to get most of it [install the project with development packages](#how-to-run-the-server).

After installing the project, you must get the model `.joblib` file. For this, you also have two options:

- Follow the instructions on [how to train the model from scratch](#creating-the-model-file), which will enable to run the server without the need of an S3 bucket or AWS credentials. This also enables our second option.
- If you already have a model file saved in a S3 bucket and the [environment variables](#setting-environment-variables) set accordingly, then you are good to go.

Whichever way you've chosen, with the `.joblib` file at it's right place and with your `Pipenv` environment activated, you just need to run:
```
pipenv shell                       # to activate the environment
uvicorn churn_api:app --port 8000
```
and the server will start. You can also supply the `--reload` argument, so the [FastAPI][fastapi] framework will watch your api project files for any modifications and automatically restart your server if an update is needed.

### Run via Docker

This is a good **deployment** option, as the dependencies installation and resource management is managed by Docker. You can also develop / customize the project in this mode, but this is not as straighforward.

First you need to build the image with the command `docker build -t churnprediction-api:latest .`. After that run:

<pre><code>docker run -it -p 8000:<b>HOST_PORT</b> \
-e AWS_ACCESS_KEY_ID=<b>AWS_ACCESS_KEY_ID</b> \
-e AWS_SECRET_ACCESS_KEY=<b>AWS_SECRET_ACCESS_KEY</b> \
churnprediction-api:latest</code></pre>

Where `HOST_PORT` is the port in your host machine that you want to access the API through, `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are[your AWS ID and secret][aws_credentials]. Note that for this execution option to work, you must to have a S3 bucket with a pre-trained model `.joblib` in it.

## API documentation

One of the most interesting features of [FastAPI][fastapi] is that it automatically builds an [OpenAPI Specification][openapi] for your API without any additional action.

With the API server running in your machine, in you browser, open the link `http://localhost:8000/docs`, and see the beatiful API documentation created by the framework.

![Churn Prediction API documentation][churn-prediction-api-docs]

## Solution Architecture

As mentioned before, the API was built using the [FastAPI][fastapi] framework. I chose this option instead of others (like [Flask][flask]) due to it's simple and robust approach, [high performance][fastapi-performance] (due to the use of asynchronous programming), great community and growing attention from industry.

The API makes use of a [Scikit-Learn][sklearn] model, that is loaded from a `.joblib` file, which can be obtained by either training the model from scratch or by downloading a pre-trained model from a specific S3 bucket.

The API is served, by default, through port `8000`. So, when [running the server using docker](#run-via-docker), rembemer redirect the right port.

Here is the general overview of the solution achiteture.

![Churn Prediction API Architeture][churn-prediction-api-architeture]

## Machine Learning model overview

The model itself used to make the API inferences is a simple Scikit-Learn [Logistic Regression][sklearn-logreg]. The inputs are pre-processed with the following approach:

- **Numerical features** are processed using the [MinMaxScaler][sklearn-minmax] transformer;
- **Categorical features** are processed using the [OneHotEncoder][sklearn-ohe] transformer.

Everything was conveniently put together using a Scikit-Learn's [Pipeline][sklearn-pipeline] object, enabling the easy model training and inference.

This model architeture is based on one of my Kaggle kernels, which can be found [here][kaggle-kernel]. A version of this kernel is also part of my [Data Science Notebooks repository][dsnotebooks], and can be also found [here][churnprediction-notebook].

Here is the overview of the model pipeline used in the API.

![Churn Prediction Model][churnprediction-model]

## Creating the model file

To create the `.joblib` model file you must follow the [1rst server execution option](#installing-the-dependecies) and have the project's virtual environment installed on your machine. Next, download the training [dataset][dataset] into the _data_ folder (in the root directory), and execute the following command:
```
pipenv shell               # to activate the virtual environment
python model_training.py
```

This will create the model `.joblib` file inside the _model_ (also in root directory). You can also supply the `--bucket-name` argument, passing the name of a existing S3 bucket name in which the model will be saved.

### Running without using AWS

With the model file in the right place, you don't need any AWS connection at all, and can opt to not set the [environment variables](#setting-environment-variables). This is also true when using the Docker image, as long as you set a volume pointing to the _models_ folder to the right place in the container. For example, you can run the following command:

<pre><code>docker run -it -p 8000:8000 \
-v <b>MODELS_FOLDER_LOCATION</b>:/app/models \
churnprediction-api:latest</code></pre>

this will make the application used the existing `.joblib` file instead of download a new one everytime it starts. This is greate if you're customizing this project and want to just test the Docker image.

<!-- Link Definitions -->

[churn-prediction-api-docs]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/openapi-page.png
[churn-prediction-api-architeture]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/churn-prediction-api-arch.png
[fastapi]: https://fastapi.tiangolo.com/
[pipenv]: https://pipenv.pypa.io/en/latest/
[uvicorn]: https://www.uvicorn.org/
[pandas]: https://pandas.pydata.org/
[sklearn]: https://scikit-learn.org/stable/
[numpy]: https://numpy.org/
[boto3]: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
[docker]: https://www.docker.com/
[dataset]: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
[aws_credentials]: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
[openapi]: https://swagger.io/specification/
[flask]: https://flask.palletsprojects.com/en/2.2.x/
[fastapi-performance]: https://fastapi.tiangolo.com/#performance
[sklearn-logreg]: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
[sklearn-minmax]: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html
[sklearn-ohe]: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
[sklearn-pipeline]: https://scikit-learn.org/stable/modules/compose.html
[kaggle-kernel]: https://www.kaggle.com/code/thecamilovisk/simple-end-to-end-project
[dsnotebooks]: https://github.com/TheCamilovisk/DSNotebooks
[churnprediction-notebook]: https://github.com/TheCamilovisk/DSNotebooks/tree/main/ChurnPrediction
[churnprediction-model]: https://raw.githubusercontent.com/TheCamilovisk/ChurnPredictionApp/main/imgs/churn-prediction-model.png
