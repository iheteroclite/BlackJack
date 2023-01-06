from math import erf, prod, comb, sqrt

def chance_zero_blackjack_total(not_bj_probs):
    """
    rounds = number of rounds so far
    not_bj_probs = an array of (1-p(r)) where p(r) is the probability of
    blackjack in round r

    Therefore, chance_zero_blackjack_total =
    P(0) = product from r = 1 to rounds (1 - p(r))

    """
    return prod(not_bj_probs)


def chance_one_blackjack_total(ratios, P_0):
    # array = [p_bj / p_not_bj for p_bj, p_not_bj in bj_probs, not_bj_probs]
    print('P_0', P_0)

    return P_0 * sum(ratios)


def chance_n_blackjack_total(results, n_bjs=False):
    """Calculate the probability of n blackjacks, and at least n blackjacks.

    Arguments:
    results -- A list of dictionaries representing each deal with
              'probability' and 'blackjack' attributes
    --
    """

    # calculate n_bjs
    if not n_bjs:
        n_bjs = len([1 for result in results if result['blackjack']])

    # Get array of the probabilities of getting blackjack for each round
    bj_probs = [r['probability'] for r in results]
    not_bj_probs = [1 - r['probability'] for r in results]

    ratios = [p / (1 - p) for p in bj_probs]
    rounds = len(results)

    P_0 = chance_zero_blackjack_total(not_bj_probs)
    if n_bjs == 0:
        print('n blackjacks=0')

        # Chance of 0 blackjacks is P_0, chance of at least 0 blackjacks is 1
        return P_0, 1

    P_1 = chance_one_blackjack_total(ratios, P_0)
    if n_bjs == 1:
        print('n blackjacks=1')
        # Chance of 1 blackjack is P_1
        # Chance of at least 1 blackjack (only subtract chance of 0 blackjacks)
        return P_1, 1 - P_0

    P_n_array = [P_0, P_1]

    # print('ratios: ', ratios)
    coeff = sum(ratios)

    for n in range(2, n_bjs + 1):
        ratios_n = [ratio**(n) for ratio in ratios]
        # print('ratios_n: ', ratios_n)
        P_n = P_n_array[-1] * coeff - P_0 * sum(ratios_n)
        P_n_array.append(P_n)

    P_n = P_n_array[-1]
    # TODO: problem may arise here:
    P_at_least_n = 1 - sum(P_n_array[:-1])
    print('for n_bjs, P_n, P_at_least_n, : ', n_bjs, P_n, P_at_least_n)
    print('with P_0, P_1', P_0, P_1)

    # Return Probability of n blackjacks, Probability at least n blackjacks
    return P_n, P_at_least_n

