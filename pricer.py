from arg_parser import get_args
from barbora import get_barbora
from rimi import get_rimi
from process_results import process_results


def main():
    '''
    -Get User Input
    (command line program)

    -Grab data for item

    -Sort data

    -Return items


    FURTHER FUNCTIONS:
    -Import list of items
    -Choose to sort by list price or unit price
    -Save watch list
        -Track if price goes up/down from last fetch
        -Save history of price data?
    -Create list in program

    -Make results more robust such as sorting by similarity to search term    
    '''
    args = get_args()

    if args.search:
        barbora_list = get_barbora(args.search)
        print("Barbora search completed")
        rimi_list = get_rimi(args.search)
        print("Rimi search completed\n")
        if barbora_list or rimi_list:
            cheapest_items, options = process_results(barbora_list + rimi_list, args.order)
            print(cheapest_items)
            print(options)
        else:
            print(f"No Results for search: '{args.search}'")



if __name__ == "__main__":
    main()