from datetime import datetime
import os
import os
from networksecurity.constant import training_pipeline


class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        self.piepline_name = "networkSecurity"
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)
        self.timestamp: str = timestamp


class DataIngestionConfig:
    def __init__(self, TrainingPipelineConfig: TrainingPipelineConfig):
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.train_test_split_ratio = (
            training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        )
        self.data_ingestion_dir = os.path.join(
            training_pipeline.ARTIFACT_DIR, training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_dir = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR
        )
        self.ingested_dir = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR
        )
