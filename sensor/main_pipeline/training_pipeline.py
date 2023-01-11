from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, \
        DataValidationConfig
from sensor.exceptions import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import sys
from sensor.pipeline_components.A_data_ingestion_component import DataIngestioncomponent
from sensor.pipeline_components.B_data_validation_component import DataValidationcomponent

class TrainPipeline:

    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()

        self.training_pipeline_config=training_pipeline_config
        self.data_ingestion_config=DataIngestionConfig(
            training_pipeline_config=training_pipeline_config)
        self.data_validation_config = DataValidationConfig()

        # self.data_transformation_config = DataTransformationConfig()

        # self.model_trainer_config = ModelTrainerConfig()

        # self.model_evaluation_config = ModelEvaluationConfig()

        # self.model_pusher_config = ModelPusherConfig()

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
    
    def start_data_validation(self,data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        try:
            logging.info("Starting Data Validation")
            data_validation = DataValidationcomponent(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            data_validation_artifact = data_validation.main_initiate_data_validation()

            logging.info("Performed the data validation operation")
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
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)                      # self.start_data_transformation()
            # self.start_model_trainer()
            # self.start_model_evaluation()
            # self.start_model_pusher()
        except Exception as e:
            raise SensorException(e,sys)
