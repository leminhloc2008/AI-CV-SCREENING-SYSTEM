from typing import List
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculate cosine similarity between two embeddings.
    """
    return cosine_similarity([embedding1], [embedding2])[0][0]