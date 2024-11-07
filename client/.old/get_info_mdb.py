from PyLibreHardwareMonitor import Computer
from time import sleep
import pymongo
import datetime

# MongoDB Conn
url = 'mongodb+srv://pvAnlizz:2704HwrvPL3eJoLL@srvdev.nn96g.mongodb.net/?retryWrites=true&w=majority&appName=srvdev'
client = pymongo.MongoClient(url)
db = client['pcAnlizz']

# Get user info
user_collection = db['user']
id_user = user_collection.find_one({"username":"lucasphill"})
user = {
    "$ref": "user", 
    "$id": id_user['_id'], 
    "$db": "pcAnlizz", 
}

# Get data and insert into MongoDB
pc_collection = db['pc_data']
while True:
    computer = Computer()
    data = {
            "user": user, 
            "timestamp": datetime.datetime.now(),
            "cpu": computer.cpu, 
            "gpu":computer.gpu,
            "memory":computer.memory,
            "network":computer.network,
            "storage":computer.storage,
            "motherboard":computer.motherboard,
            "controller":computer.controller,
    }
    pc_collection.insert_one(data)
    print(datetime.datetime.now())
    sleep(60)