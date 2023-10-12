import requests
from bs4 import BeautifulSoup


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




