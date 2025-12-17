import os

### Creating path for data ingestion ###

DATA_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(DATA_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(DATA_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(DATA_DIR, "test.csv")

CONFIG_PATH = "config/config.yaml"



###  Data processing file ###

PROCESSED_DIR = "artifacts/processed"
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR,"processed_train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR,"processed_test.csv")


### Model Save path
MODEL_SAVE_PATH = "artifacts/models/lgbm_model.pkl"