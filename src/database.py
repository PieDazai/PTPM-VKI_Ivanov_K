import sqlite3

class Database:

    def __init__(self, database_name="database.db"):
        self.connection = sqlite3.connect(database_name)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                login TEXT,
                password TEXT,
                confirm_password TEXT,
                result INTEGER,
                message TEXT
            )
        """)

    def add_user(
            self,
            login,
            password,
            confirm_password,
            result,
            message
    ):
        self.connection.execute(
            """
            INSERT INTO registrations
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                login,
                password,
                confirm_password,
                result,
                message
            )
        )

        self.connection.commit()

    def get_user(
            self,
            login
    ):
        cursor = self.connection.execute(
            """
            SELECT result, message
            FROM registrations
            WHERE login = ?
            """,
            (login,)
        )

        return cursor.fetchone()

    def delete_user(
            self,
            login,
            password
    ):
        delete_result = self.connection.execute(
            """
            DELETE FROM registrations
            WHERE login = ?
            AND password = ?
            """,
            (
                login,
                password
            )
        )

        self.connection.commit()

        return delete_result.rowcount > 0