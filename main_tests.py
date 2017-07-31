from api_caller.streaming import Streaming
from api_caller.streaming import TickDirection


# Array to run tests (currently only one test)
# [test_streaming]
test_array = [1]

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

if __name__ == "__main__":
    main_tests()
