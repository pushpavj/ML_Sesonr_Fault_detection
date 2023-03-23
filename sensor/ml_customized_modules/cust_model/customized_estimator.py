import sys,os

from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sensor.constants.pipeline_constant import SAVED_MODEL_DIR,MODEL_FILE_NAME

from sensor.exceptions import SensorException
from sensor.logger import logging


class CustTargetValueMapping:
    def __init__(self):
        self.neg: int = 0

        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()

        return dict(zip(mapping_response.values(), mapping_response.keys()))


class CustSensorModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        self.preprocessing_object = preprocessing_object

        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        logging.info("Entered predict method of SensorTruckModel class")

        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")

            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise SensorException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelResolver:

    def __init__(self,model_dir=SAVED_MODEL_DIR):
        try:
            self.model_dir=model_dir
        
        except Exception as e:
            raise e
    def get_best_model(self,):
        try:
            timestamps= list(map(int,os.listdir(self.model_dir)))
            latest_timestamp=max(timestamps)
            latest_model_path=os.path.join(self.model_dir,str(latest_timestamp),MODEL_FILE_NAME)
            return latest_model_path

        except Exception as e:
            raise e
    
    def is_model_exists(self):
        try:
            print("os.path.exists(self.model_dir)", os.path.exists(self.model_dir))
            if not os.path.exists(self.model_dir):
                return False

            timestamps=os.listdir(self.model_dir)
            if len(timestamps)==0:
                return False
            latest_model_path=self.get_best_model()
            print("latest_model_path", latest_model_path)
            if not os.path.exists(latest_model_path):
                return False
            return True
        except Exception as e:
            raise e



