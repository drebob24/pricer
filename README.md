# PRICER - Price Comparison Tool

A price comparison tool that takes inputs of a list of items and retrieves data from different Lithuanian stores (Barbora and Rimi) and outputs the results. It also supports the ability to store a watchlist and directly compare a total price between the stores.

This is largely a proof of concept program not intended for mass use since it is scraping data.

## Features

- **Item Search**: Search for items across two different stores.
- **Price Comparison**: Compare the total cost of a list of items across both stores.
- **Watchlist Management**: Add, update, or remove items in a watchlist.
- **Historical Data Storage**: Optionally store price history in a file.

## Requirements

- Python 3.6+
- `argparse` module
- some understanding of Lithuanian, English searches will not yield good results

## Usage

--items -i: Accepts a list of string values (e.g., --items item1 item2 item3). Currently limited to 10 items.

--file -f: Accepts a file path to load in a list of items (expects a txt file). Currently limited to 10 items.

--search-watchlist: Load list of items from the watchlist to perform search or compare.

--search -s: Run a basic search and return results for each individual item.

--compare: Run a total cost comparison either combining prices across both stores with 'together', or 'seperate' gives total cost per store separately.

--watchlist: Create/Add to a watchlist using 'add' and either the --items or --file argument to pass in items. 'update' will update the watchlist with the option to store old data with the --store-history arg. Remove items from the watchlist with 'remove' and the --items or --file argument.

--order: Choose 'list' to sort by the listed item price (e.g., 5 EUR/1 bag (30g)), or 'unit' price to sort by the price per unit (e.g., 10 EUR/kg). Default is unit price.

--results: Number of results to return. Default is 3. Expanding much above 3-5 is likely to bring in a lot of unwanted results depending on the search.

--save: Save results as either TXT or in a CSV. CSV is not compatible with compare mode due to the resulting data.

--store-history: Flag to store historical data when updating the watchlist with --watchlist update.

**Example Commands**
Search for items:
python pricer.py --items apple banana --search

Compare prices together:
python pricer.py --items apple banana --compare together

Add items to watchlist:
python pricer.py --items apple banana --watchlist add

Update watchlist with historical data storage:
python pricer.py --watchlist update --store-history

## Limitations

Most obviously since this relies on scraping, scaling to a more used program would run into results with http requests.
Also any changes to the used web sources could easy break the program.

Price Comparisons need to be made a lot more robust to fully work for a large shopping list. 
Items of different unit amounts (vnt vs kg) do not really directly compare and would need to be handled differently.
For instance, when searching for coffee, coffee pods with a unit price per vnt (pod) ends up significantly cheaper than ground coffee, even though the ground coffee is much cheaper as far as cost/cup of coffee.

Item comparisons are fairly rudementary. Some level of string comparison is needed ensure similar products are being compared.
Right now the program largely relies on how the sources do their own relevancy sorting but even then comparisons often get skewed by a barely related product.

## Future Development Ideas

Add Ability to email results to yourself.

Make price comparison more robust accounting for both the unit_price and the list_price as needed: When comparing the stores it would better to compare total unit price and use that as the basis for the cheaper store, but also provide the total price you would directly pay.

Add ability to track a specific product and not just items based off a search term, based off the product title and likely the internal product that can be grabbed from the sources.
--This would also allow for the ability to track if item is in stock/out of stock

Add "relevancy" field using either a python library to compare strings or potentially AI? Not sure how well AI handles Lithuanian.

Specific code reworking:
handle_item_search() could be cleaned up/split up a bit.
process_results() should be reworked to only return json styled data for better modularity, then splitting it into strings is handled in another function.

