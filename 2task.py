import psycopg2
from multiprocessing import Process
from multiprocessing import current_process
import string
import random
import threading
import schedule
import sched
import time
import logging
from time import sleep
import configparser

class Message:    
    
    def __init__(self):
        self.message = ''
        
    def generate_message(self, process_id, counter, message):                        
        if int(process_id) == 1:            
            if counter %3 == 0:                
                chars = random.choices(string.ascii_lowercase, k=4)
                chars.insert(random.randrange(len(chars)+1), 'b')
                message= message.join(chars)
            else:                
                chars = random.choices(string.ascii_lowercase, k=5)
                message= message.join(chars)
        elif int(process_id) == 2:
            if counter %3 == 0:
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
        
class Db(ProcessLog):

    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read('database.ini')
        db = {}
        if parser.has_section('postgresql'):
            params = parser.items('postgresql')
            for param in params:
                db[param[0]] = param[1]
        params = db
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()
        ProcessLog.__init__(self)
        self.cur.execute("CREATE TABLE IF NOT EXISTS poruke \
                        (process_id TEXT, message TEXT)")
        self.conn.commit()
        
    def insert_message(self, process_id, message):        
        self.cur.execute("INSERT INTO poruke VALUES(%s,%s)", \
                        (process_id, message))
        self.conn.commit()
        
    def search_message(self, process_id):
        if int(process_id) == 1:
            self.cur.execute("SELECT message FROM poruke WHERE \
                            process_id = '2'")
            poruke = self.cur.fetchall()
            lista = [poruka[0] for poruka in poruke]            
            if lista:
                for elem in lista:
                    if 'a' in elem:                        
                        self.logger.info(elem)
                    else:                        
                        self.logger.info("Procitana poruka ne sadrzi slovo a!")
            else:
                self.logger.info("Poruka nije pronadena!")
        elif int(process_id) == 2:
            self.cur.execute("SELECT message FROM poruke WHERE \
                            process_id = '1'")
            poruke = self.cur.fetchall()                
            lista = [poruka[-1] for poruka in poruke]
            if lista:
                for elem in lista:
                    if 'b' in elem:
                        self.logger.info(elem)
                    else:
                        self.logger.info("Procitana poruka ne sadrzi slovo b!")
            else:
                self.logger.info("Poruka nije pronadena!")

class MyProcess(Message, Db, ProcessLog):
	logging.basicConfig(level=logging.INFO, filename="CentralLog.log", 
                        format="%(asctime)s:%(message)s")
	def __init__(self):
		self.process_id = ''
		self.counter = 0
		Process(target=self.work, args=(self.process_id, \
                                                self.counter)).start()
		
	def work(self, process_id, counter):
		scheduler = sched.scheduler(time.time, time.sleep)
		Db.__init__(self)
		Message.__init__(self)
		_id = self.process_name
		self.process_id = _id[-1]
		message=''
		while True:
			Db.search_message(self, self.process_id)
			#scheduler.enter(3, 1, Message.generate_message(self, self.process_id, self.counter, message))
			#scheduler.run()
			Message.generate_message(self, self.process_id, \
                                                self.counter, message)
			#print(self.message)
			Db.insert_message(self, self.process_id, self.message)
			self.counter += 1
			sleep(1)

if __name__ == '__main__':
     
    
    p1 = MyProcess()
    p2 = MyProcess()
    
#conn.close()