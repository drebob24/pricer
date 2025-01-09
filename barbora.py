import requests
import json
import re
from bs4 import BeautifulSoup
from typing import List, Optional


def grab_barbora_products(items) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(f"https://barbora.lt/paieska?q={items}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e: 
        raise ValueError(f"Error grabbing HTML: {e} :Barbora")
    soup_data = BeautifulSoup(response.text, "html.parser")
    if soup_data:
        return soup_data
    else:
        raise ValueError("Empty Return or Invalid HTML: Barbora")


def extract_barbora_items(raw_data: BeautifulSoup) -> Optional[List[dict]]:
    script_tag = raw_data.find("script", string=re.compile(r"window\.b_productList"))
    if script_tag:
        page_content = script_tag.string
        pattern = r"window\.b_productList\s*=\s*(.*);"
        match = re.search(pattern, page_content)
        if match:
            items = match.group(1)
            return json.loads(items)
        else:
            raise ValueError("No productList found in <script>: Barbora")
    else:
        raise ValueError("No productList <script> found: Barbora")
    


def parse_barbora_data(products: List[dict], amount=5) -> list:
    '''
    amount is for future proofing if functionality to allow the user to choose how many items to grab is added.
    Would need to be capped at 52 because that's how many items are returned per page
    '''
    items = []
    i = 0
    for product in products:
        #Only want the first 5 listed (in stock) items
        if i > amount-1:
            break
        item = {}
        if product["status"] == "suspended":
            #Skip product if sold out
            continue
        item["title"] = product["title"]
        item["list_price"] = product["units"][0]["price"]
        try:
            item["retail_price"] = product["units"][0]["retail_price"]
        except KeyError:
            #If no retail_price exists, then item not on sale and retail_price = listed_price
            item["retail_price"] = product["units"][0]["price"]
        item["unit_price"] = product["comparative_unit_price"]
        item["unit"] = product["comparative_unit"]
        item["store"] = "Barbora"
        items.append(item)
        i += 1
    return items


def get_barbora(search_item):
    page_data = grab_barbora_products(search_item)
    product_list = extract_barbora_items(page_data)
    cleaned_list = parse_barbora_data(product_list)
    return cleaned_list


def print_html(html):
    '''
    Currently only used for troubleshooting, to be removed?
    '''
    with open("barbora_items.json", "w") as save:
        json.dump(html, save, indent=2)


if __name__ == "__main__":
    get_barbora()
