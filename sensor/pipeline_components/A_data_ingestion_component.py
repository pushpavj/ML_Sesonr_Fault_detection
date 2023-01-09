from sensor.exceptions import SensorException
from sensor.logger import logging
import os, sys
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_util_code.sensor_data_util import GetSensorData
from sklearn.model_selection import train_test_split

class DataIngestioncomponent:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise SensorException(e,sys)


    def sub_export_data_into_feature_store(self):
        """
        Export mongo db collection record as dataframe into feature store
        """
        try:
            logging.info("export_data_into_feature_store started")
            sensor_data=GetSensorData()
            dataframe=sensor_data.main_export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
                )
            
            feature_store_file_path= self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            logging.info("export_data_into_feature_store completed")
            return dataframe
            
            
            
            
        except Exception as e:
            raise SensorException(e,sys)

    def sub_split_data_as_train_test(self,data_frame)->None:
        """
        Exported data from feature store will be split into train and test file
        """
        try:
            logging.info("split_data_as_train_test started")
          
            train_set, test_set = train_test_split(
                data_frame, test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train test split on the dataframe")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            logging.info(f"Exported train and test file path.")

            logging.info("split_data_as_train_test completed")
        except Exception as e:
            raise SensorException(e,sys)

    def main_initiate_data_ingestion(self,)->DataIngestionArtifact:
        try:
            logging.info("Data ingestion initiated")
            dataframe=self.sub_export_data_into_feature_store()
            self.sub_split_data_as_train_test(data_frame=dataframe)

            data_ingestion_artifact=DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info("Data Ingestion initiation completed")

            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)