from sensor.configuration.mongodb_conection_config import MongoDBClientConnection
from sensor.exceptions import SensorException
import os, sys
from sensor.logger import logging
from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from sensor.main_pipeline.training_pipeline import TrainPipeline
from sensor.configuration.mongodb_conection_config import MongoDBClientConnection
import pandas as pd


from sensor.main_pipeline import training_pipeline
from sensor.utilities.utility_codes import util_read_yaml_file
from sensor.constants.pipeline_constant import SAVED_MODEL_DIR,TARGET_COLUMN
from fastapi import FastAPI
from sensor.constants.application_constants import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.ml_customized_modules.cust_model.customized_estimator import ModelResolver,CustTargetValueMapping
from sensor.utilities.utility_codes import util_load_object,util_read_csv
from fastapi.middleware.cors import CORSMiddleware

env_file_path=os.path.join(os.getcwd(),"env.yaml")

def set_env_variable(env_file_path):

    if os.getenv('MONGO_DB_URL',None) is None:
        env_config = util_read_yaml_file(env_file_path)
        os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict")
async def predict_route():
    try:
        #get data from user csv file
        #conver csv file to dataframe

        df=None
        training_pipeline_config=TrainingPipelineConfig()
        Ingest_data=DataIngestionConfig(training_pipeline_config)
        test_data_path=Ingest_data.test_data_file_path
        data=util_read_csv(test_data_path)
        df=pd.DataFrame(data.iloc[1]).T
        df1=df.copy(deep=True)  
        print("columns", df.columns)
        df.drop(columns=TARGET_COLUMN, axis=1,  inplace=True)
        print("df",df)
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model()
        model = util_load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df1['predicted_column'] = y_pred
        df1['predicted_column'].replace(CustTargetValueMapping().reverse_mapping(),inplace=True)
        print("successfull")
        #decide how to return file to user.
        return Response(f"{df1.head()}")
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")

def main():
    try:
        set_env_variable(env_file_path)
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__=="__main__":
    #main()
    # set_env_variable(env_file_path)
    app_run(app, host=APP_HOST, port=APP_PORT)

#*********************************************************************************

# if __name__=='__main__':
#     train_pipeline=TrainPipeline()
#     train_pipeline.run_pipeline()



    # training_pipeline_config=TrainingPipelineConfig()
    # data_ingestion_config=DataIngestionConfig(training_pipeline_config)
    # print(data_ingestion_config.__dict__)

    # mongdb_client=MongoDBClient()
  
    # print(mongdb_client.database_name)
  #  print(mongdb_client.database.list_collection_names())
    
    #print(mongdb_client.database.list_collection_names()) #.list_collection_names())
