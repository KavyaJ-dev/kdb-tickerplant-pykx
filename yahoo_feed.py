# import yfinance, which includes a WebSocket client for Yahoo's live price stream
import yfinance as yf
# import PyKX so we can send each tick to the tickerplant
import pykx as kx

# connect to the tickerplant (tp.q must already be running on port 5010)
tp = kx.SyncQConnection(host='localhost', port=5010)

# tickers to stream; BTC-USD trades 24/7 so you can test when stock markets are closed
SYMBOLS = ['AAPL', 'MSFT', 'GOOG', 'BTC-USD']

# remembers each ticker's previous cumulative day volume, used to work out trade size
last_volume = {}

# this function runs once for every message Yahoo pushes to us
def handle(msg):
    # print the raw message so you can see Yahoo's field names (delete this line later)
    print(msg)
    # get the ticker name from the message ('id' is Yahoo's field for the symbol)
    sym = msg.get('id')
    # get the latest traded price
    price = msg.get('price')
    # skip messages that don't carry a symbol and a price (such as heartbeats)
    if sym is None or price is None:
        return
    # Yahoo sends cumulative volume for the day; numbers may arrive as strings, so convert safely
    day_vol = int(float(msg.get('day_volume') or 0))
    # look up the previous cumulative volume for this ticker (first tick: assume no change)
    prev = last_volume.get(sym, day_vol)
    # the difference approximates the size of this trade (never negative)
    size = max(day_vol - prev, 0)
    # store the new cumulative volume for next time
    last_volume[sym] = day_vol
    # call feed[sym;price;size] on the tickerplant, which timestamps and publishes it
    tp('feed', kx.SymbolAtom(sym), float(price), size)

# try/finally so the tickerplant connection closes cleanly on Ctrl+C
try:
    # open the Yahoo WebSocket connection (closes automatically when the block ends)
    with yf.WebSocket() as ws:
        # tell Yahoo which tickers we want
        ws.subscribe(SYMBOLS)
        # block here forever, calling handle() for every incoming message
        ws.listen(handle)
finally:
    # close our connection to the tickerplant
    tp.close()