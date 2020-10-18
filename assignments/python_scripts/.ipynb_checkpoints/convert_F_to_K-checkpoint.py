#!/usr/bin/env python3
#https://github.com/jekuszynski/bch5884jek/tree/master/assignments
# -*- coding: utf-8 -*-

print("What is the temperature in \u2109 ?:")
t = input()
c = round(((int(t)-32)*(5/9))+273.15,3)
print("The temperature in K is: " + str(c))