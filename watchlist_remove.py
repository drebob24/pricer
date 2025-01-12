from file_handling import get_item_list


def remove_items(item_list: list, delete_list: list) -> list:
    return [item for item in item_list if item["search"] not in delete_list]


def remove_from_watchlist(watchlist: list, args) -> list:
    removal_list = get_item_list(args)
    return remove_items(watchlist, removal_list)
