from sensor.configuration.mongodb_conection import MongoDBClient
from sensor.exceptions import SensorException
import os, sys
from sensor.logger import logging
from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig

if __name__=='__main__':

    training_pipeline_config=TrainingPipelineConfig()
    data_ingestion_config=DataIngestionConfig(training_pipeline_config)
    print(data_ingestion_config.__dict__)

    # mongdb_client=MongoDBClient()
    # print(mongdb_client.database.list_collection_names())