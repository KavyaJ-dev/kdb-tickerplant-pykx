/ ---- agg.q : subscribes to the tickerplant and builds live 1-minute bars ----

/ open a connection to the tickerplant on port 5010
tp:hopen 5010;

/ subscribe; the tickerplant returns an empty trade table, which becomes our local table
trade:tp"sub[]";

/ the tickerplant calls this on every publish; append the new rows to our table
upd:{[t;x] t insert x};

/ compute OHLC, volume and VWAP per ticker per minute (like SQL GROUP BY sym, minute)
bars:{select o:first price, h:max price, l:min price, c:last price, vol:sum size, vwap:size wavg price by sym, bar:1 xbar time.minute from trade};