import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score,recall_score,f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.model_params import *
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:

    def __init__(self,train_path, test_path, model_save_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_save_path = model_save_path
        self.params_dist = LIGHT_GBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_split_data(self):
        try:
            logger.info(f"Loading train data from {self.train_path} ")
            df_train = load_data(self.train_path)
            x_train = df_train.drop(columns = "booking_status")
            y_train = df_train["booking_status"]

            logger.info(f"Loading test data from {self.test_path} ")
            df_test = load_data(self.test_path)
            x_test = df_test.drop(columns = "booking_status")
            y_test = df_test["booking_status"]

            logger.info("Data loaded succesfully")
            return x_train, x_test, y_train, y_test
        
        except Exception as e:
            logger.error(f"Error in loading data pipeline  {e}")
            raise CustomException("Error in loading data pipeline",e)
        
    def training(self,x_train,y_train):
        try:
            logger.info("Initializing model ")
            lgbm_model = lgb.LGBMClassifier(random_state = self.random_search_params["random_state"])

            logger.info(" Hyperparameter tuning")
            random_search = RandomizedSearchCV(
                                  estimator=  lgbm_model,
                                  param_distributions= self.params_dist,
                                  n_iter = self.random_search_params["n_iter"],
                                  cv = self.random_search_params["cv"],
                                  verbose = self.random_search_params["verbose"],
                                  random_state =self.random_search_params["random_state"],
                                  scoring= self.random_search_params["scoring"]
                                  )
            
            logger.info("Starting the Hyperparameter tuning")
            random_search.fit(x_train,y_train)

            logger.info( f"Best model hyperparameters are {random_search.best_params_} ")
            best_lgbm_model = random_search.best_estimator_

            return best_lgbm_model


        except Exception as e:
            logger.error(f"Error in model training pipeline  {e}")
            raise CustomException("Error in model training pipeline ", e )
    
    def evaluate(self,x_test,y_test,model):
        try:
            logger.info("Model evaluation on test data")
            y_pred = model.predict(x_test)
            accuracy = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test, y_pred)
            f1_Score = f1_score(y_test, y_pred)
            logger.info(f"Model evaluation completed with accuracy: {accuracy}, precision:{precision}, recall:{recall} & F1score: {f1_Score} ")
            return {"accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1_Score": f1_Score
                    }
        
        except Exception as e:
            logger.error(f"Error in model evaluation pipeline  {e}")
            raise CustomException("Error in model evaluation pipeline ", e )
    

    def save_model(self,model):
        try:
            os.makedirs(os.path.dirname(self.model_save_path),exist_ok = True)
            joblib.dump(model,self.model_save_path)
            logger.info(f"Model saved at {self.model_save_path}")
        
        except Exception as e:
            logger.error(f"Error while saving model  {e}")
            raise CustomException("Error while saving model", e )
    
    def run(self):
        try:
            with mlflow.start_run():

                logger.info("Starting model training pipeline")
                logger.info("Starting our MLFLOW experimentation")
                logger.info("Logging the training and testing dataset to MLFLOW")

                mlflow.log_artifact(self.train_path, artifact_path = "datasets")
                mlflow.log_artifact(self.test_path, artifact_path = "datasets")


                x_train, x_test, y_train, y_test = self.load_split_data()
                model = self.training(x_train,y_train)
                metrics = self.evaluate(x_test,y_test,model)
                self.save_model(model)

                logger.info("Logging model to MLFLOW")
                mlflow.log_artifact(self.model_save_path)

                mlflow.log_params(model.get_params())
                mlflow.log_metrics(metrics)
                logger.info("Model training, evaluation and saving successfully  completed")

        except Exception as e:
            logger.error(f"Error while running pipeline  {e}")
            raise CustomException("Error while  running pipeline", e )
    
if __name__ =="__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH,MODEL_SAVE_PATH)
    trainer.run()