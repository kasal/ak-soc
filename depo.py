#!/bin/python

from util import *

# use global variable to store all the sequences found upto now
#
# The loist contains pairs (a, ap) where A is the period of the sequence
# and AP is sequence where each letter is replaced by the length of its period.
#
deposit_list = []

# check and normalize
#
def check_normalize(prefix, first, period):
    assert len(first) = len(period)
    # compute the length of the whole period
    per = nsn(period)
    txt = [0] * per
    for i in range(len(first)):
        j = first[i]
        while j < per:
            txt[
