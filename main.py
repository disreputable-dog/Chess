# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:06:21 2019

@author: georg
"""

import board_class

response = None

while response not in range(1,4):
    response = int(input("Enter 1 for PvP, 2 for PvAI, 3 for AIvAI: "))

board_obj = board_class.Game(8, response)
outcome = board_obj.main(response)
print(outcome)