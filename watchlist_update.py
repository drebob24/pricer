from process_searches import handle_item_search
from file_handling import save_results
from text_generation import generate_update_report
from watchlist_add import add_timestamp

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


def update_watchlist(watchlist: list, args) -> list:
    update_list = parse_searches(watchlist)
    update_results = handle_item_search(update_list, args)
    new_watchlist, history_data = compare_watchlist_data(watchlist, update_results)
    new_watchlist = add_timestamp(new_watchlist)
    print("\n"+"\n".join(generate_update_report(new_watchlist, args))+"\n")
    if args.store_history:
        save_results(history_data, args, "historical_data.csv", "history")
    return new_watchlist