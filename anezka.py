#!/bin/python

delka_abecedy = 5
print_debug = not True

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
        print(prefix)
        return()
    remaining_fraction = compute_remaining_fraction(period)
    if (remaining_fraction < 0.0000001):
        debug(indent+"unused letters remain")
        return(prefix)
    # zkontroluj, jestli neni pismeno vynuceno
    #  ... to ted jeste nepotrebujeme
    povinny_znak = None

    for i in range(len(first)):
        if (period[i] is not None):
            if (len(prefix) % period[i] == first[i]):
                if (povinny_znak is None):
                    povinny_znak = i
                else:
                    # collision - no result possible
                    return()
    if (povinny_znak is not None):
        generate(prefix + [povinny_znak], first, period, indent+'  ')
    else:
        # 1) add a new letter, or
        # 2) repeat one of the letters with no period
        #
        # 1) - take the next unused letter: len(first)
        ltr = len(first)
        if (ltr < delka_abecedy):
            generate(prefix + [ltr], first + [len(prefix)], period.copy(), indent+'  ')
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
    # TODO: we can add more clever tests, to eliminate future collisions
    return(ok)

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


main()

# vim: ts=4 sw=4 et
