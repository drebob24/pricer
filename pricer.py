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
        total_cost = handle_cost_comparison(search_results, args)
        report = generate_cost_report(search_results, total_cost, args.mode)
        save_results(report, "txt")

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
        return calculate_together_cost(item_list)
    if args.compare == "seperate":
        ...


def calculate_together_cost(cheapest_list):
    searches = set()
    cost = 0
    for item in cheapest_list:
        if item["search"] not in searches:
            searches.add(item["search"])
            cost += item["list_price"]
    return cost


def generate_cost_report(items, total_cost, mode):
    report = []
    report += [f"The Cheapest Total Cost for the Shopping List is: {total_cost} €\n"]
    report += generate_item_text(items, mode)
    return report


if __name__ == "__main__":
    main()
