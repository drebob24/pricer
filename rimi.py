import requests
import json
import re
from bs4 import BeautifulSoup

'''
Save for later, regex to find end unit in name of item:      [,\/]\s*(\d+,*\d*)\s*(\w+)$
'''

def grab_rimi_html():
    response = requests.get("https://www.rimi.lt/e-parduotuve/lt/paieska?currentPage=3&pageSize=20&query=pyragas")
    soup_data = BeautifulSoup(response.text, "html.parser")
    if soup_data:
        return soup_data
    else:
        raise ValueError("No html data found")


def extract_rimi_product_containers(raw_data):
    product_containers = raw_data.find_all("div", class_="js-product-container card -horizontal-for-mobile")
    if product_containers:
        return product_containers
    else:
        raise ValueError("No product data found")
    

def get_unit_price(product_container):
    price_per = product_container.find("p", class_="card__price-per")
    price_per = price_per.get_text(strip=True)
    if price_per:
        found_price = re.search(r'^(.+)\n\s*.*\/(\w*\.*)$', price_per)
    else:
        raise ValueError("No price_per found")
    if found_price:
        unit_price, unit = found_price.group(1), found_price.group(2)
        unit_price = unit_price.replace(",", ".")
        return [float(unit_price), unit]
    else:
        found_price = re.search(r'Šiuo metu prekės nėra', price_per)
        return False


def get_discount_price(product_container):
    discount_price = product_container.find("div", class_="price-label__price")
    if discount_price:
        euro, cents = [span.get_text(strip=True) for span in discount_price.find_all("span", class_=["major", "cents"])]
        current_price = euro + "." + cents
    else:
        current_price = False
    return float(current_price)


def get_old_price(product_container):
    old_price = product_container.find("div", class_="old-price-tag card__old-price")
    if old_price:
        retail_price = old_price.find("span").get_text(strip=True)
        retail_price = retail_price[:-1].replace(",", ".")
    else:
        retail_price = False
    return float(retail_price)


def get_card_price(product_container):
    card_price = product_container.find("div", class_="price-tag card__price")
    if card_price:
        euro = card_price.find("span").get_text(strip=True)
        cents = card_price.find("sup").get_text(strip=True)
    else:
        raise ValueError("No card_price found")
    return float(euro + "." + cents)


def organize_rimi_data(name: str, list_price: str, retail_price: str, unit_price: list):
    item = {}
    item["title"] = name
    item["list_price"] = list_price
    item["unit_price"] = unit_price[0]
    item["unit"] = unit_price[1]
    item["retail_price"] = retail_price
    item["store"] = "Rimi"
    return item


def parse_rimi_data(product_data, amount=5):
    '''
    amount is for future proofing if functionality to allow the user to choose how many items to grab is added.
    Would need to be capped at 20 because that's how many items are returned per page
    '''
    i = 0
    item_list = []
    for product in product_data:
        if i > amount-1:
            break
        on_sale = False
        per_price = get_unit_price(product)
        #Skip item if False returned -> indicates out of stock
        if not per_price:
            continue
        listed_price = get_discount_price(product)
        if listed_price:
            retail_price = get_card_price(product)
            on_sale = True
        retail_price = get_old_price(product)
        if retail_price:
            listed_price = get_card_price(product)
            on_sale = True
        if not on_sale:
            listed_price = get_card_price(product)
            retail_price = listed_price
        product_name = product.get('data-gtm-click-name')
        product_information = organize_rimi_data(product_name, listed_price, retail_price, per_price)
        item_list.append(product_information)
        i += 1
    return item_list


def get_rimi():
    page_data = grab_rimi_html()
    container_data = extract_rimi_product_containers(page_data)
    product_list = parse_rimi_data(container_data)
    print_html(product_list)


def print_html(html):
    with open("rimi_items.json", "w") as save:
        json.dump(html, save, indent=2)


if __name__ == "__main__":
    get_rimi()