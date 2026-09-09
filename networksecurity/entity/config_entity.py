from datetime import datetime
import os

from networksecurity.constant import training_pipeline


class TrainingPipelineConfig:
    def __init__(self, timestamp: datetime = None):
        if timestamp is None:
            timestamp = datetime.now()
        self.pipeline_name = "networkSecurity"
        self.timestamp: str = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # constants from training_pipeline
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.train_test_split_ratio = (
            training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        )

        # build directories under the run-specific artifact dir
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME,
        )
        self.feature_store_dir = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR
        )
        self.ingested_dir = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR
        )

        # file paths
        self.training_file_path = os.path.join(
            self.ingested_dir, training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path = os.path.join(
            self.ingested_dir, training_pipeline.TEST_FILE_NAME
        )


class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.validation_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME,
        )
        self.valid_data_dir = os.path.join(
            self.validation_dir, training_pipeline.VALID_DATA_DIR
        )
        self.invalid_data_dir = os.path.join(
            self.validation_dir, training_pipeline.INVALID_DATA_DIR
        )
        self.valid_train_file_path = os.path.join(
            self.valid_data_dir, training_pipeline.VALID_TRAIN_FILE_NAME
        )
        self.valid_test_file_path = os.path.join(
            self.valid_data_dir, training_pipeline.TEST_FILE_NAME
        )
        self.invalid_train_file_path = os.path.join(
            self.invalid_data_dir, training_pipeline.INVALID_TRAIN_FILE_NAME
        )
        self.invalid_test_file_path = os.path.join(
            self.invalid_data_dir, training_pipeline.TEST_FILE_NAME
        )
        self.drift_report_dir = os.path.join(
            self.validation_dir, training_pipeline.DRIFT_REPORT_DIR_NAME
        )
        self.drift_report_file_path = os.path.join(self.drift_report_dir, "report.yaml")


class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMATION_DIR_NAME,
        )
        self.transformed_train_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),
        )
        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"),
        )
        self.transformed_object_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,
        )


class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.MODEL_TRAINER_DIR_NAME,
        )
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir,
            training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
            training_pipeline.MODEL_TRAINER_MODEL_FILE_NAME,
        )
        self.expected_score: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold: float = (
            training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD
        )
