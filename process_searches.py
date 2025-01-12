import sys
import time
import random
from process_results import process_results
from barbora import get_barbora
from rimi import get_rimi


def handle_item_search(search_list: list, args) -> list:
    max_items = 10
    if len(search_list) > max_items:
        raise ValueError(
            f"Error: At most {max_items} items may be searched per instance."
        )
    print("Searching for items...")
    search_results = []
    for index, item in enumerate(search_list):
        if not args.save == "csv" and args.search and not args.watchlist:
            search_results += [f"\nResults for '{item}':\n"]
        search_results += get_search_results(item, args)
        if not args.save and not args.compare and not args.watchlist:
            print("\n".join(search_results))
            search_results = []
        if index < len(search_list) - 1:
            time.sleep(random.randint(2, 5))
    if (args.save or args.watchlist) and not search_results:
        print("No Results found. Nothing to output.")
        sys.exit(1)
    return search_results


def get_search_results(item: str, args) -> list:
    barbora_list = get_barbora(item, args.results)
    print(f"Barbora search '{item}' completed")
    rimi_list = get_rimi(item, args.results)
    print(f"Rimi search '{item}' completed")
    if barbora_list or rimi_list:
        return process_results(barbora_list + rimi_list, item, args)
    elif args.save == "csv" or args.compare or args.watchlist:
        return []
    else:
        return [f"No Results for search: '{item}'"]
