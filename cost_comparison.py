from text_generation import generate_cost_report
from process_searches import handle_item_search


def handle_cost_comparison(item_list: list, args) -> list:
    if args.compare == "together":
        #data is formatted to match that of the seperate comparison
        shopping_data = [
            {
                "store": "both",
                "cost": calculate_together_cost(item_list),
                "items": item_list,
            }
        ]
        return shopping_data
    if args.compare == "seperate":
        return calculate_seperate_cost(item_list)


def calculate_together_cost(cheapest_list: list) -> float:
    """
    Item list should only include the cheapest item per search at this point per code.
    There could be multiple "cheapest" items though so need to just grab the first price for each search.
    """
    searches = set()
    cost = 0
    for item in cheapest_list:
        if item["search"] not in searches:
            searches.add(item["search"])
            cost += item["list_price"]
    return cost


def calculate_seperate_cost(results):
    """
    Results list should already be sorted by cheapest price, so need the first instance of an item
    per each store per search.
    """
    store_prices = [
        {
            "store": "Barbora",
            "cost": 0,
            "items": [],
        },
        {
            "store": "Rimi",
            "cost": 0,
            "items": [],
        },
    ]
    searches = set()
    for item in results:
        if item["search"] not in searches:
            barbora_found = False
            rimi_found = False
            searches.add(item["search"])
        if item["store"] == "Barbora" and not barbora_found:
            store_prices[0]["cost"] += item["list_price"]
            store_prices[0]["items"].append(item)
            barbora_found = True
        if item["store"] == "Rimi" and not rimi_found:
            store_prices[1]["cost"] += item["list_price"]
            store_prices[1]["items"].append(item)
            rimi_found = True
    return store_prices


def create_comparison_report(search_list: list, args) -> list:
    search_results = handle_item_search(search_list, args)
    cost_data = handle_cost_comparison(search_results, args)
    return generate_cost_report(cost_data, args)
