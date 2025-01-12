from process_searches import handle_item_search
from file_handling import save_results, parse_searches
from text_generation import generate_update_report
from watchlist_add import add_timestamp


def compare_watchlist_data(watchlist: list, updated_list: list) -> list:
    '''
    Debatable if comparing the list prices or unit prices is better.
    Went with unit prices as otherwise you end up with results such that a 6 pack was decrease in price 
    compared to a 10 pack.
    Still would have issues comparing say something that is listed per kg, and something listed per vnt.
    Compeltely accurace comparison would need to be much more robust. 
    '''
    watchlist_search_list = [item["search"] for item in watchlist]
    for item in updated_list:
        index = watchlist_search_list.index(item["search"])
        item["percent_change"] = calculate_percentage(
            item["unit_price"], float(watchlist[index]["unit_price"])
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