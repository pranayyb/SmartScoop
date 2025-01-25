import os
from dotenv import load_dotenv
from typing import Dict, List, Any
from datetime import datetime
from enum import Enum


class SeasonalEvent(Enum):
    CHRISTMAS = "christmas"
    BLACK_FRIDAY = "black_friday"
    CYBER_MONDAY = "cyber_monday"
    PRIME_DAY = "prime_day"
    BACK_TO_SCHOOL = "back_to_school"


# Predefined discount rates for seasonal events
DISCOUNTS = {
    SeasonalEvent.CHRISTMAS: 10,
    SeasonalEvent.BLACK_FRIDAY: 40,
    SeasonalEvent.CYBER_MONDAY: 30,
    SeasonalEvent.PRIME_DAY: 25,
    SeasonalEvent.BACK_TO_SCHOOL: 15,
}


class SeasonalOptimizer:
    def __init__(self):
        self.events = {}

    def register_event(
        self, event: SeasonalEvent, start_date: datetime, end_date: datetime
    ):
        """Registers a seasonal event with its start and end dates."""
        self.events[event] = {"start_date": start_date, "end_date": end_date}

    def should_wait_for_sale(self, product_id: str, current_price: float) -> bool:
        """Determines if waiting for an upcoming sale is beneficial based on expected discounts."""
        upcoming_events = self._get_upcoming_events()
        if not upcoming_events:
            return False

        event_discounts = self._calculate_expected_discounts(upcoming_events)

        # Display upcoming events and their discounts
        print("Upcoming events, discounts, and dates:")
        for event in event_discounts:
            print(
                f"- {event['event'].value.capitalize()}: "
                f"{event['discount']}% discount "
                f"(From {event['start_date'].strftime('%d-%m-%Y')} "
                f"to {event['end_date'].strftime('%d-%m-%Y')})"
            )

        # Wait for a sale if any event offers a discount greater than 15%
        return any(event["discount"] > 15 for event in event_discounts)

    def _get_upcoming_events(self) -> List[Dict]:
        """Fetches a list of upcoming events."""
        now = datetime.now()
        return [
            {
                "event": event,
                "data": {
                    "start_date": data["start_date"],
                    "end_date": data["end_date"],
                },
            }
            for event, data in self.events.items()
            if data["start_date"] > now
        ]

    def _calculate_expected_discounts(self, events: List[Dict]) -> List[Dict]:
        """Calculates expected discounts for the upcoming events."""
        return [
            {
                "event": eve["event"],
                "discount": DISCOUNTS[eve["event"]],
                "start_date": eve["data"]["start_date"],
                "end_date": eve["data"]["end_date"],
            }
            for eve in events
        ]
