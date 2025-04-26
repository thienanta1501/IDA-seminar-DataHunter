from typing import List, Union
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def train_linear_regression(
    features_data: List[List[Union[int, float]]],
    target_data: List[Union[int, float]],
    test_ratio: float=0.2
) -> dict:
    """
    Train a linear regression model and return the model's weights and intercept.
    Args:
        features_data (List[List[Union[int, float]]]): a list of lists containing feature values for training.
        target_data (List[Union[int, float]]): a list containing the target values corresponding to the features.
        test_ratio (float, optional): the proportion of data to be reserved for testing (default is 0.2).
    Returns:
        dict: A dictionary containing the model's coefficients and 'intercept'.
            - 'weights': list of model coefficients (floats).
            - 'intercept': the model's intercept (float).
    """
    # Convert data to numpy arrays for processing
    X = np.array(features_data, dtype=float)
    y = np.array(target_data, dtype=float)

    # Standardize the features 
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split the data into training and testing sets
    X_train, _, y_train, _ = train_test_split(X_scaled, y, test_size=test_ratio, random_state=42)

    # Train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Return model parameters 
    return {
        "coefficients": model.coef_.tolist(),
        "intercept": model.intercept_,
    }


def predict_linear_regression(
    input_data: List[List[Union[int, float]]],
    features_data: List[List[Union[int, float]]],
    target_data: List[Union[int, float]],
    test_ratio: float = 0.2
) -> Union[float, List[float]]:
    """
    Predict values for input data based on a trained linear regression model using provided training data.
    Args:
        input_data (List[List[Union[int, float]]]): a list of input feature values to predict.
        features_data (List[List[Union[int, float]]]): the training features used to train the model.
        target_data (List[Union[int, float]]): the training target values corresponding to the features.
        test_ratio (float, optional): the proportion of data to reserve for testing during training (default is 0.2).
    Returns:
        Union[float, List[float]]: the predicted value(s). If there is only one input, a single float is returned.
            If there are multiple inputs, a list of floats is returned.
    """
    # Train the model to obtain weights and intercept
    model_params = train_linear_regression(features_data, target_data, test_ratio)

    # Extract the model's weights and intercept
    weights = np.array(model_params["weights"], dtype=float)
    intercept = model_params["intercept"]

    # Standardize the input data 
    scaler = StandardScaler()
    scaler.fit(np.array(features_data, dtype=float))  

    # Transform the input data using the scaler
    input_scaled = scaler.transform(np.array(input_data, dtype=float))

    # Calculate the predictions using the learned weights and intercept
    predictions = input_scaled @ weights + intercept

    # Return the prediction
    return predictions[0] if len(predictions) == 1 else predictions.tolist()