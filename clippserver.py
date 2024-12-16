#CT30A3401 Distributed Systems
#Practical assignment
#Name: Teemu Juura
#Studentnum: 0509164

import socket
import socketserver
import string
import datetime
from threading import Lock

HOST = '0.0.0.0'
PORT = 8080
clipboard = None
rwlock = Lock()

def respond(head, payload):
    '''Constructs the response'''
    resp = str(head) + str(payload)
    resp = bytes(resp, 'ascii')
    return resp


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class TCPHandler(socketserver.BaseRequestHandler):
    
      def handle(self):
        global clipboard
        buf = str(self.request.recv(1024), 'ascii')
        req = None

        if buf.startswith('set'):
            req = 'set'
            buf = buf[len('set'):]
            rwlock.acquire()
            clipboard = buf
            rwlock.release()
            response = respond('ok', '')
            
        elif buf.startswith('get'):
            req = 'get'
            if clipboard:
                response = respond('ok', clipboard)
            else:
                response = respond('ok', '')

        print("{} -- Handled {} request from {}:{}".format(datetime.datetime.now(), req, self.client_address[0],
self.client_address[1]))
        self.request.sendall(response)
        self.request.close()
            

def main():
    server = ThreadedTCPServer((HOST, PORT), TCPHandler)
    server.allow_reuse_address = True

    try:
        server.serve_forever()
    except KeyboardInterrupt as e:
        server.shutdown()


if __name__ == '__main__':
    main()
        
