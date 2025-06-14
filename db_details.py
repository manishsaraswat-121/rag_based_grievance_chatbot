import sqlite3

def display_all_complaints(db_path="api/complaints.db", table_name="complaints"):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute query to fetch all rows
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Get column names
        columns = [description[0] for description in cursor.description]

        # Print header
        print(" | ".join(columns))
        print("-" * 80)

        # Print each row
        for row in rows:
            print(" | ".join(str(cell) for cell in row))

        if not rows:
            print("No records found.")

        # Close the connection
        conn.close()

    except sqlite3.Error as e:
        print("Database error:", e)
    except Exception as e:
        print("Other error:", e)

# Run the function
if __name__ == "__main__":
    display_all_complaints()
