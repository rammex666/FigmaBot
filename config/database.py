import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="discord_bot"
    )

def create_table_if_not_exists():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_levels (
            user_id BIGINT PRIMARY KEY,
            experience INT DEFAULT 0,
            level INT DEFAULT 1
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()