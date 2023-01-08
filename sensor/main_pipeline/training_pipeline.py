from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.exceptions import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact
import sys
from sensor.pipeline_components.A_data_ingestion_component import DataIngestioncomponent

class TrainPipeline:

    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()

        self.training_pipeline_config=training_pipeline_config
        self.data_ingestion_config=DataIngestionConfig(
            training_pipeline_config=training_pipeline_config)

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Starting Data ingestion")
            
            data_ingestion=DataIngestioncomponent(
                data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact=data_ingestion.main_initiate_data_ingestion()
            
            
            logging.info(f"Data ingestion is complete and aritifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_data_validation(self):
        try:
            logging.info("Starting Data Validation")
            logging.info("Data Validation is complete")
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_transformation(self):
        try:
            logging.info("Starting Data transformation")
            logging.info("Data transformation is complete")
        except Exception as e:
            raise SensorException(e,sys)
    def start_model_trainer(self):
        try:
            logging.info("Starting model trainer")
            logging.info("Model trainer is complete")
        except Exception as e:
            raise SensorException(e,sys)
    def start_model_evaluation(self):
        try:
            logging.info("Starting model evaluation")
            logging.info("Model evaluation is complete")
        except Exception as e:
            raise SensorException(e,sys)
    def start_model_pusher(self):
        try:
            logging.info("Starting Model Pusher")
            logging.info("Model Pusher is complete")
        except Exception as e:
            raise SensorException(e,sys)



    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact=self.start_data_ingestion()
            # self.start_data_validation()
            # self.start_data_transformation()
            # self.start_model_trainer()
            # self.start_model_evaluation()
            # self.start_model_pusher()
        except Exception as e:
            raise SensorException(e,sys)
