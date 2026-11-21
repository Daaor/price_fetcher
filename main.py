# I want to build a price fetcher that works with two api's: one for id name and the other for prices and whatnot
# Two ways of getting said price
# 1. Manual lookup
# 2. Searching --Done this


import requests
import sys

coin_url = 'https://api.coingecko.com/api/v3/simple/price' # Endpoint for Coin Prices and 24hour comparison variables.
id_url = 'https://api.coingecko.com/api/v3/coins/list' # Endpoint for ID's, symbols, whatnot.


# 1. Extract all the id data from id_url. then save the id's inside a variable.
try:
    id_response = requests.get(id_url, timeout=10) # returns a server response
    id_response.raise_for_status()
    id_data = id_response.json() # converts server response to JSON
except requests.exceptions.ConnectionError:
    sys.exit("No Net. Try again later.")
except requests.exceptions.HTTPError as e:
    print(f"Server raised a '{e}'")
except requests.exceptions.Timeout:
    sys.exit('The server did not respond on time. Please, try again.')

# 2. Pagination. I want 25 coins on a page.
page = 1
per_page = 25

is_running = True
current = id_data
match = []

def show_coins(rows, page, total_pages):
    
    for index, coin in enumerate(rows, start=1):
        print(f"{index:>3} {coin['symbol']:<15} : {coin['name']:.30}")

    print(f'Page {page} of {total_pages}')

def show_coin(coin_id, coin_url):
    print('--------------------' + 'Selected Coin' + '--------------------')
    print(f'Coin ID: {coin_id}')


    try:
        coin_response = requests.get(coin_url, params={'ids':coin_id, 'vs_currencies':'usd'}, timeout=10)
        coin_response.raise_for_status()
        coin_data = coin_response.json()
        print(f"Price: {coin_data[coin_id]['usd']}")
    except requests.exceptions.ConnectionError:
        print('No Good Internet. Please try again.')
    except requests.exceptions.Timeout:
        print('Server did not respond on time. Please try again.')
    except requests.exceptions.HTTPError as e:
        print(f"Server raised a '{e}'")
    except KeyError:
        print('Coin has no USD price')

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
            5. q - to exit the program

        '''
    ).lower()

    if instructions.isdigit():
        num = int(instructions) - 1
        if 0 <= num < len(window):
            selected_coin = window[num]
            show_coin(selected_coin['id'], coin_url)
        else:
            print(f"Valid range is between 1 and {len(window)}")
    elif instructions == 'n' and page < total_pages: page += 1
    elif instructions == 'p' and page > 1: page -= 1
    # Pagination done.
    elif instructions == 's':
        match = []
        what_coin = input('Enter Coin ID(bitcoin) or Coin Symbol(btc): or coin name(Bitcoin) ').lower().strip()
        for coin in id_data:
            if what_coin in (coin['id'].lower(), coin['symbol'].lower(), coin['name'].lower()):
                match.append(coin)
        if not match:
            print('Coin not found!')
        else:
            current = match
            page = 1
    elif instructions == 'b':
        current = id_data
        page = 1
    elif instructions == 'q': is_running = False
