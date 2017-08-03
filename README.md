# Stock Trading

Test and Trade different Bitmex Stock market techniques. Virtual trading is provided by the simulator. Actual trading is provided by the api_caller library.

### Tips

  - Run the main_tests function to see if you have all of the modules installed
  - By default all of the tests should be turned on, to check this check the ```test_array``` variable to see if all of the elements are set to 1 (1 means on, anything else means off, usually 0)
  - Some of the tests take time so you can turn them off by setting that element of the array to zero

## API Caller

#### Streaming

The streaming class connects to the Bitmex api, https://www.bitmex.com/api/explorer/, and streams all relevant data for the Exchange

The methods within the Streaming class include:

 - [x] subscribe_price() - for starting a price connection
 - [x] subscribe_orderbook() - for starting an orderbook connection
 - [x] update_price() - for updating the current prices of the Subscribe object
 - [x] update_orderbook() - for updating the current Orderbook (list of all the active orders at a given time)
 - [x] close_price_connection() - for closing the websocket connection to the price stream
 - [x] close_orderbook_connection() - for closing the websocket connection to the Orderbook stream

TODO: Update README for Trading Object and finish the simulator as well

## Simulator

#### Simulated Streaming

The simulated streaming creates a series of potential bitcoin trading prices.

The methods within the Simulated Streaming class include:

  - [x] subscribe_price(start_price) - for starting a PSEUDO price connection
  - [x] update_price() - for updating the current prices of the Simulated_Subscribe object
  - [x] close_price_connection() - for closing the object (Doesn't actually do anything, just for consistency's sake)
