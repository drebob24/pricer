from arg_parser import get_args
from barbora import get_barbora
from rimi import get_rimi
from process_results import process_results, generate_item_text
from file_handling import read_item_file, write_results_txt, write_results_csv
import sys
import time
import random


def main():
    """
    FURTHER FUNCTIONS:
    -Save watch list
        -Track if price goes up/down from last fetch
        -Save history of price data?
    -Create list in program (why?)

    -Make results more robust such as sorting by similarity to search term
    """
    args = get_args()
    search_list = get_search_list(args)
    if args.mode == "search":
        search_results = handle_item_search(search_list, args)
        save_results(search_results, args.save)
    if args.mode == "total":
        search_results = handle_item_search(search_list, args)
        cost_data = handle_cost_comparison(search_results, args)
        report = generate_cost_report(cost_data, args.mode)
        if args.save:
            save_results(report, args.save)
        else:
            print("\n" + "\n".join(report))


def get_search_list(args):
    if args.items:
        return args.items
    if args.file:
        return read_item_file(args.file)


def save_results(search_results: list, filetype):
    if filetype == "txt":
        write_results_txt(search_results)
    if filetype == "csv":
        write_results_csv(search_results)


def handle_item_search(search_list: list, args) -> list:
    max_items = 10
    if len(search_list) > max_items:
        raise ValueError(
            f"Error: At most {max_items} items may be searched per instance."
        )
    print("Searching for items...")
    search_results = []
    for index, item in enumerate(search_list):
        if not args.save == "csv" and args.mode == "search":
            search_results += [f"\nResults for '{item}':\n"]
        search_results += get_search_results(item, args)
        if not args.save and not args.mode == "total":
            print("\n".join(search_results))
            search_results = []
        if index < len(search_list) - 1:
            time.sleep(random.randint(2, 5))
    if args.save and not search_results:
        sys.exit("No Results found. Nothing to output. (Exit Code: 1)")
    return search_results


def get_search_results(item: str, args) -> list:
    barbora_list = get_barbora(item, args.results)
    print(f"Barbora search '{item}' completed")
    rimi_list = get_rimi(item, args.results)
    print(f"Rimi search '{item}' completed")
    if barbora_list or rimi_list:
        return process_results(barbora_list + rimi_list, item, args)
    elif args.save == "csv" or args.mode == "total":
        return []
    else:
        return [f"No Results for search: '{item}'"]


def handle_cost_comparison(item_list, args):
    if args.compare == "together":
        shopping_data = [{
            "store": "both",
            "cost": calculate_together_cost(item_list),
            "items": item_list
        }]  
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


def generate_cost_report(cost_data: list, mode: str) -> list:
    report = []
    # cheapest_cost = min(cost_data, key=lambda x: x["cost"])
    sorted_data = sorted(cost_data, key=lambda x: x["cost"])
    report += [f"The Cheapest Total Cost for the Shopping List is: {sorted_data[0]["cost"]} €"]
    if sorted_data[0]["store"] != "both":
        report[-1] += f" from {sorted_data[0]["store"]}."
        report += [f"Total Cost is {sorted_data[1]["cost"]} € at {sorted_data[1]["store"]}."]
    for data in sorted_data:
        report += generate_item_text(data["items"], mode)
    return report


def calculate_seperate_cost(results):
    '''
    Results list should already be sorted by cheapest price, so need the first instance of an item
    per each store per search.
    '''
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
    

if __name__ == "__main__":
    main()
