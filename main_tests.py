from api_caller.streaming import Streaming
from api_caller.streaming import TickDirection
from api_caller.streaming import Order_Book_Value

from simulator.simulated_streaming import Simulated_Streaming
from simulator.simulated_trading import Filled
from simulator.simulated_trading import Type
from simulator.simulated_trading import Order_Class
from simulator.simulated_trading import Simulated_Trading


# Array to run tests (currently only one test)
# [test_streaming]
test_array = [1, 1, 1, 1]

# run tests here
def main_tests():

    global test_array

    # test if the live streaming of the price works
    if(test_array[0] == 1):
        # check streaming object
        print("Creating new object and subscribing")
        new_streaming_object = Streaming()
        new_streaming_object.subscribe_price()

        # check the data coming in for 50 times
        for x in range(1, 50):
            print(new_streaming_object.update_price())

        # close the web socket connection
        print("Closing Web Connection")
        new_streaming_object.close_price_connection()

    # check if the order book works
    if(test_array[1] == 1):

        # check streaming object
        print("Creating new object and subscribing")
        new_streaming_object = Streaming()
        new_streaming_object.subscribe_orderbook()

        # check the data coming in for 50 times
        for x in range(1, 50):
            print(new_streaming_object.update_orderbook())

        # close the web socket connection
        print("Closing Web Connection")
        new_streaming_object.close_orderbook_connection()

    # check if the simulated price works
    if(test_array[2] == 1):

        # check streaming object
        print("Creating new simulated object and subscribing")
        new_streaming_object = Simulated_Streaming()
        new_streaming_object.subscribe_price()

        # check the data coming in for 50 times
        for x in range(1, 50):
            print(new_streaming_object.update_price())

        # close the web socket connection
        print("Closing Web Connection")
        new_streaming_object.close_price_connection()

    # check if the simulated price works
    if(test_array[3] == 1):

        print("Creating new Simulated Trading object")
        simulated_trading = Simulated_Trading()

        print("Creating new object and subscribing")
        new_streaming_object = Streaming()
        new_streaming_object.subscribe_price()

        # check the data coming in for 50 times
        for x in range(1, 50):
            returned_price_obj = new_streaming_object.update_price()

            simulated_trading.place_buy_order(returned_price_obj["lastPrice"], 3400.0, 1)
            print(simulated_trading.update_loop(returned_price_obj["lastPrice"]))
            print(simulated_trading.check_profit(returned_price_obj["lastPrice"]))

            print(returned_price_obj)

        # close the web socket connection
        print("Closing Web Connection")
        new_streaming_object.close_price_connection()

if __name__ == "__main__":
    main_tests()
