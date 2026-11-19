# I want to build a price fetcher that works with two api's: one for id name and the other for prices and whatnot
# Two ways of getting said price
# 1. Manual lookup
# 2. Searching --Done this


import requests

coin_url = 'https://api.coingecko.com/api/v3/simple/price' # Endpoint for Coin Prices and 24hour comparison variables.
id_url = 'https://api.coingecko.com/api/v3/coins/list' # Endpoint for ID's, symbols, whatnot.


# 1. Extract all the id data from id_url. then save the id's inside a variable.
id_response = requests.get(id_url, timeout=10) # returns a server response
id_data = id_response.json() # converts server response to JSON

# 2. Pagination. I want 25 coins on a page.
page = 1
per_page = 25

is_running = True
current = id_data
match = None

def show_coins(rows, page, total_pages):
    
    for index, coin in enumerate(rows, start=1):
        print(f"{index:>3} {coin['symbol']:<15} : {coin['name']:.30}")

    print(f'Page {page} of {total_pages}')

def show_coin(coin_id, coin_url):
    print('--------------------' + 'Selected Coin' + '--------------------')
    print(f'Coin ID: {coin_id}')

    coin_response = requests.get(coin_url, params={'ids':coin_id, 'vs_currencies':'usd'}, timeout=10)
    coin_data = coin_response.json()

    print(f"Price: {coin_data[coin_id]['usd']}")

while is_running:
    window = current[(page-1) * per_page : (per_page * page)]
    total_pages = ((len(current) + per_page - 1)//per_page)
    show_coins(window, page, total_pages)
    # print(f'page {page} of {total_pages}')

    instructions = input(

        '''
            Click:
            1. n - To proceed to next page
            2. p - to go to previous page
            3. s - to search the program
            4. b - to go back to searching for coins
            5. q - to exit the progran

        '''
    ).lower()

    if instructions.isdigit():
        num = int(instructions) - 1
        if 0 <= num < len(window):
            selected_coin = window[num]
            show_coin(selected_coin['id'], coin_url)
        else:
            print(f"Valid range is between 1 and {len(window)}")

    if instructions == 'n' and page < total_pages: page += 1
    elif instructions == 'p' and page > 1: page -= 1
    # Pagination done.
    elif instructions == 's':
        match = None
        what_coin = input('Enter Coin ID: ')
        for index, coin in enumerate(id_data):
            if coin['id'] == what_coin:
                match = coin
                break
        if match is None:
            print('Coin not found!')
        else:
            current = [match]
            page = 1
    elif instructions == 'b':
        current = id_data
        page = 1
    elif instructions == 'q': is_running = False
