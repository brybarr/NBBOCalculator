import socket

host = '<put host>'
port = '<put port>'

def calculate_nbbo(symbol):
    bids = []
    asks = []

    for data in market_data[symbol].values():
        bids.append(data['bid'])
        asks.append(data['ask'])

    best_bid = max(bids)
    best_ask = min(asks)

    return best_bid, best_ask

def update_quotes(symbol, exchange, bid, ask):
    if symbol not in market_data:
        market_data[symbol] = {}

    market_data[symbol][exchange] = {'bid': bid, 'ask': ask}

def main():
    global market_data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while s:
            data = s.recv(1024).decode('utf-8')
            if data.startswith("Q|"):
                quotes = data.split("\n")
                print(f'Quotes: {quotes}')
                symbol_list = []
                market_data = {}

                for quote in quotes:
                    if quote:
                        symbol, exchange, bid, ask = quote.split('|')[1:]
                        update_quotes(symbol, exchange, bid, ask)
                        symbol_list.append(symbol)

                for symbol in set(symbol_list):
                    best_bid, best_ask = calculate_nbbo(symbol)
                    print(f"Symbol {symbol}: Best Bid is {best_bid}, Best ask is {best_ask}")

if __name__ == "__main__":
    main()
