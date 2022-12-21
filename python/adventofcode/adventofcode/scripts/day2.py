# -- Day 2: Rock Paper Scissors ---

# The Elves begin to set up camp on the beach. To decide whose tent gets to be closest
# to the snack storage, a giant Rock Paper Scissors tournament is already in progress.

# Rock Paper Scissors is a game between two players. Each game contains many rounds;
# in each round, the players each simultaneously choose one of Rock, Paper, or Scissors
# using a hand shape. Then, a winner for that round is selected: Rock defeats Scissors,
# Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape,
#  the round instead ends in a draw.

# Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide
# (your puzzle input) that they say will be sure to help you win. "The first column is
# what your opponent is going to play: A for Rock, B for Paper, and C for Scissors.
# The second column--" Suddenly, the Elf is called away to help with someone's tent.

# The second column, you reason, must be what you should play in response: X for Rock,
# Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the
# responses must have been carefully chosen.

# The winner of the whole tournament is the player with the highest score. Your total
# score is the sum of your scores for each round. The score for a single round is the
# score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus
# the score for the outcome of the round (0 if you lost, 3 if the round was a draw,
# and 6 if you won).

# Since you can't be sure if the Elf is trying to help you or trick you,
# you should calculate the score you would get if you were to follow the strategy guide.

# For example, suppose you were given the following strategy guide:

# A Y
# B X
# C Z

# This strategy guide predicts and recommends the following:

#     In the first round, your opponent will choose Rock (A), and you should choose
# Paper (Y). This ends in a win for you with a score of 8 (2 because you chose
# Paper + 6 because you won).
#     In the second round, your opponent will choose Paper (B), and you should
# choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
#     The third round is a draw with both players choosing Scissors, giving you a
#  score of 3 + 3 = 6.

# In this example, if you were to follow the strategy guide,
# you would get a total score of 15 (8 + 1 + 6).

# What would your total score be if everything goes exactly according to
# your strategy guide?

# --- Part Two ---

# The Elf finishes helping with the tent and sneaks back over to you.
# "Anyway, the second column says how the round needs to end: X means you need to lose,
# Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

# The total score is still calculated in the same way, but now you need to figure
# out what shape to choose so the round ends as indicated.
# The example above now goes like this:

#     In the first round, your opponent will choose Rock (A), and you need the
# round to end in a draw (Y), so you also choose Rock. This gives you a score of
# 1 + 3 = 4.
#     In the second round, your opponent will choose Paper (B), and you choose
# Rock so you lose (X) with a score of 1 + 0 = 1.
#     In the third round, you will defeat your opponent's Scissors with Rock
# for a score of 1 + 6 = 7.

# Now that you're correctly decrypting the ultra top secret strategy guide,
# you would get a total score of 12.

# Following the Elf's instructions for the second column, what would your
# total score be if everything goes exactly according to your strategy guide?


import os
from ast import literal_eval


class RockPaperScissors:
    def __init__(self):
        _data = open(os.getcwd() + "/../../problem_specs/day2.txt", "r")
        self.strategy_guide = _data.read().splitlines()
        _data.close()
        self.score = {"Rock": 1, "Paper": 2, "Scissors": 3}
        self.first_column = sorted(list(set(x[0] for x in self.strategy_guide)))
        self.second_column = sorted(list(set(x[-1] for x in self.strategy_guide)))

        self.winning_strategy = {
            "Rock": "Paper",
            "Paper": "Scissors",
            "Scissors": "Rock",
        }
        self.losing_strategy = {
            "Rock": "Scissors",
            "Paper": "Rock",
            "Scissors": "Paper",
        }

    def _convert(self, play: str):
        """Convert A, B or C (equiv X, Y or Z) to Rock, Paper or Scissors.

        Parameters
        ----------
        play : str
            The given play, one of A, B, C, X, Y, or Z.

        Returns
        -------
        str
            Rock, Paper or Scissors.
        """

        idx = (
            self.first_column.index(play)
            if play in self.first_column
            else self.second_column.index(play)
        )

        return list(self.score.keys())[idx]

    def game_outcome(self, elf_plays: str, i_play: str):
        """Get the outcome of a single game.

        Parameters
        ----------
        elf_plays : str
            Which hand the elf played: Rock, Paper or Scissors.
        i_play : str
            Which hand I played: Rock, Paper or Scissors.

        Returns
        -------
        int
            The total score of the game, for me.
        """
        outcome = self.score[i_play] - self.score[elf_plays]

        if outcome == 0:
            return 3 + self.score[i_play]

        if outcome in [1, -2]:
            return 6 + self.score[i_play]

        if outcome in [-1, 2]:
            return 0 + self.score[i_play]

    def _tactics(self, opponent: str, instruction: str):
        """_summary_

        Parameters
        ----------
        opponent : str
            What play the opponent has made, one of Rock, Paper or Scissors.
        instruction : str
            The instruction on whether to win ("Z"), lose ("X") or draw ("Y").

        Returns
        -------
        str
            My corresponding play, one of Rock, Paper or Scissors.

        Raises
        ------
        ValueError
            If the instruction is invalid.
        """
        if instruction not in ["X", "Y", "Z"]:
            raise ValueError("Incorrect instruction passed, must be one of X, Y or Z")

        return (
            self.losing_strategy[opponent]
            if instruction == "X"
            else self.winning_strategy[opponent]
            if instruction == "Z"
            else opponent
        )

    def part1(self):
        """In part1, assume the second column are instructions for which
        hand to play.
        """
        return sum(
            [
                self.game_outcome(
                    elf_plays=self._convert(entry[0]), i_play=self._convert(entry[-1])
                )
                for entry in self.strategy_guide
            ]
        )

    def part2(self):
        """In part2, assume the second column is instructions for how the
        game should end.
        """
        score = 0
        for entry in self.strategy_guide:
            elf_plays = self._convert(entry[0])
            i_play = self._tactics(opponent=elf_plays, instruction=entry[-1])
            score += self.game_outcome(elf_plays, i_play)

        return score


if __name__ == "__main__":
    rps = RockPaperScissors()
    print(rps.part1())
    print(rps.part2())
