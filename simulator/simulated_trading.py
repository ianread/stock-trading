import hashlib
import hmac
import time
import requests
import json
from enum import Enum
from websocket import create_connection
import pylab as plt
import random
import collections

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# Filled Enum type
class Filled(Enum):
    NOT_FILLED = 1
    OPEN = 2
    CLOSED = 3

# what is the type of order
class Type(Enum):
    BUY = 1
    SELL = 2

# order class
class Order_Class(object):

    def __init__(self, buy_price, quantity, type_buy_sell):
        self.symbol = "XBTUSD"
        self.type = type_buy_sell
        self.buy_price = buy_price
        self.quantity = quantity
        self.order_date = int('{0:.0f}'.format((time.time()+5)*1000))
        self.filled = Filled.NOT_FILLED

class Simulated_Trading:

    # initiate a simulated trading environment
    def __init__(self):
        self.order_array = []
        self.personal_xbt = 0.2311
        self.profit = 0

    def __check_unavaliable(self):
        unavaliable_xbt = 0
        for o in self.order_array:
            if o.filled == Filled.NOT_FILLED:
                unavaliable_xbt += float(o.quantity)/float(o.buy_price)
        return unavaliable_xbt

    def __check_profit(self, last_price, order_array):

        if (order_array == []):
            return (0,0)

        unavaliable_xbt = 0

        total_buy = 0
        total_buy_price = 0

        total_sell = 0
        total_sell_price = 0

        for o in self.order_array:
            if o.filled == Filled.OPEN:
                if o.type == Type.BUY:
                    total_buy += o.quantity
                    total_buy_price += (o.quantity * o.buy_price)
                elif o.type == Type.SELL:
                    total_sell += o.quantity
                    total_sell_price += (o.quantity * o.buy_price)

        if(total_buy != 0):
            total_buy_price = total_buy_price/total_buy

        if(total_sell != 0):
            total_sell_price = total_sell_price/total_sell

        net_total = total_buy - total_sell

        if (net_total > 0):
            if(total_sell != 0):
                return (((1.0/float(total_buy_price) - 1.0/float(total_sell_price)) * total_sell), (((1.0/float(total_buy_price)) - (1.0/float(last_price))) * net_total))
            else:
                return (0, (((1.0/float(total_buy_price)) - (1.0/float(last_price))) * net_total))
        elif (net_total < 0):
            if(total_buy != 0):
                return (((1.0/float(total_buy_price) - 1.0/float(total_sell_price)) * total_buy), (((1.0/float(last_price)) - (1.0/float(total_sell_price))) * -1 * net_total))
            else:
                return (0, (((1.0/float(last_price)) - (1.0/float(total_sell_price))) * -1 * net_total))
        elif not(total_buy == 0) and not (total_sell == 0):
            return (((1.0/float(total_buy_price) - 1.0/float(total_sell_price)) * total_buy), 0)
        else:
            return (0, 0)

    def place_buy_order(self, last_price, price, amount):
        errors = ""

        unavaliable_open = self.__check_unavaliable()
        unavaliable_sell = self.__check_profit(last_price, self.order_array)

        total_avaliable = (self.personal_xbt + unavaliable_sell[0] - unavaliable_open)

        limit_price = float(last_price)-1.0

        if(price < limit_price):

            if (total_avaliable - ((amount*1.0)/price)) >= 0:
                self.order_array.append(Order_Class(price, amount, Type.BUY))
            else:
                errors += "Can't Buy Order at " +str(price)+ " because it exceeds your total available \n";
        else:
            errors += "Can't Buy Order at " +str(price)+ " because current price is "+str(last_price)+"\n"

        print(errors)

    def place_sell_order(self, last_price, price, amount):

        errors = ""

        unavaliable_open = self.__check_unavaliable()
        unavaliable_sell = self.__check_profit(last_price, self.order_array)

        total_avaliable = (self.personal_xbt + unavaliable_sell[0] - unavaliable_open)

        limit_price = float(last_price)+1.0

        if(price > limit_price):
            if (total_avaliable - ((amount*1.0)/price)) >= 0:
                self.order_array.append(Order_Class(price, amount, Type.SELL))
            else:
                errors += "Can't Sell Order at " +str(price)+ " because it exceeds your total available \n";
        else:
            errors += "Can't Sell Order at " +str(price)+ " because current price is "+str(last_price)+"\n"

    def __check_order(self, last_price):
        for o in self.order_array:
            if o.type == Type.BUY and o.filled == Filled.NOT_FILLED:
                if (float(last_price) <= float(o.buy_price)):
                    o.filled = Filled.OPEN
            elif o.type == Type.SELL and o.filled == Filled.NOT_FILLED:
                if (float(last_price) >= float(o.buy_price)):
                    o.filled = Filled.OPEN

    #this function must be called in the loop
    def update_loop(self, last_price):
        self.__check_order(last_price)
        return self.order_array

    def check_profit(self, last_price):
        return self.__check_profit(last_price, self.order_array)

