from Networksecurity.components.data_ingestion import DataIngestion
from Networksecurity.components.data_validation import DataValidation
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logging
from Networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from Networksecurity.entity.config_entity import TrainingPipelineConfig
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

    except Exception as e:
        raise NetworkSecurityException(e, sys)
        