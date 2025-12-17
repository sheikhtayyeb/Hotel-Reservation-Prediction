import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE


logger = get_logger(__name__)

class DataProcessor:

    def __init__(self, train_path, test_path, processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self, df):

        try:
            logger.info("Data processing started")
            df.drop(columns = ['Unnamed: 0', 'Booking_ID'], inplace=True)
            df.drop_duplicates(inplace = True)

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info(" Applying label encoding")
            label_encoder = LabelEncoder()
            mappings = {}
            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col]= {label: code for label, code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}

            logger.info("label mapping are: ")
            for col, mapping in mappings.items():
                logger.info(f"{col} : {mapping}")

            logger.info("Doing skewness handling")
            skew_threshold = self.config['data_processing']['skewness_threshold']
            skewness = df[num_cols].apply(lambda x: x.skew()) 
            for col in num_cols:
                if skewness[col] > skew_threshold:
                    df[col] = np.log1p(df[col])
                
            return df
        except Exception as e:
            logger.error(f"Error during data preprocess {e}")
            raise CustomException("Error while processing data",e)

    def balance_data(self, df):

        try:
            logger.info("Starting creating a balanced dataset")

            x = df.drop(columns = "booking_status")
            y = df["booking_status"]
            smote = SMOTE(random_state =42)
            x_resampled, y_resampled = smote.fit_resample(x,y)
            balanced_df = pd.DataFrame(x_resampled, columns=x.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Balanced dataset succesfully created")
            return balanced_df
        
        except Exception as e:
            logger.error(f"Error during creating balanced dataset {e}")
            raise CustomException("Error while creating balanced dataset",e)

    def feature_select(self,df):

        try:
            logger.info("Started feature selection")
            x = df.drop(columns = "booking_status")
            y = df["booking_status"]
            model = RandomForestClassifier(random_state=42)
            model.fit(x,y)
            feature_imp = model.feature_importances_
            feature_imp_df = pd.DataFrame( {'feature':x.columns,
                                "feature_importance":feature_imp*100})
            feature_imp_df.sort_values(by = 'feature_importance',ascending = False,inplace=True)
            num_of_features = self.config['data_processing']['num_of_features']
            top_n_features = feature_imp_df["feature"][:num_of_features]
            df_top_n = df[top_n_features]
            # df_top_n.loc[:,"booking_status"] = df.loc[:,"booking_status"]
            df_top_n = df_top_n.join(y)
            logger.info(f"top {num_of_features} features selected are: {top_n_features}")
            logger.info("Feature selection completed")

            return df_top_n
        
        except Exception as e:
            logger.error(f"Error during feature selection {e}")
            raise CustomException("Error while feature selection",e)

    def save_processed_data(self,df, file_path):
        try:
            logger.info("Saving the data in processed folder")

            df.to_csv(file_path,index = False)

            logger.info(f"Data after processig saved in {file_path}")

        except Exception as e:
            logger.error(f"Error during saving data {e}")
            raise CustomException("Error while saving data",e)

    def process(self):

        try:
            logger.info("Loading data from raw directory")

            df_train = load_data( self.train_path)
            df_test =  load_data( self.test_path)

            df_train = self.preprocess_data(df_train)
            df_test  = self.preprocess_data(df_test)

            df_train = self.balance_data(df_train)
            #df_test = self.balance_data(df_test)

            df_train = self.feature_select(df_train)
            df_test = df_test[df_train.columns]

            self.save_processed_data(df_train,PROCESSED_TRAIN_DATA_PATH)
            self.save_processed_data(df_test,PROCESSED_TEST_DATA_PATH)

            logger.info("Data proccessed successfully and saved at {self.processed_dir}")

        except Exception as e:
            logger.error(f"Error in pipeline while proceesing data {e}")
            raise CustomException("Error in pipeline while proceesing data",e)

if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,
                              PROCESSED_DIR,CONFIG_PATH)
    processor.process()




