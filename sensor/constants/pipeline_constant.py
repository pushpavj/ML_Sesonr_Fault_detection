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
SCHEMA_FILE_PATH=os.path.join("lookup_info","schema_file.yaml")

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


"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"

DATA_VALIDATION_VALID_DIR: str = "validated"

DATA_VALIDATION_INVALID_DIR: str = "invalid"

DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"

DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "Drift_report_file.yaml"

"""
Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME
"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"

DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"

DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"

MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"

MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"

MODEL_TRAINER_EXPECTED_SCORE: float = 0.6

MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("lookup_info", "model_info_file.yaml")
"""
MODEL Evauation related constant start with MODEL_EVALUATION var name
"""

MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02

MODEL_PUSHER_BUCKET_NAME = TRAINING_BUCKET_NAME

MODEL_PUSHER_S3_KEY = "model-registry"
