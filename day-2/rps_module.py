# simple datastructure like map of scores and basis vectors
# rock      = (1, 0, 0)  (play score = 1)
# paper     = (0, 1, 0)  (play score = 2)
# scissors  = (0, 0, 1)  (play score = 3)
OPONENT_LUT = {
    #key: (score, basis_vector)
    "A": (1, (1, 0, 0)),     # rock
    "B": (2, (0, 1, 0)),     # paper
    "C": (3, (0, 0, 1)),     # scissor
}

RPS_LUT = {
    #key: (score, basis_vector)
    "X": (1, (1, 0, 0)),     # rock
    "Y": (2, (0, 1, 0)),     # paper
    "Z": (3, (0, 0, 1)),     # scissors
}

STRATEGY_LUT = {
    #key: (game score, desired outcome)
    "X": (0, -1),  # lose
    "Y": (3, 0),   # draw
    "Z": (6, 1),   # win
}

def __argmin(vec: tuple[int]):
    return min(range(len(vec)), key=lambda x: vec[x])


def __argeq(vec: tuple[int], value):
    """returns first index where a value is present"""
    return __argmin(tuple(abs(v - value) for v in vec))


def __vec3d_cross_product(a: tuple[int, 3], b: tuple[int, 3]) -> tuple[int]:
    """3d vector cross product
    
    arguments:
        a (tuple[int, 3]), length 3 tuple of vector a
        b (tuple[int, 3]), length 3 tuple of vector b
    returns:
        c (tuple[int, 3]) cross product c = a x b
    """
    a0, a1, a2 = a
    b0, b1, b2 = b
    return (a1*b2 - a2*b1,
            a2*b0 - a0*b2,
            a0*b1 - a1*b0)


def __calc_round_outcome(oponent_vec: tuple[int, 3], my_vec: tuple[int, 3]) -> int:
    """Calculate the outcome of one round

    if an invalid input is passed, throws a value error

    The cross product in the basis 
        Rock = (1, 0, 0)
        Paper = (0, 1, 0)
        Sciccors = (0, 0, 1)
    neatly solves this problem since
    a x b = - b x a,  a x a = 0

    Since integer multiplication and addition is fast, this allows
    us to solve the problem without slow if/else statements

    By summing over all indices after the cross product we get a score
    -1, 0, 1 (loss, draw, win) which is easily converted to a round score.

    arguments:
        oponent_input (tuple[int, 3]): basis vector of oponent input
        my_input (tuple[int, 3]): basis vector of my input

    returns:
        outcome (int): 0 if lost, 1 if draw, 2 if win
    """
    cross_prod = __vec3d_cross_product(oponent_vec, my_vec)
    raw_score = sum(cross_prod)
    return raw_score + 1


def __calc_round_score(oponent_input: str, my_input: str) -> int:
    """Calculate the score of a round ending in a win, draw, or loss

    essentially wraps calc_round_outcome and multiplies by 3

    arguments:
        oponent_input (str): "A", "B" or "C" (Rock, Paper, Scissor)
        my_input (str): "X", "Y" or "Z" (Rock, Paper, Scissor)

    returns:
        score (int): 0 if lost, 3 if draw, 6 if win
    """
    return 3 * __calc_round_outcome(oponent_input, my_input)


def round_score_calculator(oponent_input: str, my_input: str) -> int:
    """Calculate the entire score of one round 

    Part 1 of day 2 challenge
    A = X = rock
    B = Y = paper
    C = Z = scissors
    
    Calculates victory score and adds score associated with
    playing rock, paper or scissors (1, 2, 3).

    arguments:
        oponent_input (str): 'A', 'B', or 'C'
        my_input (str): 'X', 'Y', or 'Z'
    returns:
        round_score (int)
    """
    _, oponent_vec = OPONENT_LUT.get(oponent_input)
    play_score, my_vec = RPS_LUT.get(my_input)
    round_score = __calc_round_score(oponent_vec, my_vec)
    return round_score + play_score


def __brute_force_solve(oponent_vec: tuple[int, 3]) -> tuple[int, 3]:
    """calculate outcome of all outcomes for oponent input

    calculates cross product score of
        sum(a x b_i) = c_i
    where a = oponent_vec
        b_i in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    
    output vector will look something like
        (-1, 0, 1) or (0, 1, -1)

    arguments:
        oponent_vec (tuple[int, 3]): input basis vector
    returns:
        c (tuple[int, 3]), round scores for all possible plays
    """
    return tuple(sum(__vec3d_cross_product(oponent_vec, b)) for b in
                 ((1, 0, 0), (0, 1, 0), (0, 0, 1)))

def __brute_force_solve_strategy(oponent_vec: tuple[int, 3], desired_outcome: int) -> int:
    solution_vec =__brute_force_solve(oponent_vec)
    return __argeq(solution_vec, desired_outcome)


def strategy_score_calculator(oponent_input, my_input) -> int:
    """Follow strategy guide and calculate full score

    Part 2 of day 2 challenge
    A = rock,       X = end in victory
    B = paper,      Y = end in draw
    C = scissors,   Z = end in loss

    if oponent chooses A
        X -> I choose B (win)
        Y -> I choose A (draw)
        Z -> I choose C (loss)

    By checking a given input against all possible plays
    we can select the play that has the desired outcome
    for our given strategy. This is an OK solution
    computationally fast, and OK since the problem is
    small (i.e. brute force is OK).

    arguments:
        oponent_input (str): 'A', 'B', or 'C'
        my_input (str): 'X', 'Y', or 'Z'
    returns:
        round_score (int)
    """
    _, oponent_vec = OPONENT_LUT.get(oponent_input)
    game_score, desired_outcome = STRATEGY_LUT.get(my_input)
    play_idx = __brute_force_solve_strategy(oponent_vec, desired_outcome)
    play_score = play_idx + 1
    return game_score + play_score

if __name__ == "__main__":
    # game score tests
    assert __calc_round_outcome((1, 0, 0), (0, 1, 0)) == 2
    assert __calc_round_outcome((0, 1, 0), (1, 0, 0)) == 0
    assert __calc_round_outcome((0, 1, 0), (0, 1, 0)) == 1

    # aoc2022 example 1
    assert round_score_calculator("A", "Y") == 8
    assert round_score_calculator("B", "X") == 1
    assert round_score_calculator("C", "Z") == 6

    # __argmin test
    assert __argmin((0, 1, 2)) == 0
    assert __argmin((1, 2, 0)) == 2

    # __argeq test
    assert __argeq((0, 1, 2), 2) == 2
    assert __argeq((1, 2, 0), 2) == 1

    # aoc2022 example 2
    assert strategy_score_calculator("A", "Y") == 4
    assert strategy_score_calculator("B", "X") == 1
    assert strategy_score_calculator("C", "Z") == 7