from arg_parser import get_args
from barbora import get_barbora
from rimi import get_rimi


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
    '''
    args = get_args()

    if args.search:
        barbora_list = get_barbora(args.search)
        rimi_list = get_rimi(args.search)
        print(barbora_list)
        print(rimi_list)



if __name__ == "__main__":
    main()