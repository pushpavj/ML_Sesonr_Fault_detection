import sys
from typing import Optional

import numpy as np
import pandas as pd

from sensor.configuration.mongodb_conection import MongoDBClient
from sensor.constants.database import DATABASE_NAME
from sensor.exceptions import SensorException
from sensor.logger import logging


class SensorData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """

    def __init__(self):
        """
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise SensorException(e, sys)

    # def export_collection_as_dataframe(
    #     self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
    #     try:
    #         """
    #         export entire collectin as dataframe:
    #         return pd.DataFrame of collection
    #         """
    #         if database_name is None:
    #             collection = self.mongo_client.database[collection_name]

    #         else:
    #             db=self.mongo_client.client[database_name]
    #             collection = db[collection_name]
    #         recs=collection.find()
    #        # rec=collection.find_one()
            
    #         l=[]
    #         for i in recs:
    #             l.append(i)
    #         print("recs***********",l)    
    #        # print(rec)
    #         df = pd.DataFrame(list(recs))

    #         if "_id" in df.columns.to_list():
    #             df = df.drop(columns=["_id"], axis=1)

    #         df.replace({"na": np.nan}, inplace=True)

    #         return df

    #     except Exception as e:
    #         raise SensorException(e, sys)

class SensorData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """

    def __init__(self):
        """
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise SensorException(e, sys)

    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None
    ) -> pd.DataFrame:
        try:
            """
            export entire collectin as dataframe:
            return pd.DataFrame of collection
            """
            if database_name is None:
                collection = self.mongo_client.database[collection_name]

            else:
                collection = self.mongo_client.client[database_name][collection_name]
            recs=collection.find()
            df = pd.DataFrame(list(collection.find()))
            print("DF*********",df)

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise SensorException(e, sys)


