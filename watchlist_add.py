import sys
from datetime import datetime
from file_handling import get_item_list
from process_searches import handle_item_search


def check_if_exists(watchlist: list, new_items: list) -> list:
    existing_searches = {watched["search"] for watched in watchlist}
    filterd_items = []
    for item in new_items:
        if item in existing_searches:
            print(f"'{item}' already exists in the watchlist, ignoring item.")
        else:
            filterd_items.append(item)
    if not filterd_items:
        print("No items to add to watchlist.")
        sys.exit(1)
    return filterd_items


def add_timestamp(item_list: list) -> list:
    for item in item_list:
        item["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return item_list


def add_percentage_key(item_list: list) -> list:
    for item in item_list:
        item["percent_change"] = 0.0
    return item_list


def add_to_watchlist(watchlist: list, args) -> list:
    new_items = get_item_list(args)
    new_items = check_if_exists(watchlist, new_items)
    search_results = handle_item_search(new_items, args)
    search_results = add_percentage_key(search_results)
    search_results = add_timestamp(search_results)
    return watchlist + search_results