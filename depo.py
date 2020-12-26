#!/bin/python

from util import *

# config:
# type 1: list of letters (numbers)
# type 2: period length, n, p
print_type = 2

# use global variable to store all the sequences found upto now
#
# The list contains pairs (a, ap) where A is the period of the sequence
# and AP is sequence where each letter is replaced by the length of its period.
#
sequences_list = []

# check_and_normalize
#
# if incorrect, return None
#
def check_and_normalize(prefix, first, period):
    assert len(first) == len(period)
    assert all([p > 0 for p in period])
    # compute the length of the whole period
    per = nsn(period)
    a  = [-1] * per
    ap = [0] * per
    for i in range(len(first)):
        j = first[i]
        while j < per:
            # check for conflict - incorrect specification:
            if a[j] != -1:
                return None
            a[j] = i
            ap[j] = period[i]
            j += period[i]
    # check the specification - are all positions filled?
    if any([c == -1 for c in a]):
        return None
    # Oll Korrect
    return (a, ap)

# check that the sequence is new
# if yes, add it to the list of knows sequenes (and print it)
def store_seq(prefix, first, period):
    ret = check_and_normalize(prefix, first, period)
    if ret is None:
        return
    a, ap = ret
    # check if the sequence is already known
    for a1, ap1 in sequences_list:
        if are_equal(ap, ap1):
            return
    # A new one!
    sequences_list.append( (a, ap) )
    if print_type == 1:
        print('SEQ: ' + str(a) + '*')
    else:
        print_n_p(first, period)

def print_n_p(first, period):
    print("seq with period length {}".format(nsn(period)))
    print("  n: " + format_num(first))
    print("  p: " + format_num(period))

def format_num(seq):
    txt = ["{:2d}".format(i) for i in seq]
    return " ".join(txt)

def print_summary(num_letters):
    print("\nFor alphabet size {}, we found {} words.".format(num_letters, len(sequences_list)))
