import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import DATA_DIR, RAW_FILE_PATH, TRAIN_FILE_PATH, TEST_FILE_PATH, CONFIG_PATH

from utils.common_functions import read_yaml
# print(CONFIG_PATH)
logger = get_logger(__name__)

class DataIngestion:

    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]
        print( self.config)
        print(self.bucket_name)
        print(self.file_name)
        print(self.train_test_ratio )
        os.makedirs(DATA_DIR, exist_ok=True)

        logger.info(f" Data Ingestion started with {self.bucket_name} and file name: {self.file_name}")


    def download_csv_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            print(bucket)
            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"raw data file is successfully downloaded to {RAW_FILE_PATH}")

        except Exception as e:
            logger.error("Error while downloading the csv file ")
            raise CustomException("FAiled to download csv file",e)

    def split_data(self):
        try:
            logger.info("Starting the train-test splitting process")
            data = pd.read_csv(RAW_FILE_PATH)

            train_data, test_data = train_test_split(data,test_size= 1 - self.train_test_ratio, random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"train and test data saved to {TRAIN_FILE_PATH} and {TEST_FILE_PATH} respectively")
        
        except Exception as e:
            logger.error("Error with splitting data ")
            raise CustomException("FAiled to split data to  train and test sets",e)

    def run(self):
        try:
            logger.info("Starting data ingestion process")
            self.download_csv_gcp()
            self.split_data()

            logger.info("Data ingestion completed")

        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")
        
        finally:
            logger.info("DAta ingestion completed")


if __name__ =="__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()