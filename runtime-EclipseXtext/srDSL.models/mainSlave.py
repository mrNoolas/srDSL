from utils import utils
from vitals import vitals
from checkColor import checkColor
from movement import movement
from threading import Thread
from doMovements import doMovements
from time import sleep
from receiveMessage import receiveMessage

import bluetooth

server_mac = 'CC:78:AB:50:B2:46'

def main():
    u = utils()
    v = vitals(u)
    m = movement(v, u) 
    
    move = doMovements(v,m)
    c = checkColor(u)
    r = receiveMessage(u, c)

    behaviors = [move,r,c]   
    runBluetooth(behaviors)
    print("Shutting down...")
    return 0
    
def connect():
    port = 3
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print('Connecting...')
    sock.connect((server_mac, port)) 
    print('Connected to ', server_mac)
    return sock, sock.makefile('r'), sock.makefile('w')

def runBluetooth(behaviors):
    sock, sock_in, sock_out = connect()
    listener = Thread(target=listen, args=(sock_in, sock_out, behaviors))
    listener.start()
    sender = Thread(target=send, args=(sock_in, sock_out, behaviors))
    sender.start()
    Thread(target=go, args=[behaviors]).start()
    Thread(target=doAction, args=[behaviors]).start()
    while not behaviors[2].foundAllColors:
        sleep(1)
        
    sock_out.close()
    sock_in.close()
    sock.close()

def listen(sock_in, sock_out, behaviors):
    print('SLAVE: Now listening...')
    while not behaviors[2].foundAllColors:
        data = int(sock_in.readline())
        print('SLAVE: Received ' + str(data))
        behaviors[1].receivedColor = data
        behaviors[1].user = "Slave"
        behaviors[1].receivedMessage = True
            
def send(sock_in, sock_out, behaviors):
    while not behaviors[2].foundAllColors:
        if behaviors[2].readyToSend:
            print('SLAVE: Ready to send!')
            sock_out.write(str(behaviors[2].lastColor) + '\n')
            sock_out.flush()
            print('SLAVE: Sent ' + str(behaviors[2].lastColor))
            behaviors[2].readyToSend = False
        
def go(behaviors):
    activeBehavior = 0 #Standard = movement
    highest = 0 #Standard = movement
    behaviors[highest].active = True
    while not behaviors[2].foundAllColors: 
        #print("SLAVE: Current running behavior " + str(activeBehavior))
        #print("Colors to be checked:")
        #print(behaviors[1].colorsToFind)
        for i in range(len(behaviors)-1, -1, -1):
            if i > activeBehavior:
                if behaviors[i].takeControl() and behaviors[activeBehavior].active:
                    print("SLAVE: Behavior " + str(i) + " wants to take control!")
                    print("SLAVE: Suppressing behavior " + str(activeBehavior))
                    behaviors[activeBehavior].suppress()
                    print("SLAVE: Starting behavior " + str(i))
                    behaviors[i].suppressed = False
                    behaviors[i].active = True
                    activeBehavior = i
            elif not behaviors[activeBehavior].active:
                #No behavior is running, thus the highest can be started. 
                if behaviors[i].takeControl():
                    #print("SLAVE: Starting behavior " + str(i))
                    behaviors[i].suppressed = False
                    behaviors[i].active = True
                    activeBehavior = i
                    
        sleep(0.1)
                    
def doAction(behaviors):
    while not behaviors[2].foundAllColors:
        for i in range(len(behaviors)-1, -1, -1): 
            if behaviors[i].active:
                print("SLAVE: Thread runs behavior " + str(i))
                behaviors[i].action();
    
main()
