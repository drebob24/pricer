from arg_parser import get_args
from barbora import get_barbora
from rimi import get_rimi
from process_results import process_results
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
    if args.search:
        search_results = handle_item_search(args, search_list)
        save_results(args, search_results)


def get_search_list(args):
    if args.items:
        return args.items
    if args.file:
        return read_item_file(args.file)


def save_results(args, search_results: list):
    if args.save == "txt":
        write_results_txt(search_results)
    if args.save == "csv":
        write_results_csv(search_results)


def handle_item_search(args, search_list: list) -> list:
    max_items = 10
    if len(search_list) > max_items:
        raise ValueError(
            f"Error: At most {max_items} items may be searched per instance."
        )
    print("Searching for items...")
    search_results = []
    for index, item in enumerate(search_list):
        search_results += get_search_results(item, args)
        if not args.save == "csv":
            search_results = [f"Results for '{item}':\n"] + search_results
        if not args.save:
            print("\n".join(search_results))
        if index < len(search_list) - 1:
            time.sleep(random.randint(2, 5))
    if not search_results:
        sys.exit("No Results found. Nothing to output. (Exit Code: 1)")
    return search_results


def get_search_results(item: str, args) -> list:
    barbora_list = get_barbora(item, args.results)
    print(f"Barbora search '{item}' completed")
    rimi_list = get_rimi(item, args.results)
    print(f"Rimi search '{item}' completed")
    if barbora_list or rimi_list:
        return process_results(barbora_list + rimi_list, item, args.order, args.save)
    elif args.save == "csv":
        return []
    else:
        return [f"No Results for search: '{item}'"]


if __name__ == "__main__":
    main()
