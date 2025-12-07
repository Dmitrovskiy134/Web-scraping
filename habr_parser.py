import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

URL = "https://habr.com/ru/all/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


def has_keywords(text):
    if not text:
        return False
    for keyword in KEYWORDS:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
            return True
    return False


def get_full_article(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        article_body = soup.find('div', id='post-content-body')
        if article_body:
            return article_body.text

        return ""
    except Exception:
        return ""


def main():
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')

        for article in articles:
            preview_text = article.text
            if has_keywords(preview_text):
                title = article.find('h2').text.strip()
                link = article.find('h2').find('a')['href']
                full_link = f'https://habr.com{link}' if link.startswith('/') else link

                date_str = article.find('time')['datetime']
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                date = date_obj.strftime('%d.%m.%Y')

                print(f'{date} – {title} – {full_link}')
            else:
                title_elem = article.find('h2')
                if title_elem:
                    link_elem = title_elem.find('a')
                    if link_elem and link_elem.get('href'):
                        link = link_elem['href']
                        full_link = f'https://habr.com{link}' if link.startswith('/') else link

                        full_text = get_full_article(full_link)
                        time.sleep(0.1)

                        if has_keywords(full_text):
                            title = title_elem.text.strip()

                            time_elem = article.find('time')
                            if time_elem and time_elem.get('datetime'):
                                date_str = time_elem['datetime']
                                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                                date = date_obj.strftime('%d.%m.%Y')
                            else:
                                date = "Дата не указана"

                            print(f'{date} – {title} – {full_link}')

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()