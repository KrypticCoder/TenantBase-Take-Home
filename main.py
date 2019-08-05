import sys
import socket
import threading
import requests 
from flask import Flask, request, json, render_template
from flask_cors import CORS
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_socketio import SocketIO, emit
from multiprocessing import Process

flask_port = 8000
memcached_port = 11211

app = Flask(
    __name__, 
    static_folder="build/static", 
    template_folder="build"
)

socketio = SocketIO(app)
Base = declarative_base()
Session = sessionmaker()

class Item(Base):
    __tablename__ = 'item'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    key = Column(String(250))
    value = Column(String(250))

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def toJSON(self):
        return {"key": self.key, "value": self.value}

class Memcached(threading.Thread):
    def __init__(self, tup):
        self.socket = tup[0]
        self.address = tup[1]
        threading.Thread.__init__(self)

    def run(self): 
        while(True):
            data = decode(self.socket.recv(1024))
            args = data.split(" ")

            command = args[0]
            num_args = len(args)

            if command == 'get':
                if num_args != 2:
                    self.socket.send(encode('ERROR'))
                else:
                    command, key = args
                    result = getItem(key)

                    if result:
                        self.socket.send(encode('VALUE ' + str(key) + ' 1 ' + str(len(result))))
                        self.socket.send(encode(result))
                    
                    self.socket.send(encode('END'))

            elif command == 'set':
                if num_args != 5:
                    self.socket.send(encode('ERROR'))
                else:
                    command, key, flag, expiry, length = args
                    value = decode(self.socket.recv(1024))
                    
                    if len(value) != int(length):
                        self.socket.send(encode('CLIENT_ERROR bad data chunk'))
                        self.socket.send(encode('ERROR'))
                    else:
                        result = setItem(key, value)
                        if result:
                            self.socket.send(encode('STORED'))
                            sendGetEvent()
                        else:
                            self.socket.send(encode('ERROR'))

            elif command == 'delete':
                if num_args != 2:
                    self.socket.send(encode('ERROR'))
                else:
                    command, key = args
                    result = deleteItem(key)
                    
                    if result:
                        self.socket.send(encode('DELETE'))
                        sendGetEvent()
                    else:
                        self.socket.send(encode('NOT FOUND'))

            else:
                self.socket.send(encode('ERROR'))

        self.socket.close()

def getItem(key=None):
    session = Session()

    # get single item
    if key:
        item = session.query(Item).filter_by(key=key).first()
        return item.value if item else None

    # Return all items to client
    else:
        result = session.query(Item).all()
        items = [item.toJSON() for item in result]
        return items

def setItem(key, value):
    session = Session()

    if key:
        item = session.query(Item).filter_by(key=key).first()

        if item:
            item.value = value
            session.add(item)
            session.commit()
            return True
        else:
            item = Item(key=key, value=value)
            session.add(item)
            session.commit()
            return True
    else:
        return False

def deleteItem(key):
    session = Session()

    if key:
        item = session.query(Item).filter_by(key=key).first()
        if item:
            session.delete(item)
            session.commit()
            return True
        else:
            return False
        
    else:
        return False

def encode(msg):
    msg += '\n'
    return msg.encode('utf-8')

def decode(msg):
    return msg.decode('utf-8').strip("\r\n")

def sendGetEvent():
    endpoint = 'http://127.0.0.1:%s/get' % flask_port
    requests.get(endpoint)

@socketio.on('connect')
def connect():
    items = getItem()
    emit('return_items', {'items': items})

@app.route("/get")
def getItems():
    items = getItem()
    socketio.emit('return_items', {'items': items})
    return 'ok'

@app.route("/")
def index():
    return render_template('index.html')

def runFlask():
    print('Starting app on port %s' % flask_port)
    socketio.run(app, port=flask_port)

def runMemcached():
    print('Starting memcached server on port %s' % memcached_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', memcached_port))
    s.listen(1)

    while True:
        Memcached(s.accept()).start()

def main():
    if (len(sys.argv) < 2):
        print("Missing required parameters >>> python <main.py> <database.sqlite>")
        return

    db_name = sys.argv[1]
    engine = create_engine('sqlite:///' + db_name)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

    Process(target=runFlask).start()
    Process(target=runMemcached).start()

if __name__ == '__main__': main()