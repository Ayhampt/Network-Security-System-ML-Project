from networksecurity.exception.exception import customException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import sys
import os
import pymongo
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from typing import List

from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGODB_URI)


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise customException(e, sys) from e

    """
    Read data from MongoDB collection and export it as a DataFrame
    """

    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGODB_URI)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df = df.drop(columns=["_id"])
            df.replace({"nan": np.nan}, inplace=True)
            logging.info(
                f"Exporting collection: {collection_name} from database: {database_name}"
            )
            return df

        except Exception as e:
            raise customException(e, sys) from e

    """
    Export DataFrame to the feature store directory
    """

    def export_data_to_feature_store(self, df: pd.DataFrame):
        try:
            feature_store_dir = self.data_ingestion_config.feature_store_dir
            os.makedirs(feature_store_dir, exist_ok=True)
            feature_store_file_path = os.path.join(
                feature_store_dir, "feature_store.csv"
            )
            df.to_csv(feature_store_file_path, index=False, header=True)
            return df
        except Exception as e:
            raise customException(e, sys) from e

    """Train test split of the data and export it to the ingested directory"""

    def split_data_as_train_test(self, df: pd.DataFrame):
        try:
            train_test_split_ratio = self.data_ingestion_config.train_test_split_ratio
            ingested_dir = self.data_ingestion_config.ingested_dir
            os.makedirs(ingested_dir, exist_ok=True)

            train_set, test_set = train_test_split(
                df, train_size=train_test_split_ratio, random_state=42
            )
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True,
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True,
            )
            logging.info("Performed train test split")
            logging.info(
                f"Saved train data to {self.data_ingestion_config.training_file_path} and test data to {self.data_ingestion_config.testing_file_path}"
            )

        except Exception as e:
            raise customException(e, sys) from e

    """
    combining the above two methods to initiate data ingestion process
    """

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataframe_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )
            return dataframe_ingestion_artifact
        except Exception as e:
            raise customException(e, sys) from e
