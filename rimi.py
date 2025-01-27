import requests
import re
from bs4 import BeautifulSoup
from typing import Optional

'''
Save for later, regex to find end unit in name of item:      [,\/]\s*(\d+,*\d*)\s*(\w+)$
'''

def grab_rimi_html(item) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(f"https://www.rimi.lt/e-parduotuve/lt/paieska?query={item}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e: 
        raise ValueError(f"Error grabbing HTML: {e} :Rimi")
    soup_data = BeautifulSoup(response.text, "html.parser")
    if soup_data:
        return soup_data
    else:
        raise ValueError("Empty Return or Invalid HTML: Rimi")


def extract_rimi_product_containers(html_data: BeautifulSoup) -> Optional[BeautifulSoup]:
    product_containers = html_data.find_all("div", class_="js-product-container card -horizontal-for-mobile")
    if product_containers:
        return product_containers
    else:
        raise ValueError("No product data found: Rimi")
    

def check_no_results(html_data: BeautifulSoup) -> bool:
    error_page = html_data.find("h1", class_="error-page__heading")
    if error_page.get_text(strip=True) == "Prekė nerasta":
        return True
    else:
        return False
   

def get_unit_price(product_container: BeautifulSoup) -> Optional[list]:
    price_per = product_container.find("p", class_="card__price-per")
    price_per = price_per.get_text(strip=True)
    if price_per:
        found_price = re.search(r'^(.+)\n\s*.*\/(\w*\.*)$', price_per)
    else:
        raise ValueError("No price_per found: Rimi")
    if found_price:
        unit_price, unit = found_price.group(1), found_price.group(2)
        unit_price = unit_price.replace(",", ".")
        return [float(unit_price), unit]
    else:
        found_price = re.search(r'Šiuo metu prekės nėra', price_per)
        return None


def get_discount_price(product_container: BeautifulSoup) -> Optional[float]:
    discount_price = product_container.find("div", class_="price-label__price")
    if discount_price:
        euro, cents = [span.get_text(strip=True) for span in discount_price.find_all("span", class_=["major", "cents"])]
        current_price = euro + "." + cents
        return float(current_price)
    else:
        return None
    

def get_old_price(product_container: BeautifulSoup) -> Optional[float]:
    old_price = product_container.find("div", class_="old-price-tag card__old-price")
    if old_price:
        retail_price = old_price.find("span").get_text(strip=True)
        retail_price = retail_price[:-1].replace(",", ".")
        return float(retail_price)
    else:
        return None
    

def get_card_price(product_container: BeautifulSoup) -> float:
    card_price = product_container.find("div", class_="price-tag card__price")
    if card_price:
        euro = card_price.find("span").get_text(strip=True)
        cents = card_price.find("sup").get_text(strip=True)
    else:
        raise ValueError("No card_price found: Rimi")
    return float(euro + "." + cents)


def get_discount_unit_price(product_container: BeautifulSoup) -> float:
        price_per = product_container.find("div", class_="price-per-unit")
        if price_per:
            unit_price = price_per.get_text(strip=True)
            unit_price = re.search(r"(\d+,\d+)", unit_price).group(1)
            unit_price = unit_price.replace(",", ".")
            return float(unit_price)
        else:
            raise ValueError("Discount Unit Price expected but not found: Rimi")


def organize_rimi_data(name: str, list_price: float, retail_price: float, unit_price: list) -> dict:
    item = {}
    item["title"] = name
    item["list_price"] = list_price
    item["unit_price"] = unit_price[0]
    item["unit"] = unit_price[1]
    item["retail_price"] = retail_price
    item["store"] = "Rimi"
    return item


def parse_rimi_data(product_data: BeautifulSoup, amount=5) -> list:
    '''
    Amount will self-cap at 20 (page cap) or fewer if there are not many results.
    '''
    i = 0
    item_list = []
    for product in product_data:
        if i > amount-1:
            break
        on_sale = False
        per_price = get_unit_price(product)
        #Skip item if None returned -> indicates out of stock
        if not per_price:
            continue
        listed_price = get_discount_price(product)
        if listed_price:
            retail_price = get_card_price(product)
            per_price[0] = get_discount_unit_price(product)
            on_sale = True
        else:
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


def get_rimi(search_item: str, results: int) -> list:
    page_data = grab_rimi_html(search_item)
    try:
        container_data = extract_rimi_product_containers(page_data)
    except ValueError as e:
        if check_no_results(page_data):
            print(f"No results found for '{search_item}': Rimi")
        else:
            print(f"ERROR: {e}")
        return []
    product_list = parse_rimi_data(container_data, results)
    return product_list
    # print_html(page_data)


def print_html(html):
    '''
    Currently only used for troubleshooting, to be removed?
    '''
    # with open("rimi_items.json", "w") as save:
    #     json.dump(html, save, indent=2)
    with open("rimi_container.html", "w") as f:
        f.write("".join(str(tag) for tag in html))


if __name__ == "__main__":
    get_rimi()