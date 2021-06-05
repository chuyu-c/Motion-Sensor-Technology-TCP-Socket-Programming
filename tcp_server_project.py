#!/usr/bin/env python3

import socket
import threading
import csv
import json
import argparse
import sys
import time
import datetime


class ThreadedServer(object):
    def __init__(self, host, opt):
        self.device = {}
        self.device['NoMode'] = {'points': 0}
        self.device['label'] = {'label': 0, 'points': 0}
        self.host = host
        self.port = opt.port
        self.opt = opt
        self.state = self.device[opt.mode if opt.mode else 'NoMode']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.lock = threading.Lock()

    def listen(self):
        self.sock.listen(5) # server prepares a queue of 5
        while True:
            client, address = self.sock.accept()
            print(f'Connection from {address} has been established! ')
            client.settimeout(500)
            threading.Thread(target=self.listenToClient, args=(client, address)).start()
            threading.Thread(target=self.sendStreamToClient, args=
            (client, self.sendCSVfile())).start()

    def handle_client_answer(self, obj):
        if self.opt.mode is not None and self.opt.mode == 'label':

            if 'label' not in obj:
                return
            self.lock.acquire()
            if self.state['label'] == int(obj['label']):
                self.state['points'] += 1
            self.lock.release()
        return

    def listenToClient(self, client, address):
        size = 1024
        total = 0
        while True:
            try:
                data = client.recv(size).decode()

                if data:
                    # Set the response to echo back the recieved data

                    a = json.loads(data.rstrip('\n\r '))
                    self.handle_client_answer(a)
                    total += 1
                    print(f"Correctly predicted: {self.state['points']} records.")
                    print(f"Rate: {self.state['points']/total}")
                    # client.send(response)
                else:
                    print('Client disconnected')
                    return False
            except:
                print(f"so far we have {self.state['points']} points")
                print('Client closed the connection')
                print("Unexpected error:", sys.exc_info()[0])
                client.close()
                return False

    def handleCustomData(self, buffer):
        if self.opt.mode is not None and self.opt.mode == 'label':
            self.lock.acquire()
            #buffer['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.state['label'] = int(buffer['label'])
            buffer['label'] = 0   # NEED FUTURE WORKS!!!
            self.lock.release()

    def sendStreamToClient(self, client, buffer):
        for i in buffer:
            print(i)
            self.handleCustomData(i)
            try:
                client.send((self.convertStringToJSON(i) + '\n').encode('utf-8'))
                time.sleep(self.opt.interval)
            except:
                print('End of stream')
                return False
        client.send((self.convertStringToJSON(self.state) + '\n').encode('utf-8'))
        return False

    def convertStringToJSON(self, st):
        return json.dumps(st)

    def sendCSVfile(self):
        out = []
        for f in self.opt.files:
            print('reading file %s...' % f)
            csvfile = open(f, 'r')
            reader = csv.DictReader(csvfile)
            for row in reader:
                out += [row]
        return out


if __name__ == "__main__":

    parser = argparse.ArgumentParser(usage='python tcp_server_project.py -p 9998 -f training.csv -t 1 -m label')
    #parser = argparse.ArgumentParser(usage='usage: tcp_server -p port [-f -m]')
    #parser = argparse.ArgumentParser(usage='usage: tcp_server.py -p 9998 -f occupancy/censortraining.csv -t 1')
    parser.add_argument('-f', '--files', nargs='+')
    parser.add_argument("-m", "--mode", action="store", dest="mode")
    parser.add_argument("-p", "--port", action="store", dest="port", type=int)
    parser.add_argument("-t", "--time-interval", action="store",
                        dest="interval", type=int, default=1)


    opt = parser.parse_args()
    #host = opt.host
    #port = opt.port
    if not opt.port:
        parser.error('Port not given')
    ThreadedServer('localhost', opt).listen()

'''
{"wrist": "0", "acceleration_x": "0.265", "acceleration_y": "-0.7814", "acceleration_z": "-0.0076",
"gyro_x": "-0.059", "gyro_y": "0.0325", "gyro_z": "-2.9296", "label": "0"}

{"CO2": "760.4", "Temperature": "23.718", "Light": "578.4", "Number": "141",
"Occupancy": "1", "Humidity": "26.29", "HumidityRatio": "0.00477266099212519",
"date": "2015-02-02 14:19:59"}
https://zhuanlan.zhihu.com/p/64893344
https://levelup.gitconnected.com/face-recognition-socket-programming-and-multithreading-in-python-6f9717fa2864
'''