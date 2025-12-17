import os
import pandas
from src.logger import get_logger
import pandas as pd
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)


## reading yaml files
def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"file is not in given path")
        
        with open(file_path,"r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Succesfully read YAML file")
            return config
    
    except Exception as e:
        logger.error("Error while reading yaml file")
        raise CustomException("Failed to read YAML file",e)


def load_data(path):
    try:
        logger.info("Loading data")
        return pd.read_csv(path)
    
    except Exception as e:
        logger.error(f"Error loading the data {e}")
        raise CustomException("Failed to load data",e)