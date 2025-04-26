from typing import List, Union
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

def train_decision_tree_classifier(
    features_data: List[List[Union[int, float]]],
    target_data: List[Union[int, float]],
    test_ratio: float = 0.2
) -> dict:
    """
    Train a decision tree classifier and return the model.

    Args:
        features_data: 2D list of training feature values.
        target_data: list of training labels.
        test_ratio: tatio of test data.

    Returns:
        dict: trained DecisionTreeClassifier model and class names.
    """
    X_train, _, y_train, _ = train_test_split(features_data, target_data, test_size=test_ratio, random_state=42)
    model = DecisionTreeClassifier(criterion="entropy")
    model.fit(X_train, y_train)

    return {
        "model": model,
        "classes": model.classes_.tolist()
    }


def predict_decision_tree_classifier(
    input_data: List[List[Union[int, float]]],
    features_data: List[List[Union[int, float]]],
    target_data: List[Union[int, float]],
    test_ratio: float = 0.2
) -> Union[str, List[str]]:
    """
    Predict class labels using a decision tree trained on provided data.

    Args:
        input_data: data to be predicted.
        features_data: training feature values.
        target_data: training labels.
        test_ratio: ratio of test data.

    Returns:
        Predicted label(s).
    """
    result = train_decision_tree_classifier(features_data, target_data, test_ratio)
    model = result["model"]

    predictions = model.predict(input_data)
    return predictions[0] if len(predictions) == 1 else predictions.tolist()

if __name__ == "__main__":
    X_train = [
    [5, 30],   
    [10, 50], 
    [2, 15],   
    [8, 45],   
    [1, 10],   
    [3, 25],   
    [12, 60],  
    [7, 40],   
]

    y_train = ["low", "high", "low", "high","low", "low", "high", "high"]  
    input_data = [
    [6, 35],  
    [4, 20],  
]
    print(predict_decision_tree_classifier(input_data, X_train, y_train))