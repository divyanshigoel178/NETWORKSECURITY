from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TrainingPipelineConfig, DtaIngestionConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys


import sys
if __name__=="__main__":
    try:
        trainingPipelineConfig=TrainingPipelineConfig()
        dataingestionconfig=DtaIngestionConfig(trainingPipelineConfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Starting data ingestion")
        data_ingestion.initiate_data_ingestion()
        print("Data ingestion completed successfully")
        logging.info("Data ingestion completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)    

