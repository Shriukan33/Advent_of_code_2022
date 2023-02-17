from typing import Union
from collections import namedtuple

with open("aoc_02_input.txt", "r") as f:
    battles = f.read().splitlines()


class JankenChoice:

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, JankenChoice):
            return False
        return self.name == other.name


class Rock(JankenChoice):
    def __init__(self):
        self.name = "Rock"
        self.beats = "Scissors"
        self.loses_to = "Paper"
        self.points = 1


class Paper(JankenChoice):
    def __init__(self):
        self.name = "Paper"
        self.beats = "Rock"
        self.loses_to = "Scissors"
        self.points = 2


class Scissors(JankenChoice):
    def __init__(self):
        self.name = "Scissors"
        self.beats = "Paper"
        self.loses_to = "Rock"
        self.points = 3


Battle = namedtuple("Battle", ["opponent_choice", "player_choice"])


def parse_battles(battles: list) -> list:
    """Parse battles from input file.

    Args:
        battles (list): List of battles.

    Returns:
        list: List of parsed battles.
    """
    parsed_battles = []
    for battle in battles:
        parsed_battle = battle.split(" ")
        choices = Battle(
            opponent_choice=parsed_battle[0],
            player_choice=parsed_battle[1],
        )

        letter_to_class = {
            "A": Rock,
            "B": Paper,
            "C": Scissors,
            "X": Rock,
            "Y": Paper,
            "Z": Scissors,
        }
        # create class instances from battle
        this_battle = Battle(
            opponent_choice=letter_to_class[choices.opponent_choice](),
            player_choice=letter_to_class[choices.player_choice](),
        )
        parsed_battles.append(this_battle)

    return parsed_battles


def compute_outcome(
    opponent_choice: Union[Rock, Paper, Scissors],
    player_choice: Union[Rock, Paper, Scissors],
) -> int:
    """Compute the outcome of a battle.

    Args:
        opponent_choice (Union[Rock, Paper, Scissors]): Opponent's choice.
        player_choice (Union[Rock, Paper, Scissors]): Player's choice.

    Returns:
        int: Outcome of the battle.

    The outcome is computed as follows: The player choice's points
    + the outcome's points : 0 for a loss, 3 for a tie, 6 for a win.
    """
    if player_choice == opponent_choice:
        return player_choice.points + 3
    elif player_choice.beats == opponent_choice.name:
        return player_choice.points + 6
    else:
        return player_choice.points


if __name__ == "__main__":
    parsed_battles = parse_battles(battles)
    total_score = 0
    for battle in parsed_battles:
        battle: Battle
        total_score += compute_outcome(
            battle.opponent_choice, battle.player_choice
        )

    print(total_score)
