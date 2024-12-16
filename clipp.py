#CT30A3401 Distributed Systems
#Practical assignment
#Name: Teemu Juura
#Studentnum: 0509164

import sys
import socket
import string
import pyperclip
import time
import threading
from config import *

def sock_conn(msg, server, port, socket):
    resp = ''
    socket.connect((server, port))
    socket.sendall(msg)
    resp = data = str(socket.recv(1024), 'ascii')
    return resp

def send_recv(msg, server, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return sock_conn (msg, server, port, s)


def parse(resp):
    '''Parses the responce'''
    head = None
    if resp.startswith('ok'):
        head = 'ok'
    elif resp.startswith('Err'):
        head = 'Err'
    else:
        print('NO responce')

    resp = resp[len(head):]
    return(head, resp)
    

def getclip(server,port):
    '''Pulls clipboard contents from server'''
    req = 'get'
    req = bytes(req,'ascii')
    resp = send_recv(req, server, port)
    head, payload = parse(resp)
    return payload

class ClipWatcher(threading.Thread):
    '''Listener for changes in clipboard between server and client'''
    def __init__(self,server, port):
        super(ClipWatcher, self).__init__()
        self._server = server
        self._port = port
        self._stop = False
        
    def run(self):
        while not self._stop:
            current = pyperclip.paste()
            sval = getclip(self._server,self._port)
            if current != sval:
                pyperclip.copy(sval)
                print("Copied " + sval + " to clipboard" )
            time.sleep(5)
            
    def stop(self):
        self._stop = True
           

def setclip(server, port):
    '''Pushes clipboard contents to server'''
    contents = pyperclip.paste()
    req = 'set'+ contents
    req = bytes(req, 'ascii')
    resp = send_recv(req, server, port)
    head, payload = parse(resp)

        

def main():
   
    watcher = ClipWatcher(server,port)
    watcher.start()
    prev =""
    while True:
        ''''Listen for changes in clipboard contents'''
        try:
             current = pyperclip.paste()
             if current != prev:
                 prev = current
                 if current != "":
                     setclip(server, port)
             time.sleep(1)
        except KeyboardInterrupt as e:
            watcher.stop()
            break
        
     
       
if __name__ == '__main__':
    main()
        
