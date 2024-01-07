import requests

my = input().lower()
req = requests.get(f'http://www.floatrates.com/daily/{my}.json').json()
rates = {
    "usd": 1 if my == 'usd' else req['usd']['rate'],
    "eur": 1 if my == 'usd' else req['eur']['rate'],
}
while True:
    currency = input().lower()
    if currency == '':
        break
    amount = float(input())
    print('Checking the cache...')
    print(f'{"Oh! It is in the cache!" if currency in rates.keys() else "Sorry, but it is not in the cache!"}')
    rates[currency] = req[currency]['rate']
    print(f'You received {amount * rates[currency]} {currency.upper()}')
