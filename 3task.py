import zmq
import time
import sys
import random
from random import choice
import string
import multiprocessing
import logging
from multiprocessing import current_process
import threading

class Message:    
    
    def __init__(self):
        self.message = ''
        
    def generate_message(self):
        message = ''
        if int(str(self.identity)[-1]) % 2 == 0:            
            if self.counter %3 == 0:                
                chars = random.choices(string.ascii_lowercase, k=4)
                chars.insert(random.randrange(len(chars)+1), 'b')
                message= message.join(chars)
            else:                
                chars = random.choices(string.ascii_lowercase, k=5)
                message= message.join(chars)
        else:
            if self.counter %3 == 0:
                chars = random.choices(string.ascii_lowercase, k=4)
                chars.insert(random.randrange(len(chars)+1), 'a')
                message= message.join(chars)
            else:            
                chars = random.choices(string.ascii_lowercase, k=5)
                message= message.join(chars)           
        
        self.message = message
        
class ProcessLog:
    
    def __init__(self):    
        self.logger = logging.getLogger()
        formatter = logging.Formatter("%(asctime)s:%(message)s")    
        self.logger.setLevel(logging.INFO)    
        self.process_name = '%s' % current_process().name    
        filename = '{}.log'.format(str(self.process_name))
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

class ClientTask(threading.Thread, ProcessLog, Message):

    def __init__(self):
        self.process_id = ''
        self.counter = 0
        threading.Thread.__init__ (self)
        
    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        #socket = context.socket(zmq.REQ)
        self.identity = 'worker-%d' % (choice([1,2,3,4]))
        print("!!!!!!!!")
        print(int(str(self.identity)[-1]))
        socket.setsockopt_string(zmq.IDENTITY, self.identity )
        socket.connect("tcp://127.0.0.1:5001")
        print ('Client %s started' % (self.identity))
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        reqs = 0
        while True:
            for i in range(5):
                sockets = dict(poll.poll(1000))
                if socket in sockets:
                    if sockets[socket] == zmq.POLLIN:
                        msg = socket.recv()
                        print ('Client %s received: %s\n' % (self.identity, msg))
                        del msg
            reqs = reqs + 1
            print ('Req #%d sent..' % (reqs))
            Message.generate_message(self)
            msg = str(self.message)
            print(msg)
            socket.send_string(msg)
            self.counter += 1
            #socket.send_string('request #%d' % (reqs))
        socket.close()
        context.term()
        
        
class ServerTask(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__ (self)
    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5001')
        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')
        workers = []
        for i in range(5):
            worker = ServerWorker(context)
            worker.start()
            workers.append(worker)
        poll = zmq.Poller()
        poll.register(frontend, zmq.POLLIN)
        poll.register(backend,  zmq.POLLIN)
        while True:
            sockets = dict(poll.poll())
            if frontend in sockets:
                if sockets[frontend] == zmq.POLLIN:
                    _id = frontend.recv()
                    msg = frontend.recv()
                    print ('Server received %s id %s\n' % (msg, _id))
                    backend.send(_id, zmq.SNDMORE)
                    backend.send(msg)
            if backend in sockets:
                if sockets[backend] == zmq.POLLIN:
                    _id = backend.recv()
                    msg = backend.recv()
                    #print ('Sending to frontend %s id %s\n' % (msg, _id))
                    frontend.send(_id, zmq.SNDMORE)
                    frontend.send_string(msg.decode('utf-8'))
        frontend.close()
        backend.close()
        context.term()
        
class ServerWorker(threading.Thread):
    
    def __init__(self, context):
        threading.Thread.__init__ (self)
        self.context = context
    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        print ('Worker started')
        while True:
            _id = worker.recv()
            msg = worker.recv()
            #print ('Worker received %s from %s' % (msg, _id))            
            time.sleep(2)
            worker.send(_id, zmq.SNDMORE)
            worker.send_string(msg.decode('utf-8'))
            del msg
        worker.close()
def main():
    
    server = ServerTask()
    server.start()
    for i in range(2):
        client = ClientTask()
        client.start()
    server.join()
        
if __name__ == "__main__":
    main()