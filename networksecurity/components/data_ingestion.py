from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DtaIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import sys
import os
import pymongo
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:

    def __init__(self, data_ingestion_config: DtaIngestionConfig):
        try:
            logging.info("Initializing DataIngestion component")
            self.data_ingestion_config = data_ingestion_config
            logging.info(f"DataIngestionConfig Loaded: {data_ingestion_config}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # --------------------------------------------------------
    def export_collection_as_dataframe(self):
        """Reads MongoDB collection and converts to DataFrame"""
        try:
            logging.info("Exporting collection as DataFrame from MongoDB")

            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            logging.info(f"Connecting to MongoDB: DB={database_name}, Collection={collection_name}")

            mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            logging.info(f"Total records fetched from MongoDB: {df.shape[0]}")

            if "_id" in df.columns:
                logging.info("Dropping MongoDB '_id' column")
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            logging.info("DataFrame exported successfully from MongoDB")

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # --------------------------------------------------------
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            logging.info("Saving DataFrame to feature store")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Created directory for feature store: {dir_path}")

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Feature store file saved at: {feature_store_file_path}")

            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # --------------------------------------------------------
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            logging.info("Starting train-test split")

            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Train-test split completed")
            logging.info(f"Train Shape: {train_set.shape}, Test Shape: {test_set.shape}")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Saving train and test files")

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(f"Train file saved at: {self.data_ingestion_config.training_file_path}")
            logging.info(f"Test file saved at: {self.data_ingestion_config.testing_file_path}")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # --------------------------------------------------------
    def initiate_data_ingestion(self):
        try:
            logging.info("===== Data Ingestion Process Started =====")

            df = self.export_collection_as_dataframe()
            df = self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info(f"Data Ingestion Artifact Created: {data_ingestion_artifact}")
            logging.info("===== Data Ingestion Process Completed Successfully =====")

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
