from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, \
        DataValidationConfig, DataTransformationConfig,                               \
        ModelTrainerConfig, ModelEvaluationConfig,ModelPusherConfig
from sensor.exceptions import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, \
    DataTransformationArtifact,ModelTrainerArtifact, ModelEvaluationArtifact,ModelPusherArtifact
import sys
from sensor.pipeline_components.A_data_ingestion_component import DataIngestioncomponent
from sensor.pipeline_components.B_data_validation_component import DataValidationcomponent
from sensor.pipeline_components.C_data_transformation_component import DataTransformationcomponent
from sensor.pipeline_components.D_model_trainer_component import ModelTrainercomponent
from sensor.pipeline_components.E_model_evaluation_component import ModelEvaluationcomponent
from sensor.pipeline_components.F_model_pusher_component import ModelPusher
from sensor.constants.s3_bucket_constatnts import TRAINING_BUCKET_NAME
from sensor.constants.pipeline_constant import SAVED_MODEL_DIR
from sensor.cloud_storage.s3_syncer import S3Sync

class TrainPipeline:
    is_pipeline_running=False
    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()

        self.training_pipeline_config=training_pipeline_config
        self.data_ingestion_config=DataIngestionConfig(
            training_pipeline_config=training_pipeline_config)
        self.data_validation_config = DataValidationConfig()

        self.data_transformation_config = DataTransformationConfig()

        self.model_trainer_config = ModelTrainerConfig()

        self.model_evaluation_config = ModelEvaluationConfig()

        self.model_pusher_config = ModelPusherConfig(training_pipeline_config=training_pipeline_config)

        self.s3_sync = S3Sync()

       
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
    def start_model_evaluation(
        self,
        data_validation_artifact: DataValidationArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
    ) -> ModelEvaluationArtifact:
        
        try:
            logging.info("Starting model evaluation")
            model_evaluation = ModelEvaluationcomponent(
                model_eval_config=self.model_evaluation_config,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact,
            )

            model_evaluation_artifact = model_evaluation.main_initiate_model_evaluation()

            logging.info("Model evaluation is complete")
            return model_evaluation_artifact
            
        except Exception as e:
            raise SensorException(e,sys)
    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            logging.info("Starting Model Pusher")
            
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher( model_pusher_config,model_evaluation_artifact,)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info("Model Pusher is complete")
            return model_pusher_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def sync_artifact_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_buket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)
            
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder = SAVED_MODEL_DIR,aws_buket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)


    def run_pipeline(self):
        
        try:
            TrainPipeline.is_pipeline_running=True
            data_ingestion_artifact:DataIngestionArtifact=self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)                      # self.start_data_transformation()
            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact )
            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact
            )
            model_evaluation_artifact = self.start_model_evaluation(
                data_validation_artifact, model_trainer_artifact,
            )
            if not model_evaluation_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact)
            TrainPipeline.is_pipeline_running=False
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
        except  Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainPipeline.is_pipeline_running=False
            raise  SensorException(e,sys)