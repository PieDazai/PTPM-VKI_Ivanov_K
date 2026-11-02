from src.parser import ForumParser
from src.database import DatabaseRepository

parser = ForumParser()
repository = DatabaseRepository()

results = parser.parse_pages("https://4pda.to/games/", repository, 2)

for post in results:
    print("\nID:", post["id"])
    print("Автор:", post["name"])
    print("Сообщение с HTML-разметкой:")
    print(post["message"])
    print("-" * 50)