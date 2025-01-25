import logging
from typing import Dict, List
import aiohttp  # type: ignore
from abc import ABC, abstractmethod

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# ProductSearchInterface for abstracting search functionality
class ProductSearchInterface(ABC):
    @abstractmethod
    async def search_products(self, query: str, filters: Dict) -> List[Dict]:
        pass

    @abstractmethod
    async def get_product_details(self, product_id: str) -> Dict:
        pass


# AmazonProductSearch class implementing the ProductSearchInterface
class AmazonProductSearch(ProductSearchInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://real-time-amazon-data.p.rapidapi.com"

    async def search_products(self, query: str, filters: Dict = None) -> List[Dict]:
        filters = filters or {}
        url = f"{self.base_url}/search"
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com",
        }
        params = {
            "query": query,
            "country": filters.get("country", "US"),
            "sort_by": filters.get("sort_by", "RELEVANCE"),
            "page": filters.get("page", 1),
            "is_prime": filters.get("is_prime", "false"),
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        return self._parse_products(result)
                    else:
                        logger.error(f"Amazon API error: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"Error searching Amazon products: {e}")
                return []

    async def get_product_details(self, product_id: str) -> Dict:
        url = f"{self.base_url}/{product_id}"
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com",
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        return self._parse_products(result)
                    else:
                        logger.error(f"Amazon API error: {response.status}")
                        return {}
            except Exception as e:
                logger.error(f"Error getting Amazon product details: {e}")
                return {}

    def _parse_products(self, products: List[Dict]) -> List[Dict]:
        """
        Extract and format product details from the API response.
        """
        # products = api_response.get("data", {}).get("products", [])
        products = products["data"]["products"]
        return [
            {
                "asin": product.get("asin"),
                "title": product.get("product_title"),
                "price": product.get("product_price"),
                "original_price": product.get("product_original_price"),
                "rating": product.get("product_star_rating"),
                "num_ratings": product.get("product_num_ratings"),
                "url": product.get("product_url"),
                "image": product.get("product_photo"),
                "is_prime": product.get("is_prime"),
                "delivery": product.get("delivery"),
                "sales_volume": product.get("sales_volume"),
            }
            for product in products
        ]
