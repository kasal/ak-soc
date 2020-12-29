#!/bin/python

import sys
from util import *
from depo import store_seq, print_summary

delka_abecedy = 9
print_debug = False

# increase recursion limit for large alphabets
sys.setrecursionlimit(10**4)

def debug(txt):
    if (print_debug):
        print(txt)

# mod_list .. utility function
#
# Returns a copy of the list, with i-th element set to x.
#
def mod_list(ll, i, x):
    res = ll.copy()
    res[i] = x
    return(res)

# generate .. compute all possible words starting with the given prefix
#
# We extend the prefix and then call generate() recursively.
# If there are more possible ways to continue, we generate several times.
# If the prefix contains contradiction, and no extension of the prefix
# is possible; the function finishes with no recursive call.
#
def generate(prefix, first, period, indent):
    debug(indent+"start generate for {}".format(prefix))
    done = all([x is not None for x in period])
    if (done):
        store_seq(prefix, first, period)
        return
    remaining_fraction = compute_remaining_fraction(period)
    if (remaining_fraction < 0.0000001):
        debug(indent+"unused letters remain")
        return
    #
    # compute all letters determined by the prefix
    #
    while True:
        next_letter = implied_letter(len(prefix), first, period)
        if next_letter is None:
            break
        prefix = prefix + [next_letter]

    # 1) add a new letter, or
    # 2) repeat one of the letters with no period
    #  ==> do 2) first and then 1):  the resulting order of all the
    #      words found is nicer.
    #
    # 2) repeat a letter:
    # Without loss of generality we can assume that 0 has the
    # shortest period.  Thus letter 0 is the first to repeat.
    if (period[0] is None):
        ltrs_to_repeat = [0]
        min_peri = 0
    else:
        min_peri = 1 / (remaining_fraction + 0.000001)  # beware: float arithmetics
        ltrs_to_repeat = [i for i in range(len(first))
                            if ok_to_repeat(i, prefix, first, period, min_peri)]
    debug(indent+"--- to repeat: {} (min_peri={:.2f})".format(ltrs_to_repeat, min_peri))
    for ltr in ltrs_to_repeat:
        new_peri = len(prefix) - first[ltr]
        generate(prefix + [ltr], first.copy(), mod_list(period, ltr, new_peri), indent+'  ')
    #
    # 1) - take the next unused letter: len(first)
    ltr = len(first)
    if (ltr < delka_abecedy):
        generate(prefix + [ltr], first + [len(prefix)], period.copy(), indent+'  ')

# find the letter that must be on position n, if any
#
# There must be at most one, as we cleverly prevent collisions.
#
def implied_letter(n, first, period):
    for i in range(len(first)):
        if (period[i] is not None and n % period[i] == first[i]):
            return i
    return None

# returns True, iff ltr can be used now for the second time
#
def ok_to_repeat(ltr, prefix, first, period, min_period):
    if (period[ltr] is not None):
        return(False)
    new_period = len(prefix) - first[ltr]
    # - period must be > first; if not there would be an obligatory occurence
    # at position first - period
    # - must be at least min_period
    ok = (new_period > first[ltr] and new_period >= min_period)
    if (not ok):
        return(False)
    # Moreover, check for collision with other letters that already have period set:
    letters_with_period_set = [i for i in range(len(first))
                                 if period[i] is not None]
    for i in letters_with_period_set:
        if collides((first[i],period[i]), (first[ltr],new_period)):
            return(False)
    # passes all checks
    return(True)

def collides(ltr_one, ltr_two):
    n1, p1 = ltr_one; n2, p2 = ltr_two
    k = nsd([p1, p2])
    # Look at sub-sequences modulo k.
    # k | p1, so the first letter has all occurences in one of these sub-sequences.
    # Likewise the second letter.  But are both letters in the same sub-sequence?
    same_sub_sequence = (n1 % k) == (n2 % k)
    # If not, they cannot meet.
    # But if they live in the same, they must meet as their relative periods are coprime.
    return(same_sub_sequence)

def compute_remaining_fraction(period):
    # fractions occupied by the letters
    frac = [1/x for x in period if x is not None]
    return(1 - sum(frac))

def main():
    # first .. list containing the position of the first occurence of each letter
    # len(first) .. number of letter used up to now
    # period .. list of period lengths of each character; len(period) == delka_abecedy
    prefix = [0, 1]
    first = [0, 1]
    period = [None] * delka_abecedy

    generate(prefix, first, period, '')
    print_summary(delka_abecedy)


main()

# vim: ts=4 sw=4 et
