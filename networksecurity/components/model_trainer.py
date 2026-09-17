import os
import sys

from networksecurity.exception.exception import customException
from networksecurity.logging.logger import logger

from networksecurity.entity.artifact_entity import DataTransformationArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact

from networksecurity.utils.main_utils.utils import (
    load_numpy_array_data,
    evaluate_models,
)
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_object, save_object
from networksecurity.utils.ml_utils.metric.classification_metric import (
    get_classification_score,
)

from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise customException(e, sys) from e

    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            logger.info("Training model")
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost Classifier": AdaBoostClassifier(),
            }
            params = {
                "Decision Tree": {
                    "criterion": ["gini", "entropy"],
                },
                "Gradient Boosting": {
                    "learning_rate": [0.1, 0.01, 0.001],
                    "subsample": [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "Logistic Regression": {},
                "AdaBoost Classifier": {
                    "learning_rate": [0.1, 0.01, 0.5, 0.001],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "Random Forest": {
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
            }
            model_report: dict = evaluate_models(
                X_train=x_train,
                y_train=y_train,
                X_test=x_test,
                y_test=y_test,
                models=models,
                param=params,
            )

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            y_train_pred = best_model.predict(x_train)
            classification_train_metric = get_classification_score(
                y_true=y_train, y_pred=y_train_pred
            )
            ## TODO: Track the ML-flow
            y_test_pred = best_model.predict(x_test)
            classification_test_metric = get_classification_score(
                y_true=y_test, y_pred=y_test_pred
            )
            preprocessor = load_object(
                file_path=self.data_transformation_artifact.transformed_object_file_path
            )
            model_dir_path = os.path.dirname(
                self.model_trainer_config.trained_model_file_path
            )
            os.makedirs(model_dir_path, exist_ok=True)
            Network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=Network_model,
            )

            # Model traininer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric,
            )
            logger.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise customException(e, sys) from e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logger.info("Loading transformed training and testing arrays")
            train_array = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_train_file_path
            )
            test_array = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_test_file_path
            )
            logger.info("Splitting training and testing input and target feature")
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            logger.info("Loading preprocessor object")
            model = self.train_model(x_train, y_train, x_test, y_test)
            return model
        except Exception as e:
            raise customException(e, sys) from e
