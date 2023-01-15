from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, \
        DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from sensor.exceptions import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, \
    DataTransformationArtifact,ModelTrainerArtifact
import sys
from sensor.pipeline_components.A_data_ingestion_component import DataIngestioncomponent
from sensor.pipeline_components.B_data_validation_component import DataValidationcomponent
from sensor.pipeline_components.C_data_transformation_component import DataTransformationcomponent
from sensor.pipeline_components.D_model_trainer_component import ModelTrainercomponent
class TrainPipeline:

    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()

        self.training_pipeline_config=training_pipeline_config
        self.data_ingestion_config=DataIngestionConfig(
            training_pipeline_config=training_pipeline_config)
        self.data_validation_config = DataValidationConfig()

        self.data_transformation_config = DataTransformationConfig()

        self.model_trainer_config = ModelTrainerConfig()

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
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact
    ) -> DataTransformationArtifact:
        try:
            logging.info("Starting Data transformation")
            data_transformation = DataTransformationcomponent(
                data_validation_artifact, self.data_transformation_config
            )

            data_transformation_artifact = (
                data_transformation.main_initiate_data_transformation()
            )

            
            logging.info("Data transformation is complete")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys)
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact
    ) -> ModelTrainerArtifact:
        try:
            logging.info("Starting model trainer")
            model_trainer = ModelTrainercomponent(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = model_trainer.main_initiate_model_trainer()
            logging.info("Model trainer is complete")
            return model_trainer_artifact
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
            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact )
            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact
            )
            # self.start_model_evaluation()
            # self.start_model_pusher()
        except Exception as e:
            raise SensorException(e,sys)
