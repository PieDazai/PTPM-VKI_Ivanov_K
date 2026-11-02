import time

import requests
from bs4 import BeautifulSoup

class ForumParser:

    def parse_page(self, url, repository):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/150.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        bs = BeautifulSoup(response.text, "html.parser")

        posts = bs.find_all("article")

        results = []

        for post in posts:
            name = post.find("span", class_="autor")
            message = post.find("div", itemprop="description")

            post_id = post.get("itemid")

            if not post_id:
                continue
            else:
                post_id = int(post_id)


            if message and post_id:
                results.append({
                    "id": post_id,
                    "name": name.get_text(strip=True) if name else "Неизвестный автор",
                    "message": str(message)
                })

        saved_count = self.save_to_db(results, repository)

        print("Найдено записей:", len(results))
        print("Сохранено новых записей:", saved_count)

        return results

    def save_to_db(self, data, repository):
        saved_count = 0

        for post in data:
            if repository.get_by_id(post["id"]) is None:
                repository.add(
                    post["id"],
                    post["name"],
                    post["message"]
                )

                saved_count += 1

        return saved_count

    def parse_pages(self, url, repository, pages):
        all_results = []
        base_url = url.rstrip("/")

        for page in range(pages):
            if page == 0:
                page_url = f"{base_url}/"
            else:
                page_url = f"{base_url}/page/{page + 1}/"

            print(f"\nПарсинг страницы {page + 1}...")
            results = self.parse_page(page_url, repository)
            all_results.extend(results)

            if page < pages - 1:
                time.sleep(1)

        print("\nВсего найдено записей:", len(all_results))
        return all_results