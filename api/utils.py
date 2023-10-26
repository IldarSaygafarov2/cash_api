import random

import requests
import json
from bs4 import BeautifulSoup
from .models import Category, Currency

BASE_URL = "https://uznews.uz"


def get_soup(url: str) -> BeautifulSoup:
    html = requests.get(url).text
    return BeautifulSoup(html, "html.parser")


def get_top_news(url=BASE_URL):
    soup = get_soup(url)
    result = []
    wrapper = soup.find("div", class_="infinite-scroll-component")
    items = wrapper.find_all("div", {"itemprop": "itemListElement"})

    for item in items:
        title = item.find("h3", {"itemprop": "name"}).get_text(strip=True)
        description = item.find("p", {"itemprop": "description"}).get_text(strip=True)
        image = item.find("noscript").find("img").get("src")
        link = BASE_URL + item.find("a")["href"]
        result.append({
            "title": title,
            "description": description,
            "image": image,
            "link": link
        })
    return result


# def save_to_json():
#     with open("../news.json", mode="w", encoding="utf-8") as file:
#         data = get_top_news()
#         json.dump(data, file, indent=4, ensure_ascii=False)
#
#
# save_to_json()


def read_from_json(filename):
    with open(filename, mode="r", encoding="utf-8") as file:
        data = json.load(file)
        return data


def generate_code():
    return ''.join(random.sample([f"{i}" for i in range(10)], 6))


def make_qs_list(qs, item_type):
    result = []
    for item in qs:
        category = Category.objects.filter(pk=item['category_id']).values()
        currency = Currency.objects.get(pk=item['currency_id'])

        res = {
            'id': item['id'],
            'created_at': item['created_at'],
            'amount': item['amount'],
            'currency': currency.code,
            'category': category.first(),
            'user': item['user_id'],
            'type': item_type
        }

        result.append(res)
    return result



