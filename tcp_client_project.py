import socket
import sys

HOST, PORT = "localhost", 9998
# data = " ".join(sys.argv[1:])
#list_numbers=[]

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    cnt = 0
    while cnt<10:

        print(cnt)
        received = str(sock.recv(1024), "utf-8")
        print(received)
        sock.send('{"label": "0"}'.encode("utf-8"))
        cnt += 1
    #sock.close()
    #list_numbers.append(int(received))
    #print(sum(list_numbers)/len(list_numbers))