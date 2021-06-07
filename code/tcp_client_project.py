import socket
import sys
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

# train the model
train_df=pd.read_csv(os.getcwd() + '/training.csv')
nt_df = train_df.copy()
Y = nt_df["label"]
X = nt_df.iloc[:,0:7]
train_x, test_x, train_y, test_y = train_test_split(X, Y,
                                                    train_size=0.7,
                                                    random_state=42)
def fit_model (model):
    classifier = model(n_estimators=100)  #train with default model parameters
    classifier.fit(train_x, train_y)
    return classifier

rf = fit_model(RandomForestClassifier)

HOST, PORT = "localhost", 9998
# data = " ".join(sys.argv[1:])
#list_numbers=[]

predict_list = []
current_act = 0
times = 0
# Create function to handle the received dictionary
def handle_dict_predcit(dct):
    values = list(dct.values())
    col = list(dct.keys())
    predict_df = pd.DataFrame([values])
    predict_df.columns = col
    return predict_df

def predict_rf(df, model):
    pred_cols = list(df.columns.values)[:-1]
    pred = model.predict(df[pred_cols])
    return int(pred)

def correct_error(indication):
    global predict_list
    if indication == 0:
        old = predict_list[-1]
        predict_list[-1] = abs(old-1)

def action_warning():
    global predict_list
    global current_act
    global times
    if current_act == predict_list[-1]:
        times += 1
    else:
        current_act = predict_list[-1]
        times = 1
    if times >= 2:
        if current_act == 1:
            print('You run over 2 times, you should try walk instead.')
        else:
            print('You walk over 2 times, you should try run instead.')

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    cnt = 0
    while cnt<50:

        print(cnt)
        received = str(sock.recv(1024), "utf-8")
        received = json.loads(received)
        # correct previous predict result if wrong
        if cnt > 0:
            indication = list(received.values())[-1]
            correct_error(indication)
            action_warning()
        print('predict_result', predict_list)
        predict_df = handle_dict_predcit(received)
        result = predict_rf(predict_df, rf)
        predict_list.append(result)
        predict_result = {'label': result}
        sock.send(json.dumps(predict_result).encode("utf-8"))
        cnt += 1
    #sock.close()
    #list_numbers.append(int(received))
    #print(sum(list_numbers)/len(list_numbers))

