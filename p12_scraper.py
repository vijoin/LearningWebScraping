import requests
from bs4 import BeautifulSoup

url = 'https://www.pagina12.com.ar'

def build_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'lxml')

def get_sections_links(index_soup):
    sections = index_soup.find(
        'ul', attrs={'class': 'horizontal-list main-sections hide-on-dropdown'}
        ).find_all('li')
    return [section.a.get('href') for section in sections]

def get_article_links(soup):
    articles = soup.find_all(attrs={'class': 'title-list'})
    return [article.a.get('href') for article in articles]

def get_body(article_soup):
    body_paragraph_list = article_soup.find('div', attrs={'class': 'article-text'}).find_all('p')
    return ' '.join([p.get_text() for p in body_paragraph_list])


def get_article_data(article_soup):
    return {
        'title': article_soup.find('div', attrs={'class': 'article-header'}).h1.get_text(),
        'date': article_soup.find('span', attrs={'pubdate': 'pubdate'}).get('datetime'),
        'headlines': article_soup.find('div', attrs={'class': 'article-header'}).h4.get_text(),
        'intro': article_soup.find('div', attrs={'class': 'article-header'}).h3.get_text(),
        'author': article_soup.find('div', attrs={'author-name'}).get_text().replace('Por ', ''),
        'body': get_body(article_soup),
    }



s_index = build_soup(url)
section_links = get_sections_links(s_index)

s_section = build_soup(section_links[0])
article_links = get_article_links(s_section)

s_article = build_soup(url + article_links[0])
article_data = get_article_data(s_article)
print(article_data)