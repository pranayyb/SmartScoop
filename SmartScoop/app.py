from typing import Any, Dict

from SmartScoop.agent import ShoppingAssistantAgent
from SmartScoop.database import DatabaseManager
from SmartScoop.product_search import AmazonProductSearch
from SmartScoop.recommendation import RecommendationEngine
from SmartScoop.seasonal_discount import SeasonalOptimizer
from SmartScoop.user_profile import UserProfileManager
from langchain_groq import ChatGroq
import os


class ShoppingAssistantApp:
    def __init__(self, config: Dict[str, Any]):
        self.db_manager = DatabaseManager(
            config.get("db_name", "shopping_assistant.db")
        )
        self.user_profile_manager = UserProfileManager(self.db_manager)
        self.seasonal_optimizer = SeasonalOptimizer()
        self.product_searches = [AmazonProductSearch(config["AMAZON_API_KEY"])]
        self.recommendation_engine = RecommendationEngine(self.user_profile_manager)

        self.llm = ChatGroq(
            api_key=config["GROQ_API_KEY"],
            model_name="mixtral-8x7b-32768",
            temperature=0.6,
            max_tokens=1024,
        )
        # print(self.llm)
        self.agent = ShoppingAssistantAgent(
            llm=self.llm,
            product_searches=self.product_searches,
            user_profile_manager=self.user_profile_manager,
            recommendation_engine=self.recommendation_engine,
            seasonal_optimizer=self.seasonal_optimizer,
        )

    async def handle_message(self, user_id: str, message: str) -> str:
        return await self.agent.process_message(user_id, message)
