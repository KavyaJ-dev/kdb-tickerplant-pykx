/ ---- tp.q : tickerplant, the pub/sub hub that receives ticks and forwards them ----

/ define an empty trade table: time, sym (ticker), price, size
trade:flip `time`sym`price`size!(`timestamp$();`symbol$();`float$();`long$());

/ list of connection handles for everyone subscribed (starts empty)
subs:`int$();

/ a client calls this to subscribe: .z.w is the caller's handle, stored once; returns an empty schema
sub:{subs::distinct subs,.z.w; 0#trade};

/ send a batch to every subscriber; neg[h] means an async (non-blocking) message
pub:{[t;x] {[h;t;x] neg[h](`upd;t;x)}[;t;x] each subs};

/ core update function: whatever arrives gets published to subscribers
upd:{[t;x] pub[t;x]};

/ entry point for our Python feed: stamps the time here with .z.p, like a real tickerplant
feed:{[s;p;z] upd[`trade;(enlist .z.p;enlist s;enlist p;enlist z)]};

/ when a client disconnects, .z.pc fires: remove its handle from the subscriber list
.z.pc:{subs::subs except x};