import sys

from sensor.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
                           
from sensor.entity.config_entity import ModelPusherConfig,ModelEvaluationConfig
from sensor.exceptions import SensorException
from sensor.logger import logging
from sensor.ml_customized_modules.cust_model.s3_estimator import SensorEstimator
import os
import shutil


class ModelPusher:
    def __init__(self,
        model_pusher_config:ModelPusherConfig,
        model_evaluation_artifact:ModelEvaluationArtifact
    ):
        self.model_pusher_config = model_pusher_config
        self.model_evaluation_artifact = model_evaluation_artifact

        # self.sensor_estimator = SensorEstimator(
        # # bucket_name=self.model_pusher_config.bucket_name,
        # # model_path=self.model_pusher_config.s3_model_key_path,
        # )

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            logging.info("Uploading artifacts folder to s3 bucket")
            trained_model_path = self.model_evaluation_artifact.trained_model_path
            
            #Creating model pusher dir to save model
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)

            #saved model dir
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)

            #prepare artifact
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path, model_file_path=model_file_path)
            
            logging.info("Uploaded artifacts folder to s3 bucket")

            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")

            logging.info("Exited initiate_model_pusher method of ModelTrainer class")

            return model_pusher_artifact

        except Exception as e:
            raise SensorException(e, sys) from e
