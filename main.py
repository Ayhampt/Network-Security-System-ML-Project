from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import customException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Starting data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(data_ingestion_artifact)
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(
            data_validation_config, data_ingestion_artifact
        )
        logging.info("Initiate the data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("data Validation Completed")
        print(data_validation_artifact)
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        logging.info("data Transformation started")
        data_transformation = DataTransformation(
            data_validation_artifact, data_transformation_config
        )
        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )
        print(data_transformation_artifact)
        logging.info("data Transformation completed")

        logging.info("Initiating Model Trainer")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact,
        )
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("model trainer artifact created")
        logging.info("Model Trainer completed")
    except Exception as e:
        raise customException(e, sys)
