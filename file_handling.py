import csv
import os


def read_item_file(file_path: str) -> list:
    with open(file_path, "r") as file:
        items = [line.strip() for line in file]
    return items


def write_results_txt(results: list):
    with open("Results/search_results.txt", "w", newline='') as file:
        file.write("\n".join(results))
    print(f"Results saved successfully to: Results/search_results.txt")


def write_results_csv(results: list):
    file_path = "Results/search_results.csv"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "search",
                "title",
                "list_price",
                "unit_price",
                "unit",
                "on_sale",
                "discount",
                "store",
            ],
        )
        writer.writeheader()
        for item in results:
            writer.writerow(
                {
                    "search": item["search"],
                    "title": item["title"],
                    "list_price": item["list_price"],
                    "unit_price": item["unit_price"],
                    "unit": item["unit"],
                    "on_sale": item["on_sale"],
                    "discount": item["discount"],
                    "store": item["store"],
                }
            )
    print(f"Results saved successfully to: {file_path}")
