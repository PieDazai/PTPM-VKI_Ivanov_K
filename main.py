from src.parser import ForumParser
from src.database import DatabaseRepository

parser = ForumParser()
repository = DatabaseRepository()

# results = parser.parse_pages("https://4pda.to/games/", repository, 6)
#
# for post in results:
#     print("\nID:", post["id"])
#     print("Автор:", post["name"])
#     print("Сообщение с HTML-разметкой:")
#     print(post["message"])
#     print("-" * 50)

comments = repository.get_all()

for comment in comments:
    print(f"ID: {comment['id']}")
    print(f"Автор: {comment['name']}")
    print(f"Сообщение: {comment['message']}")
    print("-" * 50)