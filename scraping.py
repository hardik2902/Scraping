import pandas as pd
from bs4 import BeautifulSoup
import requests

HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
items = []
for i in range(1, 21):
    url = "https://www.amazon.in/s?k=bags&page=" + str(
        i) + "&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_" + str(i)
    req = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(req.content, "html.parser")
    titles = soup.find_all("div", attrs={"class": "s-result-item", "data-component-type": "s-search-result"})
    for title in titles:
        product_name = title.h2.text
        product_url = "https://amazon.com" + title.a["href"]
        try:
            product_price = title.find("span", attrs={"class": "a-price-whole"}).text
            product_rating = title.find("i", attrs={"class": "a-icon"}).text
            product_number_of_review = title.find_all("span", attrs={"aria-label": True})[1].text
        except AttributeError:
            continue
        except IndexError:
            continue
        second_req = requests.get(product_url, headers=HEADERS)
        second_soup = BeautifulSoup(second_req.content, "html.parser")
        try:
            product_description = description = second_soup.find("div", attrs={"id": "featurebullets_feature_div"}).find("ul").text.strip()
        except AttributeError:
            continue
        table = second_soup.find("table", attrs={"id": "productDetails_detailBullets_sections1"})
        list = {}
        try:
            for th in table:
                value = th.text.split("   ")
                list[value[0]] = value[-1]
        except AttributeError:
            continue
        except TypeError:
            continue
        try:
            product_asin = list['  ASIN']
            manufacturer = list['  Manufacturer']
        except KeyError:
            continue
        items.append([product_url, product_name, product_price, product_rating, product_number_of_review, description.strip(),
                      product_asin, product_description.strip(), manufacturer])
df = pd.DataFrame(items, columns=["Product URL", "Product Name", "Product Price", "Product Rating", "Number of reviews",
                                  "description", "product_asin", "product_description", "manufacturer"])
df.to_csv("scraped.csv", index=False)
