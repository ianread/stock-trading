import hashlib
import hmac
import time
import requests
import json
from enum import Enum
from websocket import create_connection

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

class TickDirection(Enum):
    MinusTick = -2
    ZeroMinusTick = -1
    ZeroTick = 0
    ZeroPlusTick = 1
    PlusTick = 2

class Order_Book_Value(object):
    def __init__(self, id, price, size, side):
        self.id = id
        self.price = price
        self.size = size
        self.side = side

# Class to call the streaming function for the BITMEX Trader
class Streaming:
    def __init__(self):

        # bitcoin socket
        self.ws_bitcoin = create_connection("wss://www.bitmex.com/realtime")
        self.ws_order_book = create_connection("wss://www.bitmex.com/realtime")

        # order book
        self.order_book = dict()

        # stock prices
        self.midPrice = None
        self.lastPrice = None
        self.fairPrice = None
        self.last_tick_direction = None
        self.last_change_percentage = None

    # private method to created enumerated tick type
    def __create_enumerated(self, string_val):
        if string_val == "MinusTick":
            return TickDirection.MinusTick
        elif string_val == "ZeroMinusTick":
            return TickDirection.ZeroMinusTick
        elif string_val == "ZeroPlusTick":
            return TickDirection.ZeroPlusTick
        elif string_val == "PlusTick":
            return TickDirection.PlusTick
        else: # default return
            return TickDirection.ZeroTick

    # call this first to open the websocket for the price
    def subscribe_price(self):
        self.ws_bitcoin.send('{"op": "subscribe", "args": ["instrument:XBTUSD"]}')

        result =  self.ws_bitcoin.recv()
        result =  self.ws_bitcoin.recv()

    # call this first to open the websocket for the orderbook
    def subscribe_orderbook(self):
        self.ws_order_book.send('{"op": "subscribe", "args": ["orderBookL2:XBTUSD"]}')

        result =  self.ws_order_book.recv()
        result =  self.ws_order_book.recv()
        result =  self.ws_order_book.recv()

        result_orderbook = json.loads(result)["data"]

        for r in result_orderbook:
            self.order_book[r["id"]] = Order_Book_Value(r["id"], r["price"], r["size"], r["side"])

    # put this in an infinite loop to receive the updated values
    def update_price(self):
        result =  self.ws_bitcoin.recv()

        # get midPrice
        try:
            self.midPrice = float(json.loads(result)["data"][0]["midPrice"])
        except:
            pass

        # get lastPrice
        try:
            self.lastPrice = float(json.loads(result)["data"][0]["lastPrice"])
        except:
            pass

        # get lastPrice
        try:
            self.fairPrice = float(json.loads(result)["data"][0]["fairPrice"])
        except:
            pass

        # get last tick direction
        try:
            self.last_tick_direction = self.__create_enumerated(str(json.loads(result)["data"][0]["lastTickDirection"]))
        except:
            pass


        # get last tick direction
        try:
            self.last_change_percentage = float(json.loads(result)["data"][0]["lastChangePcnt"])
        except:
            pass

        return_dictionary = dict()

        return_dictionary["midPrice"] = self.midPrice
        return_dictionary["lastPrice"] = self.lastPrice
        return_dictionary["fairPrice"] = self.fairPrice
        return_dictionary["last_tick_direction"] = self.last_tick_direction
        return_dictionary["last_change_percentage"] = self.last_change_percentage

        # return value of streaming
        return return_dictionary

    # def update orderbook
    def update_orderbook(self):
        result =  self.ws_order_book.recv()
        result_orderbook = json.loads(result)

        if(result_orderbook["action"] == "update"):

            data_here = result_orderbook["data"]

            for d in data_here:
                price_data = self.order_book[d["id"]].price
                size_data = self.order_book[d["id"]].size
                side_data = self.order_book[d["id"]].side

                try:
                    price_data = d["price"]
                except:
                    pass

                try:
                    size_data = d["size"]
                except:
                    pass

                try:
                    side_data = d["side"]
                except:
                    pass

                self.order_book[d["id"]].price = price_data
                self.order_book[d["id"]].size = size_data
                self.order_book[d["id"]].side = side_data

        elif(result_orderbook["action"] == "insert"):
            data_here = result_orderbook["data"]

            for d in data_here:
                self.order_book[d["id"]] = Order_Book_Value(d["id"], d["price"], d["size"], d["side"])

        elif(result_orderbook["action"] == "delete"):
            data_here = result_orderbook["data"]

            for d in data_here:
                del self.order_book[d["id"]]

        return self.order_book

    # to tidy up the price connection, call this function
    def close_price_connection(self):
        self.ws_bitcoin.close()

    # to tidy up the orderbook connection, call this function
    def close_orderbook_connection(self):
        self.ws_bitcoin.close()

