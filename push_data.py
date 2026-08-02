import os
import sys
import json

from dotenv import load_dotenv

load_dotenv()

mongodb_uri = os.getenv("MONGO_URI")
print(f"MongoDB URI: {mongodb_uri}")


import certifi

ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logger import logger
from networksecurity.exception.exception import CustomException

# ETL [extract , transform , Load]


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)

    def csv_to_json(self, csv_file_path):
        try:
            data = pd.read_csv(csv_file_path)
            data.reset_index(drop=True, inplace=True)
            records = json.loads(data.T.to_json()).values()
            return list(records)
        except Exception as e:
            raise CustomException(e, sys)

    def insert_data_to_mongodb(self, records, collection, database):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(mongodb_uri)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)

            return len(self.records)

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "NetworkSecurity"
    COLLECTION = "NetworkData"
    logger.info("Starting the data extraction process...")
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json(csv_file_path=FILE_PATH)
    logger.info(
        f"Data extraction process completed. {len(records)} records extracted from CSV file to json."
    )
    print(records)
    number_of_records = network_obj.insert_data_to_mongodb(
        records=records, collection=COLLECTION, database=DATABASE
    )
    logger.info(
        f"Data extraction process completed. {number_of_records} records inserted into MongoDB."
    )
    print(number_of_records)
