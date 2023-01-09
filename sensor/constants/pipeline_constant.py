import os
from sensor.constants.s3_bucket_constatnts import TRAINING_BUCKET_NAME



#defining common constant variables for training pipeline
TARGET_COLUMN="class"
PIPELINE_NAME:str="sensor"
ARTIFACT_DIR:str="artifacts"
FILE_NAME:str="sensor.csv"
TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

PREPROCESSING_OBJECT_FILE_NAME='preprocessing.pkl'
MODEL_FILE_NAME="model.pkl"
SCHEMA_FILE_PATH=os.path.join("config","schema.yaml")

SCHEMA_DROP_COLS = 'drop_columns'

#Data ingestion constants
DATA_INGESTION_COLLECTION_NAME:str="car"
DATA_INGESTION_DIR_NAME:str='data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested data"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float=0.2

DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_SCHEMA_DIR='schema.yaml'
DATA_VALIDATION_VALIDATED_DIR:str='validateddata'
DATA_VALIDATION_DRIFT_DIR:str="data_drift_reports"