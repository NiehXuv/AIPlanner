# components/clustering.py
from sklearn.cluster import KMeans
import numpy as np
import logging

def cluster_pois(pois, days):
    """
    Cluster POIs into groups for each day using KMeans clustering based on lat/lon.
    
    Args:
        pois (list): List of POIs, each with 'lat' and 'lon' fields.
        days (int): Number of days to cluster POIs into.
    
    Returns:
        list: List of clusters, where each cluster is a list of POIs for a day.
    """
    if not pois:
        return [[] for _ in range(days)]

    # Remove duplicates based on POI name (just in case)
    seen_names = set()
    unique_pois = []
    for poi in pois:
        if poi["name"] not in seen_names:
            seen_names.add(poi["name"])
            unique_pois.append(poi)
        else:
            logging.warning(f"Duplicate POI found before clustering: {poi['name']}")
    pois = unique_pois

    # Extract coordinates for clustering
    coords = np.array([[poi["lat"], poi["lon"]] for poi in pois])
    
    # Use KMeans to cluster POIs into 'days' clusters
    kmeans = KMeans(n_clusters=min(days, len(pois)), random_state=42)
    labels = kmeans.fit_predict(coords)
    
    # Group POIs by cluster, ensuring no duplicates
    clusters = [[] for _ in range(min(days, len(pois)))]
    assigned_pois = set()
    for poi, label in zip(pois, labels):
        if poi["name"] not in assigned_pois:
            clusters[label].append(poi)
            assigned_pois.add(poi["name"])
        else:
            logging.warning(f"POI {poi['name']} was assigned to multiple clusters. Skipping duplicate assignment.")
    
    # Ensure we have exactly 'days' clusters (pad with empty lists if needed)
    while len(clusters) < days:
        clusters.append([])
    
    return clusters