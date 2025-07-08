import os 
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.utils import save_object,evaluate_model
from src.exception import CustomException
from src.logger import logging

from sklearn.metrics import r2_score

@dataclass
class ModelTrainerConfig :
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_triner_config = ModelTrainerConfig()

    def initiate_model_triner(self, train_array, test_array, processor_path):
        try:
            logging.info("splitting training and test started")
            X_train, y_train, X_test, y_test = (
                train_array[:, : -1],
                train_array[:, -1],
                test_array[:, : -1],
                test_array[:, -1]
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            model_report:dict = evaluate_model(X_train = X_train, y_train = y_train, X_test = X_test, y_test= y_test , models = models)
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            #accepted scre threshold 
            if best_model_score < 0.6:
                raise CustomException("the best model found is under the accepted threshold")
            
            logging.info("Best model found on both trainging and testing data")

            save_object(
                file_path=self.model_triner_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(X_test)
            r2scoree = r2_score(y_test, predicted)
            return r2scoree


        except Exception as e:
            raise CustomException(e, sys)    