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

## Server Side Implementation

 1. The API called the server to set up a listening socket, which listens to a connection from the client. Once the client is ready to connect, it calls connect and the server calls accept to establish the connection. 

 2. The server loads cleaned testing dataset. Each row in the dataset is loaded into dictionary format as shown below:
    * {"wrist": "0", "acceleration_x": "0.265", "acceleration_y": "-0.7814", "acceleration_z": "-0.0076", "gyro_x": "-0.059", "gyro_y": "0.0325", "gyro_z": "-2.9296", "label": "0"}

 3. We store the actual run/walk status into variable state[‘label’]. We will use this to check if the prediction returned by client is valid in the future steps.
 4. We encoded the streaming data as JSON format and send it to the client one row by a time. The server will print ‘End of stream‘ when all data had been sent.
 5. We use the <ListenToClient> function to receive the predictions returned by the client side. At the meantime, we show how many records we correctly predicted and the accuracy rate so far. 
 6. The check variable stores if previous prediction is correct/incorrect. The server will send back this information to client on the next stream.

## Client Side Implementation
 1. Received predictor data as a dictionary
 2. Use random forest model to predict current action and print out the result
 3. Starting from second received information, client will adjust previous prediction according to server response for previous prediction, and global variable <correct> will count accurate predictions.
 4. In the meantime, <action_warning> function and global variable <current_act> and  <times> will track if user repeats the same action for more than 5 times. If yes, the client will print out the healthy warning message to notify user.
 5. Finally, after finishing the last prediction, client will calculate the accuracy rate of all predictions and print it out. This will be a crucial indication of our model’s performance.



* Link to our Kaggle publication page - https://www.kaggle.com/abbyding/motion-sensor-technology-tcp-socket-programming

