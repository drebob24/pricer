from arg_parser import get_args
from process_results import generate_cost_report
from file_handling import (
    get_item_list,
    save_results,
    load_watchlist,
)
from process_searches import handle_item_search
from cost_comparison import handle_cost_comparison
from datetime import datetime
import sys


def main():
    args = get_args()
    search_list = get_item_list(args)
    if args.search:
        search_results = handle_item_search(search_list, args)
        save_results(search_results, args)

    if args.compare:
        search_results = handle_item_search(search_list, args)
        cost_data = handle_cost_comparison(search_results, args)
        report = generate_cost_report(cost_data, args)
        if args.save:
            save_results(report, args)
        else:
            print("\n" + "\n".join(report))

    if args.watch:
        try:
            watchlist = load_watchlist("watchlist.csv")
        except FileNotFoundError:
            print("No watchlist.csv found, creating new one.")
            watchlist = []
        if args.watch == "add":
            new_items = get_item_list(args)
            new_items = check_if_exists(watchlist, new_items)
            search_results = handle_item_search(new_items, args)
            search_results = add_percentage_key(search_results)
            search_results = add_timestamp(search_results)
            new_watchlist = watchlist + search_results
        if args.watch == "remove":
            removal_list = get_item_list(args)
            new_watchlist = remove_items(watchlist, removal_list)
        if args.watch == "update":
            update_list = parse_searches(watchlist)
            update_results = handle_item_search(update_list, args)
            new_watchlist, history_data = compare_watchlist_data(watchlist, update_results)
            new_watchlist = add_timestamp(new_watchlist)

        save_results(new_watchlist, args)


def add_timestamp(item_list: list) -> list:
    for item in item_list:
        item["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return item_list


def add_percentage_key(item_list: list) -> list:
    for item in item_list:
        item["percent_change"] = 0.0
    return item_list


def remove_items(item_list: list, delete_list: list) -> list:
    return [item for item in item_list if item["search"] not in delete_list]


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


def parse_searches(item_list: list) -> list:
    searches = set(item["search"] for item in item_list)
    return list(searches)


def compare_watchlist_data(watchlist: list, updated_list: list) -> list:
    watchlist_search_list = [item["search"] for item in watchlist]
    for item in updated_list:
        index = watchlist_search_list.index(item["search"])
        item["percent_change"] = calculate_percentage(
            item["list_price"], float(watchlist[index]["list_price"])
        )

    return updated_list, watchlist


def calculate_percentage(new_price: float, old_price: float) -> int:
    percent_change = ((new_price - old_price) / old_price) * 100
    return round(percent_change)


if __name__ == "__main__":
    main()
