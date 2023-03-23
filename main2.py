from sensor.configuration.mongodb_conection_config import MongoDBClientConnection
from sensor.exceptions import SensorException
import os, sys
from sensor.logger import logging
from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from sensor.main_pipeline.training_pipeline import TrainPipeline
from sensor.configuration.mongodb_conection_config import MongoDBClientConnection



from sensor.main_pipeline import training_pipeline
from sensor.utilities.utility_codes import util_read_yaml_file
from sensor.constants.pipeline_constant import SAVED_MODEL_DIR
from fastapi import FastAPI
from sensor.constants.application_constants import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.ml_customized_modules.cust_model.customized_estimator import ModelResolver,CustTargetValueMapping
from sensor.utilities.utility_codes import util_load_object
from fastapi.middleware.cors import CORSMiddleware

if __name__=='__main__':
    train_pipeline=TrainPipeline()
    train_pipeline.run_pipeline()
