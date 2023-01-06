from sensor.configuration.mongodb_conection import MongoDBClient

if __name__=='__main__':
    mongdb_client=MongoDBClient()
    print(mongdb_client.database.list_collection_names())