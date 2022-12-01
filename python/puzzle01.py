
def calories_per_elf(input_string):
    chunks = input_string.split("\n\n")
    return [sum([int(cals) for cals in c.split("\n") if cals != ""]) for c in chunks]



if __name__ == "__main__":
    input01 = open("input01").read()
    max_calories = max(calories_per_elf(input01))
    print(f"(p1 answer) elf with most calories has: {max_calories}") # 72070

    


###########################

SAMPLE_INPUT = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

def test_calories_per_elf():
    expected = [6000, 4000, 11000, 24000, 10000]
    actual = calories_per_elf(SAMPLE_INPUT)
    assert expected == actual
