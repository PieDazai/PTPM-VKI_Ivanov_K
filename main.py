
from src.database import DatabaseRepository
from src.parser import ForumParser


parser = ForumParser()
database = DatabaseRepository()

url = "https://feeds.bbci.co.uk/news/rss.xml"

news = parser.parse_page(url)

parser.save_to_db(news, database)

for item in news:
    print(item["id"])
    print(item["name"])
    print(item["message"])
    print("-------------------")

database.close()