import os
import json

# get class name: article-info using beautiful soup
import bs4
import requests


def crawl_articles():
  response = requests.get('https://restofworld.org/series/the-rise-of-ai/')
  soup = bs4.BeautifulSoup(response.text, 'html.parser')
  soup.select('.article-info')

  # get full link of class name: article-info
  links = soup.select('.article-info a')
  headings_text = [
      heading.getText() for heading in soup.select('.article-link h2')
  ]

  links1 = soup.select('.grid-story__link h2')
  links2 = soup.select('.article-link')
  links = links1 + links2
  links_urls = [
  ]  # [link.get('href') for link in soup.select('.article-info a')]
  for link in links:
    # add to set
    if link.get('href') not in links_urls and link.get('href') != None:
      links_urls.append(link.get('href'))
  len(links_urls)

  all_articles = []
  for heading, article in zip(headings_text, links_urls):
    all_articles.append({'heading': heading, 'link': article})
  return all_articles


# newly_crawled = get_articles()
# newly_crawled


def get_new_articles(old_articles, newly_crawled):
  new_articles = []
  # old_articles_links = [old_article['link'] for old_article in old_articles]
  for article in newly_crawled:
    # check article link in old articles

    # if article['link'] not in old_articles_links:
    #     new_articles.append(article)
    if article not in old_articles:
      new_articles.append(article)
  # print(new_articles)
  return new_articles


def get_old_articles():
  if not os.path.exists('articles.json'):
    # create file
    with open('articles.json', 'w') as f:
      json.dump([], f)

    return []

  with open('articles.json', 'r') as f:
    old_articles = json.load(f)
  return old_articles


def save_articles(articles):
  with open('articles.json', 'w') as f:
    json.dump(articles, f)


def get_articles():
  old_articles = get_old_articles()
  newly_crawled = crawl_articles()
  new_articles = get_new_articles(old_articles, newly_crawled)
  if new_articles:
    old_articles = new_articles + old_articles
    save_articles(old_articles)
    return reversed(new_articles)
  return []


if __name__ == '__main__':
  for article in get_articles():
    print(article['heading'], article['link'])
