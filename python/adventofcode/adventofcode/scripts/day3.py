# --- Day 3: Rucksack Reorganization ---

# One Elf has the important job of loading all of the rucksacks with supplies for the
# jungle journey. Unfortunately, that Elf didn't quite follow the packing instructions,
# and so a few items now need to be rearranged.

# Each rucksack has two large compartments. All items of a given type are meant to go
# into exactly one of the two compartments. The Elf that did the packing failed to
# follow this rule for exactly one item type per rucksack.

# The Elves have made a list of all of the items currently in each rucksack (your puzzle
# input), but they need your help finding the errors. Every item type is identified by a
#  single lowercase or uppercase letter (that is, a and A refer to
# different types of items).

# The list of items for each rucksack is given as characters all on a single line.
# A given rucksack always has the same number of items in each of its two compartments,
# so the first half of the characters represent items in the first compartment, while
# the second half of the characters represent items in the second compartment.

# For example, suppose you have the following list of contents from six rucksacks:

# vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg
# wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
# ttgJtRGJQctTZtZT
# CrZsJsPPZsGzwwsLwLmpwMDw

#     The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its
# first compartment contains the items vJrwpWtwJgWr, while the second compartment
# contains the items hcsFMMfFFhFp. The only item type that appears in both compartments
# is lowercase p.
#     The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL.
#  The only item type that appears in both compartments is uppercase L.
#     The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg;
# the only common item type is uppercase P.
#     The fourth rucksack's compartments only share item type v.
#     The fifth rucksack's compartments only share item type t.
#     The sixth rucksack's compartments only share item type s.

# To help prioritize item rearrangement, every item type can be converted to a priority:

#     Lowercase item types a through z have priorities 1 through 26.
#     Uppercase item types A through Z have priorities 27 through 52.

# In the above example, the priority of the item type that appears in both compartments
# of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s);
# the sum of these is 157.

# Find the item type that appears in both compartments of each rucksack.
# What is the sum of the priorities of those item types?


# --- Part Two ---

# As you finish identifying the misplaced items, the Elves come to you with another
# issue.

# For safety, the Elves are divided into groups of three. Every Elf carries a badge that
# identifies their group. For efficiency, within each group of three Elves, the badge is
# the only item type carried by all three Elves. That is, if a group's badge is item type
#  B, then all three Elves will have item type B somewhere in their rucksack, and at most
#  two of the Elves will be carrying any other item type.

# The problem is that someone forgot to put this year's updated authenticity sticker on
# the badges. All of the badges need to be pulled out of the rucksacks so the new
# authenticity stickers can be attached.

# Additionally, nobody wrote down which item type corresponds to each group's badges.
# The only way to tell which item type is the right one is by finding the one item type
# that is common between all three Elves in each group.

# Every set of three lines in your list corresponds to a single group, but each group can
# have a different badge item type. So, in the above example, the first group's rucksacks are the first three lines:

# vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg

# And the second group's rucksacks are the next three lines:

# wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
# ttgJtRGJQctTZtZT
# CrZsJsPPZsGzwwsLwLmpwMDw

# In the first group, the only item type that appears in all three rucksacks is
# lowercase r; this must be their badges. In the second group, their badge item type
# must be Z.

# Priorities for these items must still be found to organize the sticker attachment
# efforts: here, they are 18 (r) for the first group and 52 (Z) for the second group.
# The sum of these is 70.

# Find the item type that corresponds to the badges of each three-Elf group.
# What is the sum of the priorities of those item types?


import os
from typing import Tuple, List, Set
import string


class Rucksacks:
    def __init__(self):
        _data = open(os.getcwd() + "/../../problem_specs/day3.txt", "r")
        self.rucksack_contents = _data.read().splitlines()
        _data.close()
        self.compartmentalised = [
            (contents[0 : len(contents) // 2], contents[len(contents) // 2 : :])
            for contents in self.rucksack_contents
        ]

        self.lower_case = list(string.ascii_lowercase)
        self.upper_case = list(string.ascii_uppercase)

        self.total_rucksacks = len(self.rucksack_contents)
        self.groups = self.total_rucksacks // 3

    def common_item(self, compartment_contents: Tuple[str, str]) -> Set[str]:
        """Return the common item(s) between two rucksack compartments.

        Parameters
        ----------
        compartment_contents : Tuple[str, str]
            The items present in the first and second compartment, respectively.

        Returns
        -------
        str
            The common item(s) between compartments.
        """
        return list(set(compartment_contents[0]) & set(compartment_contents[1]))

    def get_priority(self, item: str) -> int:
        """Return the priority value for a given item type.
        a-z == 1-26
        A-Z == 27-52

        Parameters
        ----------
        item : str
            The item type, as a string object.

        Returns
        -------
        int
            The priority score.
        """
        if item.islower():
            idx = self.lower_case.index(item)
            return range(1, 27)[idx]
        if item.isupper():
            idx = self.upper_case.index(item)
            return range(27, 53)[idx]
        raise ValueError(f"Invalid item passed: {item}")

    def part1(self):
        """Solve part 1 of the puzzle

        Returns
        -------
        int
            The answer!
        """
        return sum(
            [
                self.get_priority(item=self.common_item(rucksack)[0])
                for rucksack in self.compartmentalised
            ]
        )

    def group_badge(self, group_id: int) -> str:
        """Given a group ID, return the badge of that group.

        Parameters
        ----------
        group_id : int
            Group index, between 1 and 100 inclusive.

        Returns
        -------
        str
            The group badge.

        Raises
        ------
        ValueError
            If group ID is outside of the range [1, 100].
        """
        if not 1 <= group_id <= self.groups:
            raise ValueError("Group ID is outside the acceptable range.")

        group_rucksacks = list(
            map(
                set, self.rucksack_contents[3 * (group_id - 1) : 3 * (group_id - 1) + 3]
            )
        )

        return list(group_rucksacks[0] & group_rucksacks[1] & group_rucksacks[2])[0]

    def part2(self):
        total_priority = 0
        for group_id in range(1, self.groups + 1):
            badge = self.group_badge(group_id=group_id)
            priority = self.get_priority(item=badge)
            total_priority += priority
        return total_priority


if __name__ == "__main__":
    rk = Rucksacks()
    print(rk.part1())
    print(rk.part2())
