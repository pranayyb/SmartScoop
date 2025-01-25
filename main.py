import os
import asyncio
import warnings
from SmartScoop.app import ShoppingAssistantApp
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

load_dotenv()

if __name__ == "__main__":
    config = {
        "db_name": os.getenv("DB_NAME", "shopping_assistant.db"),
        "AMAZON_API_KEY": os.getenv("AMAZON_API_KEY"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    }

    async def main():
        app = ShoppingAssistantApp(config)

        user_id = "user123"

        response = await app.handle_message(
            user_id, "Im looking for a new laptop under $1000 with good battery life"
        )
        print(f"Search response: {response}")

    asyncio.run(main())
