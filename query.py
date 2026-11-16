# import pandas so we can control how DataFrames are printed
import pandas as pd
# import PyKX to talk to the aggregator
import pykx as kx

# make pandas print wide tables on one line instead of hiding columns with "..."
pd.set_option('display.width', 200)
# show every column, never truncate
pd.set_option('display.max_columns', None)

# connect to the aggregator on port 5011
agg = kx.SyncQConnection(host='localhost', port=5011)

# run bars[] inside the aggregator and convert the result to a pandas DataFrame
print(agg('bars[]').pd())

# count how many ticks have arrived per ticker
print(agg('select n:count i by sym from trade').pd())

# close the connection
agg.close()