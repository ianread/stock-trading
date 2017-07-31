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

# Class to call the streaming function for the BITMEX Trader
class Streaming:
    def __init__(self):

        # bitcoin socket
        self.ws_bitcoin = create_connection("wss://www.bitmex.com/realtime")

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
        elif string_val == "ZeroTick":
            return TickDirection.ZeroTick
        elif string_val == "ZeroPlusTick":
            return TickDirection.ZeroPlusTick
        elif string_val == "PlusTick":
            return TickDirection.PlusTick

        # default return
        return TickDirection.ZeroTick

    # call this first to open the websocket
    def subscribe_price(self):
        self.ws_bitcoin.send('{"op": "subscribe", "args": ["instrument:XBTUSD"]}')
        result =  self.ws_bitcoin.recv()
        result =  self.ws_bitcoin.recv()

    # put this in an infitite loop to recieve the updated values
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

    # to tidy up the connection, call this function
    def close_connection(self):
        self.ws_bitcoin.close()
