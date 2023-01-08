import pymongo
from sensor.constants.database_constatnts import DATABASE_NAME
from sensor.constants.env_variables import *
import certifi
ca=certifi.where()

class MongoDBClientConnection:
    client=None
    def __init__(self,database_name=DATABASE_NAME)->None:
        try:
            if MongoDBClientConnection.client is None:
                #mongo_db_url=os.getenv(MONGODB_URL_KEY)
                mongo_db_url="mongodb://localhost:27017/"
                #mongo_db_url="mongodb+srv://pushpaVJ:Mongodb804000@cluster0.rxjr8.mongodb.net/?retryWrites=true&w=majority"
               # MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
                self.client=pymongo.MongoClient(mongo_db_url)
              #  self.client=MongoDBClient.client
                self.database=self.client[database_name]
                self.database_name=database_name
                
        except Exception as e:
            raise e
