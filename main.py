from Networksecurity.components.data_ingestion import DataIngestion
from Networksecurity.components.data_validation import DataValidation
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logging
from Networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from Networksecurity.entity.config_entity import TrainingPipelineConfig
from Networksecurity.components.data_transformation import DataTransformation,DataTransformationConfig
import sys
import os


if __name__ == '__main__':
    try:
        TrainingPipelineConfig = TrainingPipelineConfig()
        dataingestioconfig = DataIngestionConfig(TrainingPipelineConfig)
        data_ingestion = DataIngestion(dataingestioconfig)
        logging.info('Initiate Data Ingestion')
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info('Data Ingestion is completed')
        print(dataingestionartifact)

        # Pass the correct object (dataingestionartifact) to DataValidation
        data_validation_config = DataValidationConfig(TrainingPipelineConfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info('Initiate Data Validation')
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info('Data Validation is completed')
        print(data_validation_artifact)
        data_transformation_config = DataTransformationConfig(TrainingPipelineConfig)
        logging.info("data Transformation started")
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("data Transformation completed")



    except Exception as e:
        raise NetworkSecurityException(e, sys)
        