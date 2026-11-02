import sqlite3

class DatabaseRepository:

    def __init__(self, database_name="comments.db"):
        self.connection = sqlite3.connect(database_name)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INT PRIMARY KEY,
                name TEXT NOT NULL CHECK(length(name) <= 256),
                message TEXT NOT NULL CHECK(length(message) <= 8096)
            )
        """)

    def get_all(self):
        all_posts = self.connection.execute("SELECT * FROM comments")

        rows = all_posts.fetchall()

        result = []

        for row in rows:
            comment = {
                "id": row[0],
                "name": row[1],
                "message": row[2]
            }

            result.append(comment)

        return result

    def add(self, comment_id: int, username: str, message: str):
        if not isinstance(comment_id, int):
            raise TypeError("Id должен быть числом")

        if not isinstance(username, str):
            raise TypeError("Имя должно быть строкой")

        if len(username) > 256:
            raise ValueError("Имя слишком длинное")

        if not isinstance(message, str):
            raise TypeError("Сообщение должно быть строкой")

        if len(message) > 8096:
            raise ValueError("Сообщение слишком длинное")

        self.connection.execute(
            "INSERT INTO comments VALUES (?, ?, ?)",
            (comment_id, username, message)
        )

        self.connection.commit()
        return True

    def get_by_id(self, comment_id: int):
        result = self.connection.execute(
            "SELECT * FROM comments WHERE id = ?",
            (comment_id,)
        )

        row = result.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "message": row[2]
        }

    def get_by_name(self, username: str):
        name_posts = self.connection.execute(
            "SELECT * FROM comments WHERE name = ?",
            (username,)
        )

        rows = name_posts.fetchall()

        result = []

        for row in rows:
            comment = {
                "id": row[0],
                "name": row[1],
                "message": row[2]
            }

            result.append(comment)

        return result

    def update(self, comment_id: int, new_message: str):
        if not isinstance(new_message, str):
            raise TypeError("Сообщение должно быть строкой")

        if len(new_message) > 8096:
            raise ValueError("Сообщение слишком длинное")

        result = self.connection.execute(
            "UPDATE comments SET message = ? WHERE id = ?",
            (new_message, comment_id)
        )

        self.connection.commit()

        return result.rowcount > 0

    def delete(self, comment_id: int):
        result = self.connection.execute(
            "DELETE FROM comments WHERE id = ?",
            (comment_id,)
        )

        self.connection.commit()

        return result.rowcount > 0