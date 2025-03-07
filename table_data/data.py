import sqlite3
import csv

DB_NAME = "shopping_assistant.db"

def export_table_to_csv(table_name, csv_filename):
    """Exports data from a given table to a CSV file."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Fetch all data from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Fetch column names
        column_names = [description[0] for description in cursor.description]

        # Write data to CSV
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(column_names)  # Write header
            writer.writerows(rows)  # Write data

        print(f"Exported {table_name} to {csv_filename}")

if __name__ == "__main__":
    # Export each table
    export_table_to_csv("users", "users.csv")
    # export_table_to_csv("price_alerts", "price_alerts.csv")
    export_table_to_csv("seasonal_discounts", "seasonal_discounts.csv")
