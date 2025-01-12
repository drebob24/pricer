import csv
import os


def get_item_list(args) -> list:
    if args.items:
        return args.items
    if args.file:
        return read_item_file(args.file)


def read_item_file(file_path: str) -> list:
    with open(file_path, "r") as file:
        items = [line.strip() for line in file]
    return items


def save_results(search_results: list, args):
    if args.save == "txt":
        write_results_txt(search_results, "Results/search_results.txt")
    if args.save == "csv":
        write_results_csv(search_results, "search", "Results/search_results.csv")
    if args.watch:
        write_results_csv(search_results, "watchlist", "watchlist.csv")


def write_results_txt(results: list, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w+", newline="") as file:
        file.write("\n".join(results))
    print(f"Results saved successfully to: Results/search_results.txt")


def write_results_csv(results: list, file_purpose: str, file_path: str):
    if file_purpose == "search":
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        fields = [
            "search",
            "title",
            "list_price",
            "unit_price",
            "unit",
            "on_sale",
            "discount",
            "store",
        ]
    if file_purpose == "watchlist":
        fields = [
            "search",
            "title",
            "list_price",
            "unit_price",
            "unit",
            "on_sale",
            "discount",
            "store",
            "timestamp",
        ]

    with open(file_path, "w+") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for item in results:
            row = {
                "search": item["search"],
                "title": item["title"],
                "list_price": item["list_price"],
                "unit_price": item["unit_price"],
                "unit": item["unit"],
                "on_sale": item["on_sale"],
                "discount": item["discount"],
                "store": item["store"],
            }
            if file_purpose == "watchlist":
                row["timestamp"] = item["timestamp"]
            writer.writerow(row)
    print(f"Results saved successfully to: {file_path}")


def load_watchlist(file_path: str) -> list:
    items = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(
                {
                    "search": row["search"],
                    "title": row["title"],
                    "list_price": row["list_price"],
                    "unit_price": row["unit_price"],
                    "unit": row["unit"],
                    "on_sale": row["on_sale"],
                    "discount": row["discount"],
                    "store": row["store"],
                    "timestamp": row["timestamp"],
                }
            )
    return items
