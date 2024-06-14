import requests
from bs4 import BeautifulSoup
import re
import time
url = 'https://www.nytimes.com/international/section/politics'
def parse_news():
    response = requests.get(url, headers={'User-Agent': 'Chrome/125.0.6422.176'})
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', class_='css-1l4spti')
    news = []
    for article in articles:
        title = article.find('h3', class_='css-1j88qqx e15t083i0').text
        summary = article.find('p', class_='css-1pga48a e15t083i1').text
        author = article.find('div', class_='css-1i4y2t3 e140qd2t0').text
        try:
            full_url = f"https://www.nytimes.com{article.a['href']}"
            article_response = requests.get(full_url, headers={'User-Agent': 'Chrome/125.0.6422.176'})
            article_content = BeautifulSoup(article_response.content, 'html.parser').getText()
            if re.search(r'Republ|Democrat', article_content):
                news.append({'title': title, 'summary': summary, 'author': author})
        except Exception as e:
            print(f"Ошибка при обработке статьи: {e}")
    return news

def run_parser():
    while True:
        new_news = parse_news()
        for news in new_news:
            print(f"Заголовок: {news['title']}")
            print(f"Аннотация: {news['summary']}")
            print(f"Автор: {news['author']}")
            print("-"  *  60)
        time.sleep(14400)

run_parser()
