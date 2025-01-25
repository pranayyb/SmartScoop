import sqlite3


class DatabaseManager:
    def __init__(self, db_name: str = "shopping_assistant.db"):
        """Initialize the DatabaseManager with the specified database name."""
        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        """Create necessary tables if they do not already exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Create users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    preferences TEXT,
                    style_profile TEXT,
                    budget_limits TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # Create price alerts table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS price_alerts (
                    alert_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    product_id TEXT,
                    target_price REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
                """
            )

            conn.commit()
