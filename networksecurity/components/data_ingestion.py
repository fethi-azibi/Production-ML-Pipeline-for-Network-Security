import os
import sys
import numpy as np
import pandas as pd
from typing import List
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
## configuration of the Data Ingestion Config
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.logging.logger import logging

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URL from environment variables
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

print("#####################################")
print(MONGO_DB_URL)
print("#####################################")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        """
        Initialize DataIngestion with configuration.
        """
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_collection_as_dataframe(self,):
        '''
        Reads data from MongoDB collection and exports it as a pandas DataFrame.
        Returns:
            df (pd.DataFrame): DataFrame containing collection data.
        '''
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            # Connect to MongoDB
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]
            # Convert collection to DataFrame
            df=pd.DataFrame(list(collection.find()))
            # Drop MongoDB's default '_id' column if present
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            # Replace 'na' strings with np.nan
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException

    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        """
        Saves the DataFrame to the feature store as a CSV file.
        Args:
            dataframe (pd.DataFrame): Data to be saved.
        Returns:
            dataframe (pd.DataFrame): The same DataFrame.
        """
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            # Create directory if it doesn't exist
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            # Save DataFrame to CSV
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        """
        Splits the DataFrame into train and test sets, saves them as CSV files.
        Args:
            dataframe (pd.DataFrame): Data to split.
        """
        try:
            # Split data into train and test sets
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            
            # Create directory for train/test files if it doesn't exist
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            # Save train set to CSV
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            # Save test set to CSV
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_ingestion(self):
        """
        Orchestrates the data ingestion process: 
        - Reads data from MongoDB
        - Saves to feature store
        - Splits into train/test sets
        - Returns DataIngestionArtifact with file paths
        Returns:
            dataingestionartifact (DataIngestionArtifact): Artifact containing file paths.
        """
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException

