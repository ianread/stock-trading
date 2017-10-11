import threading
import copy
import numpy as np
import collections

from api_caller.streaming import Streaming
from api_caller.streaming import TickDirection
from api_caller.streaming import Order_Book_Value

bitcoin_price = None
order_book = None

processed_order_book_buy = None
processed_order_book_sell = None

running_bool = True

d = collections.deque(maxlen=1000)

def set_price():
    global bitcoin_price
    global running_bool

    print("Creating new Price Object")
    new_streaming_object = Streaming()
    new_streaming_object.subscribe_price()

    while running_bool:
        bitcoin_price = new_streaming_object.update_price()

    new_streaming_object.close_price_connection()


def set_order_book():
    global bitcoin_price
    global order_book
    global running_bool

    global processed_order_book_buy
    global processed_order_book_sell

    print("Creating new Streaming Object")
    new_streaming_object = Streaming()
    new_streaming_object.subscribe_orderbook()

    while running_bool:
        order_book = new_streaming_object.update_orderbook()

        if(order_book != None and bitcoin_price != None):
            if(len(order_book) > 0 ):
                buy_side = [ r for k,r in order_book.iteritems() if(r.side == 'Buy')]
                sell_side = [ r for k,r in order_book.iteritems() if(r.side == 'Sell')]

                buy_side.sort(key=lambda x: (bitcoin_price["lastPrice"] - x.price), reverse=False)
                sell_side.sort(key=lambda x: (x.price - bitcoin_price["lastPrice"]), reverse=False)

                processed_order_book_buy = buy_side[0:200]
                processed_order_book_sell = sell_side[0:200]

    new_streaming_object.close_orderbook_connection()

def print_order_book():
    global bitcoin_price
    global processed_order_book_buy
    global processed_order_book_sell
    global running_bool

    while running_bool:
        if(processed_order_book_buy != None and processed_order_book_sell != None):
            buy_side = [[x.price, x.size] for x in processed_order_book_buy]
            sell_side = [[x.price, x.size] for x in processed_order_book_sell]
            current_price = bitcoin_price["lastPrice"]

            total_np_array = np.array(buy_side + sell_side)

            flattened_array = total_np_array.flatten().tolist() + [current_price]

            d.append(flattened_array)

            print(len(d[0]))

def cancel_trading():
    global running_bool

    running_bool = False

def created_windowed_data():

    pass

def boosted_tree():
    pass

s_p = threading.Thread(target=set_price)
o_b = threading.Thread(target=set_order_book)
p_o_b = threading.Thread(target=print_order_book)

# set trading to be 10 seconds
c_t = threading.Timer(10.0, cancel_trading)

s_p.start()
o_b.start()
p_o_b.start()
c_t.start()
