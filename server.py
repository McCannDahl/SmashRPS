import socket
import time
from threading import Thread

serversocket = socket.socket()
host = 'localhost'
port = 54545
clientsockets = []
t1 = None
t2 = None

serversocket.bind(('', port))
print('listening ("conrol + c" to stop)')

serversocket.listen()

def listen_for_connections():
    while True:
        clientsocket,addr = serversocket.accept()
        print("got a connection from %s" % str(addr))
        clientsockets.append(clientsocket)

def update_state():
    new_time = time.time()
    while True:
        old_time = time.time()
        t = old_time - new_time
        new_time = old_time
        # update state
        time.sleep(0.01)

def send_state():
    while True:
        for c in clientsockets:
            try:
                pass
                #c.send('update'.encode('ascii'))
            except:
                print('removing client')
                clientsockets.remove(c)
        time.sleep(0.01)

if __name__ == '__main__':
    t1 = Thread(target=listen_for_connections)
    t1.daemon = True
    t2 = Thread(target=update_state)
    t2.daemon = True
    t3 = Thread(target=send_state)
    t3.daemon = True
    t1.start()
    t2.start()
    t3.start()
    while True:
        time.sleep(10)