from sensor.exceptions import SensorException
from sensor.logger import logging
import os, sys
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData
from sensor.constants.database import DATABASE_NAME
from sklearn.model_selection import train_test_split

class DataIngestioncomponet:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise SensorException(e,sys)


    def export_data_into_feature_store(self,):
        """
        Export mongo db collection record as dataframe into feature store
        """
        try:
            logging.info("export_data_into_feature_store started")
            sensor_data=SensorData()
            dataframe=sensor_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
                )
            
            feature_store_file_path= self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)

            return dataframe
            
            
            
            logging.info("export_data_into_feature_store completed")
        except Exception as e:
            raise SensorException(e,sys)

    def split_data_as_train_test(self,data_frame)->None:
        """
        Exported data from feature store will be split into train and test file
        """
        try:
            logging.info("split_data_as_train_test started")
            logging.info("split_data_as_train_test completed")
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_ingestion(self,)->DataIngestionArtifact:
        try:
            logging.info("Data ingestion initiated")
            dataframe=self.export_data_into_feature_store()
            self.split_data_as_train_test(data_frame=dataframe)
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path)
            logging.info("Data Ingestion initiation completed")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)