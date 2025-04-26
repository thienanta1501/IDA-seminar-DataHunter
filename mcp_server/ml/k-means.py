from typing import List, Union
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def train_kmeans(
    features_data: List[List[Union[int, float]]],
    n_clusters: int = 3
) -> dict:
    """     
    Train a KMeans clustering model.

    Args:
        features_data (List[List[Union[int, float]]]): The input feature data.
        n_clusters (int): The number of clusters to form.

    Returns:
        dict: A dictionary containing the cluster centers.
            - 'centroids': A list of cluster center points.
    """
    
    # Convert data to numpy arrays for processing
    X = np.array(features_data, dtype=float)

    # Standardize the features 
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train the model
    model = KMeans(n_clusters=n_clusters, random_state=42)
    model.fit(X_scaled)

    return {
        "centroids": model.cluster_centers_.tolist()
    }
    

def predict_kmeans(
    input_data: List[List[Union[int, float]]],
    features_data: List[List[Union[int, float]]],
    n_clusters: int = 3
) -> Union[int, List[int]]:
    """
    Predict the cluster index for the given input data using KMeans.
    
    Args:
        input_data (List[List[Union[int, float]]]): the data points to assign to clusters.
        features_data (List[List[Union[int, float]]]): the data used to train the clustering model.
        n_clusters (int): the number of clusters to form.
        
    Returns:
        Union[int, List[int]]: the predicted cluster index (or list of indices) for the input data.
    """
    # Train the KMeans model to get centroids
    model_data = train_kmeans(features_data, n_clusters)
    centroids = np.array(model_data["centroids"])

    # Scale input data using training data's scaler
    scaler = StandardScaler()
    scaler.fit(np.array(features_data, dtype=float))
    input_scaled = scaler.transform(np.array(input_data, dtype=float))

    # Assign input data to nearest centroid
    distances = []
    for point in input_scaled:
        point_distances = []
        for center in centroids:
            distance = np.linalg.norm(point - center)
            point_distances.append(distance)
        distances.append(point_distances)

    distances = np.array(distances)
    labels = np.argmin(distances, axis=1)

    return labels[0] if len(labels) == 1 else labels.tolist()


if __name__ == "__main__":
    features = [
    [1.0, 2.0],
    [1.5, 1.8],
    [5.0, 8.0],
    [8.0, 8.0],
    [1.0, 0.6],
    [9.0, 11.0]
]

    new_data = [
        [1.2, 1.9],
        [6.0, 9.0]
    ]

    predicted_clusters = predict_kmeans(new_data, features, n_clusters=3)
    print(predicted_clusters)