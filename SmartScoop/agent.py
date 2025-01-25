import logging
from SmartScoop.product_search import ProductSearchInterface
from SmartScoop.recommendation import RecommendationEngine
from SmartScoop.seasonal_discount import SeasonalOptimizer
from SmartScoop.user_profile import UserProfileManager
from typing import Dict, List, Any, Optional
from langchain_core.chat_history import InMemoryChatMessageHistory
from pydantic import BaseModel
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain import hub
import asyncio


class ProductQuery(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None


class RecommendationQuery(BaseModel):
    user_id: str
    category: Optional[str] = None


class PreferenceUpdate(BaseModel):
    user_id: str
    preferences: Dict[str, Any]


class ProductInfo(BaseModel):
    product_info: Dict[str, Any]


class ShoppingAssistantAgent:
    def __init__(
        self,
        llm: "ChatGroq",
        product_searches: List[ProductSearchInterface],
        user_profile_manager: UserProfileManager,
        recommendation_engine: RecommendationEngine,
        seasonal_optimizer: SeasonalOptimizer,
    ):
        self.llm = llm
        self.product_searches = product_searches
        self.user_profile_manager = user_profile_manager
        self.recommendation_engine = recommendation_engine
        self.seasonal_optimizer = seasonal_optimizer

        chat_history = InMemoryChatMessageHistory()
        self.memory = ConversationBufferMemory(
            chat_memory=chat_history,
            memory_key="chat_history",
            return_messages=True,
            output_key="output",
        )

    def create_tools(self) -> List[Tool]:
        return [
            Tool(
                name="ProductSearch",
                func=lambda query: asyncio.run(self._search_products(query)),
                description="Search for products across multiple platforms. Input should be a single query.",
            ),
            Tool(
                name="GetRecommendations",
                func=lambda args: asyncio.run(self._get_recommendations(args)),
                description="Get personalized product recommendations based on user history and preferences. args should be user_id and category if given and pass as a dictionary.",
            ),
            Tool(
                name="SeasonalDiscount",
                func=lambda args: asyncio.run(self._check_seasonal_discount(args)),
                description="Analyze if a product might go on sale soon and if the user should wait. args should be list of dictionaries of products",
            ),
            Tool(
                name="UpdatePreferences",
                func=lambda args: asyncio.run(self._update_preferences(args)),
                description="Update user shopping preferences and style profile.",
            ),
        ]

    async def _search_products(self, query_str: str) -> str:
        args = ProductQuery(query=query_str)

        all_results = []
        for search_engine in self.product_searches:
            print(args.query)

            results = await search_engine.search_products(
                args.query, args.filters or {}
            )

            print("--------------------------------------------------------")
            print(results)
            print("--------------------------------------------------------")

            all_results.extend(results)

        if not all_results:
            return "No products found matching your criteria."

        formatted_results = [
            f"- {product['title']}\n ${product['price']} \nLink: ({product['url']})\n Rating: {product['delivery']}/5 ({product['rating']})"
            for product in all_results
        ]

        return "Found these products:\n" + "\n".join(formatted_results)

    async def _get_recommendations(self, args: RecommendationQuery) -> str:
        recommendations = await self.recommendation_engine.get_recommendations(
            args.user_id, args.category
        )

        if not recommendations:
            return "No personalized recommendations found."

        formatted_recommendations = [
            f"- {rec['name']}: ${rec['price']}\n  Recommendation Confidence: {rec['confidence_score']*100:.1f}%\n  Why: {rec['reason']}"
            for rec in recommendations
        ]
        return "Here are your personalized recommendations:\n" + "\n".join(
            formatted_recommendations
        )

    async def _check_seasonal_discount(self, args: ProductInfo) -> str:
        result = await self.seasonal_optimizer.should_wait_for_sale(args.product_info)
        if result["should_wait"]:
            return (
                f"I recommend waiting for {result['sale_event']} on {result['estimated_sale_date']}. "
                f"Expected discount: {result['expected_discount']}%. "
                f"Current price: ${result['current_price']:.2f}, "
                f"Estimated sale price: ${result['estimated_sale_price']:.2f}"
            )
        return "No significant sales expected soon. It's a good time to buy."

    async def _update_preferences(self, args: PreferenceUpdate) -> str:
        profile = await self.user_profile_manager.get_user_profile(args.user_id)
        if not profile:
            return f"No profile found for user {args.user_id}"

        profile.preferences.update(args.preferences)
        self.user_profile_manager.update_user_profile(profile)
        return f"Successfully updated preferences for user {args.user_id}"

    def _create_agent(self):
        tools = self.create_tools()
        prompt = hub.pull("hwchase17/react")
        # print(prompt)
        return create_react_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt,
        )

    async def process_message(self, user_id: str, message: str) -> str:
        try:
            agent = self._create_agent()
            agent_executor = AgentExecutor.from_agent_and_tools(
                agent=agent,
                tools=self.create_tools(),
                handle_parsing_errors=True,
                verbose=True,
                memory=self.memory,
                input_key="input",
                output_key="output",
            )

            input_dict = {
                "input": f"User {user_id} requests: {message}",
                "chat_history": self.memory.chat_memory.messages if self.memory else [],
            }

            response = await agent_executor.ainvoke(input_dict)

            if isinstance(response, dict) and "output" in response:
                return response["output"]
            return str(response)

        except IndexError as e:
            logging.error(f"Index error in process_message: {str(e)}", exc_info=True)
            raise RuntimeError("Agent configuration error") from e
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}", exc_info=True)
            return "I apologize, but I encountered an error processing your request. Please try rephrasing your question."

    def _validate_user_id(self, user_id: str) -> bool:
        """Validate user ID before processing"""
        if not user_id or not isinstance(user_id, str):
            return False
        return True

    def _validate_message(self, message: str) -> bool:
        """Validate message content before processing"""
        if not message or not isinstance(message, str):
            return False
        return True
