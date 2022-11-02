# ChurnPredictionApp

As a Data Scientist, I love to understand the intrinsics of statistical learning and artificial intelligence, and, throughout my professional life, I also became aware of the importance of knowing the _basics of the whole process_, from the modelling of a ML solution to its deployment. This project is my approach to create a deployment process of a simple but complete Machine Learning App to AWS cloud services.

It consists in 2 main components: the [backend][churnprediction-api] written in Python, and the frontend written in simple HTML, CSS and vanilla Javascript.

When deployed to an EC2 instance, it's meant to run behind a [Nginx][nginx] proxy server. But don't worry, as I created scripts to make some basic configurations to make the app up and running.

**Note 1:** This is the complete example solution, meant to be deployed to an AWS EC2 instance. If you want just the REST API backend implementation, it can be found in the [api folder][churnprediction-api] of this repository.

**Note 2:** This project is meant to be for learning purposes, for both readers and myself. So, if you find any problem or are aware of better ways of doing some of the things that I do here, please let me know. And don't forget to be kind.

<!-- Link Definitions -->

[churnprediction-api]: https://github.com/TheCamilovisk/ChurnPredictionApp/tree/main/api
[nginx]: https://www.nginx.com/