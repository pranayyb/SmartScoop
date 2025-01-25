from SmartScoop.user_profile import UserProfileManager
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict


class RecommendationEngine:
    def __init__(self, user_profile_manager: UserProfileManager):
        self.user_profile_manager = user_profile_manager
        self.model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        self.product_embeddings = {}

    def update_product_embeddings(self, products: List[Dict]):
        """
        Update product embeddings using a transformer model for product descriptions.
        """
        product_descriptions = [p.get("description", "") for p in products]

        product_embeddings = self.model.encode(
            product_descriptions, convert_to_tensor=True
        )

        self.product_embeddings = {
            p["id"]: embedding for p, embedding in zip(products, product_embeddings)
        }

    def get_recommendations(self, user_id: str, category: str = None) -> List[Dict]:
        """
        Get product recommendations based on user preferences and product descriptions.
        """
        profile = self.user_profile_manager.get_user_profile(user_id)
        if not profile or not self.product_embeddings:
            return []

        user_preferences = (
            profile.preferences
            if not category
            else profile.preferences.get(category, {})
        )
        user_vector = self._create_user_vector(user_preferences)

        user_vector_cpu = user_vector.cpu().numpy().flatten()

        similarities = {
            product_id: cosine_similarity(
                [user_vector_cpu], [embedding.cpu().numpy().flatten()]
            )[0][0]
            for product_id, embedding in self.product_embeddings.items()
        }

        sorted_products = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        return [int(product_id) for product_id, similarity in sorted_products[:10]]

    def _create_user_vector(self, preferences: Dict) -> np.ndarray:
        """
        Convert user preferences into a vector using transformer model for semantic matching.
        """
        preference_string = self._get_preference_string(preferences)

        user_vector = self.model.encode([preference_string], convert_to_tensor=True)
        return user_vector

    def _get_preference_string(self, preferences: Dict) -> str:
        """
        Generate a string based on user preferences to feed into the model.
        """
        preference_string = ""

        size = preferences.get("size", "M")
        preference_string += f"Size: {size} "

        color = preferences.get("color", "black")
        preference_string += f"Color: {color} "

        return preference_string
