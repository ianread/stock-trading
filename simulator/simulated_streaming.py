import hashlib
import hmac
import time
import requests
import random
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

class Simulated_Streaming:
    def __init__(self):

        # stock prices
        self.midPrice = None
        self.lastPrice = None
        self.fairPrice = None
        self.last_tick_direction = None
        self.last_change_percentage = None

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

    def subscribe_price(self, start_price=2300):

        self.midPrice = start_price + ((random.randint(-10, 10)*1.0)/10.0)
        self.lastPrice = start_price
        self.fairPrice = start_price + (random.randint(3,8)/10.0)

        self.last_tick_direction = TickDirection.ZeroTick

        self.last_change_percentage = 0.0

    # updated prices
    def update_price(self):

        set_price = self.lastPrice

        test_variable = random.randint(1, 10)

        if (test_variable == 1):

            new_test_var = random.randint(1, 10)

            if (new_test_var == 1):
                self.lastPrice = set_price - (random.randint(40, 100)/10.0)
            elif (new_test_var == 2 or new_test_var == 3):
                self.lastPrice = set_price - (random.randint(25, 55)/10.0)
            else:
                self.lastPrice = set_price - (random.randint(10, 30)/10.0)

        elif (test_variable == 2 or test_variable == 3):
            self.lastPrice = set_price - (random.randint(1,10)/10.0)
        elif (test_variable == 4 or test_variable == 5 or test_variable == 6 or test_variable == 7):
            self.lastPrice = set_price + (random.randint(-5,5)/10.0)
        elif (test_variable == 8 or test_variable == 9):
            self.lastPrice = set_price + (random.randint(1,10)/10.0)
        else:
            new_test_var = random.randint(1, 10)
            if (new_test_var == 1):
                self.lastPrice = set_price + (random.randint(40, 100)/10.0)
            elif (new_test_var == 2 or new_test_var == 3):
                self.lastPrice = set_price + (random.randint(25, 55)/10.0)
            else:
                self.lastPrice = set_price + (random.randint(10, 30)/10.0)

        self.midPrice = self.lastPrice - (random.randint(1,5)/10.0)
        self.fairPrice = self.lastPrice - (random.randint(3,8)/10.0)

        if(set_price < self.lastPrice):
            self.last_change_percentage = float(self.lastPrice - set_price)
            self.last_tick_direction = TickDirection.MinusTick
        elif(set_price > self.lastPrice):
            self.last_change_percentage = float(set_price - self.lastPrice)
            self.last_tick_direction = TickDirection.PlusTick
        else:
            self.last_change_percentage = float(0.0)

            if self.last_tick_direction == TickDirection.PlusTick:
                self.last_tick_direction = TickDirection.ZeroPlusTick
            elif self.last_tick_direction == TickDirection.MinusTick:
                self.last_tick_direction = TickDirection.ZeroMinusTick
            else:
                self.last_tick_direction = TickDirection.ZeroTick


        return_dictionary = dict()

        return_dictionary["midPrice"] = self.midPrice
        return_dictionary["lastPrice"] = self.lastPrice
        return_dictionary["fairPrice"] = self.fairPrice
        return_dictionary["last_tick_direction"] = self.last_tick_direction
        return_dictionary["last_change_percentage"] = self.last_change_percentage

        return return_dictionary

    def close_price_connection(self):
        return "Successfully closed orderbook connection"

