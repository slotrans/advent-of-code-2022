ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"

LOSS = "loss"
DRAW = "draw"
WIN = "win"

SCORE_BY_PLAY = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3,
}

SCORE_BY_OUTCOME = {
    LOSS: 0,
    DRAW: 3,
    WIN: 6,
}

OPPONENT_DECODER = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
}

P1_RESPONSE_DECODER = {
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}

P2_OUTCOME_DECODER = {
    "X": LOSS,
    "Y": DRAW,
    "Z": WIN,
}

HOW_TO_PLAY = {
    # tuples are (their_play, desired_outcome)
    #
    (ROCK, LOSS): SCISSORS,
    (PAPER, LOSS): ROCK,
    (SCISSORS, LOSS): PAPER,
    #
    (ROCK, DRAW): ROCK,
    (PAPER, DRAW): PAPER,
    (SCISSORS, DRAW): SCISSORS,
    #
    (ROCK, WIN): PAPER,
    (PAPER, WIN): SCISSORS,
    (SCISSORS, WIN): ROCK,
}

ROUND_RESULT = {
    # tuples are (their_play, my_play)
    #
    (ROCK, ROCK): DRAW,
    (PAPER, PAPER): DRAW,
    (SCISSORS, SCISSORS): DRAW,
    #
    (ROCK, PAPER): WIN,
    (PAPER, SCISSORS): WIN,
    (SCISSORS, ROCK): WIN,
    #
    (ROCK, SCISSORS): LOSS,
    (PAPER, ROCK): LOSS,
    (SCISSORS, PAPER): LOSS,    
}


def score_for_round(their_play, my_play):
    outcome = ROUND_RESULT[(their_play, my_play)]
    return SCORE_BY_PLAY[my_play] + SCORE_BY_OUTCOME[outcome]


def score_per_guide_p1(guide_text):
    total_score = 0
    for round_string in guide_text.split("\n"):
        if round_string == "":
            continue
        their_code, my_code = round_string.split(" ")
        their_play = OPPONENT_DECODER[their_code]
        my_play = P1_RESPONSE_DECODER[my_code]
        total_score += score_for_round(their_play, my_play)
    return total_score


def score_per_guide_p2(guide_text):
    total_score = 0
    for round_string in guide_text.split("\n"):
        if round_string == "":
            continue
        their_code, outcome_code = round_string.split(" ")
        their_play = OPPONENT_DECODER[their_code]
        desired_outcome = P2_OUTCOME_DECODER[outcome_code]
        my_play = HOW_TO_PLAY[(their_play, desired_outcome)]
        total_score += score_for_round(their_play, my_play)
    return total_score


if __name__ == "__main__":
    input02 = open("../input/input02").read()
    guide_score_p1 = score_per_guide_p1(input02)
    print(f"(p1 answer) score for following the guide using p1 rules: {guide_score_p1}") # 12458

    guide_score_p2 = score_per_guide_p2(input02)
    print(f"(p2 answer) score for following the guide using p2 rules: {guide_score_p2}") # 12683



#########################################

SAMPLE_INPUT = """\
A Y
B X
C Z
"""

def test_score_per_guide_p1():
    expected = 15
    actual = score_per_guide_p1(SAMPLE_INPUT)
    assert expected == actual


def test_score_per_guide_p2():
    expected = 12
    actual = score_per_guide_p2(SAMPLE_INPUT)
    assert expected == actual
