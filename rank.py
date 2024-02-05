# pip install google beautifulsoup4
# npm install --global google-rank

import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import time

import os


def extract_keywords(url):
    try:
        response = requests.get(f"http://{url}")
        soup = BeautifulSoup(response.text, 'html.parser')

        # meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        # if meta_keywords:
        #     keywords = meta_keywords['content'].split(',')
        # else:
        keywords = []


        title = soup.find('title')
        if title:
            keywords.extend(title.text.strip().split())


        headings = soup.find_all(re.compile(r'h\d'))
        for heading in headings:
            keywords.extend(heading.text.strip().split())

        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            keywords.extend(paragraph.text.strip().split())

        keywords = list(set(keywords))
        keywords = [re.sub(r'\W+', '', keyword) for keyword in keywords]

        return keywords[:12]  
    except Exception as e:
        print("Error extracting keywords:", e)
        return []


def get_website_rank(url, keyword, proxy=None):
    try:
        os.system(f"google-rank {url} --keywords {keyword}")
        return None
    except Exception as e:
        return None


def main():
    parser = argparse.ArgumentParser(description="Get website ranks for keywords")
    parser.add_argument("url", type=str, help="URL of the website")
    parser.add_argument("--use-proxy", action="store_true", help="Use a proxy to fetch search results")
    args = parser.parse_args()


    keywords = extract_keywords(args.url)
    print("Keywords extracted:", keywords)

    for keyword in keywords:
        get_website_rank(args.url, keyword)
        # if rank is not None:
        #     print(f"Rank for '{keyword}' on Google: {rank}")
        # else:
        #     print(f"Keyword '{keyword}' not found in Google search results")


if __name__ == "__main__":
    main()
