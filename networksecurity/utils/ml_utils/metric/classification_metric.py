from sklearn.metrics import precision_score, recall_score, f1_score
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import CustomException
import sys


def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        f1 = f1_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)

        classification_metric = ClassificationMetricArtifact(
            f1_score=f1, precision_score=precision, recall_score=recall
        )
        return classification_metric
    except Exception as e:
        raise CustomException(e, sys) from e
