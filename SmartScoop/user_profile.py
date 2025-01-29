import sqlite3
import json
from typing import Dict, Optional
from pydantic import BaseModel, Field
from SmartScoop.database import DatabaseManager


class UserProfile(BaseModel):
    user_id: str
    preferences: Dict = Field(default_factory=dict)
    style_profile: Dict = Field(default_factory=dict)
    budget_limits: Dict = Field(default_factory=dict)


class UserProfileManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        try:
            with sqlite3.connect(self.db_manager.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                user_data = cursor.fetchone()

                if user_data:
                    return UserProfile(
                        user_id=user_data[0],
                        preferences=json.loads(user_data[1]),
                        style_profile=json.loads(user_data[2]),
                        budget_limits=json.loads(user_data[3]),
                    )
            return []
        except sqlite3.DatabaseError as e:
            print(f"Error occurred while fetching the user profile: {e}")
            return []

    def update_user_profile(self, profile: UserProfile):
        try:
            with sqlite3.connect(self.db_manager.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO users (user_id, preferences, style_profile, budget_limits)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        profile.user_id,
                        json.dumps(profile.preferences),
                        json.dumps(profile.style_profile),
                        json.dumps(profile.budget_limits),
                    ),
                )
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error occurred while updating the user profile: {e}")
