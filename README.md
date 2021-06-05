# Motion-Sensor-Technology-TCP-Socket-Programming

## Introduction
In this project, we are developing a streaming analytics system which aims to detect whether the person is running or walking and to prevent the person from repeating the same action for multiple times by sending health warnings.

## Data Source


## Data Cleaning
* Nominal Features:
  * “wrist”: refers to the hand on which the device was worn;  0 for “left” and 1 for “right”
  * “activity”: refers to the physical activity being performed; 0 for “walk” and 1 for “run”
* Ratio Features:
  * (x, y, z) acceleration & (x, y, z) gyro(orientation) values 


## Model Process

| Model                        | Training Accuracy | Testing Accuracy | F-Measure | Overfitting |
|------------------------------|-------------------|------------------|-----------|-------------|
| SVM                          | 0.9884            | 0.9880           | 0.9880    | No          |
| Decision Tree                | 1.0               | 0.9832           | 0.9833    | No          |
| Random Forest                | 1.0               | 0.9900           | 0.9900    | No          |
| Logistic Regression          | 0.8589            | 0.8600           | 0.8541    | No          |
| Gradient Boosting            | 0.9854            | 0.9836           | 0.9835    | No          |
| Stochastic Gradient Boosting | 0.8613            | 0.8609           | 0.8485    | No          |
| Perceptron                   | 0.8499            | 0.8486           | 0.8394    | No          |
| Naive Bayesian               | 0.9561            | 0.9567           | 0.9554    | No          |





* Link to our Kaggle publication page - https://www.kaggle.com/abbyding/motion-sensor-technology-tcp-socket-programming

