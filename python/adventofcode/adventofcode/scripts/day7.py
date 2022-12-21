# --- Day 7: No Space Left On Device ---

# You can hear birds chirping and raindrops hitting leaves as the expedition proceeds.
# Occasionally, you can even hear much louder sounds in the distance;
# how big do the animals get out here, anyway?

# The device the Elves gave you has problems with more than just its communication
# system. You try to run a system update:

# $ system-update --please --pretty-please-with-sugar-on-top
# Error: No space left on device

# Perhaps you can delete some files to make space for the update?

# You browse around the filesystem to assess the situation and save the resulting
# terminal output (your puzzle input). For example:

# $ cd /
# $ ls
# dir a
# 14848514 b.txt
# 8504156 c.dat
# dir d
# $ cd a
# $ ls
# dir e
# 29116 f
# 2557 g
# 62596 h.lst
# $ cd e
# $ ls
# 584 i
# $ cd ..
# $ cd ..
# $ cd d
# $ ls
# 4060174 j
# 8033020 d.log
# 5626152 d.ext
# 7214296 k

# The filesystem consists of a tree of files (plain data) and directories
# (which can contain other directories or files). The outermost directory is called /.
# You can navigate around the filesystem, moving into or out of directories and
# listing the contents of the directory you're currently in.

# Within the terminal output, lines that begin with $ are commands you executed,
# very much like some modern computers:

#     cd means change directory. This changes which directory is the current directory,
# but the specific result depends on the argument:
#         cd x moves in one level: it looks in the current directory for the
# directory named x and makes it the current directory.
#         cd .. moves out one level: it finds the directory that contains the
# current directory, then makes that directory the current directory.
#         cd / switches the current directory to the outermost directory, /.
#     ls means list. It prints out all of the files and directories immediately
# contained by the current directory:
#         123 abc means that the current directory contains a file named abc with
# size 123.
#         dir xyz means that the current directory contains a directory named xyz.

# Given the commands and output in the example above, you can determine
# that the filesystem looks visually like this:

# - / (dir)
#   - a (dir)
#     - e (dir)
#       - i (file, size=584)
#     - f (file, size=29116)
#     - g (file, size=2557)
#     - h.lst (file, size=62596)
#   - b.txt (file, size=14848514)
#   - c.dat (file, size=8504156)
#   - d (dir)
#     - j (file, size=4060174)
#     - d.log (file, size=8033020)
#     - d.ext (file, size=5626152)
#     - k (file, size=7214296)

# Here, there are four directories: / (the outermost directory),
# a and d (which are in /), and e (which is in a).
# These directories also contain files of various sizes.

# Since the disk is full, your first step should probably be to find directories
# that are good candidates for deletion. To do this, you need to determine the
# total size of each directory. The total size of a directory is the sum of the
# sizes of the files it contains, directly or indirectly.
# (Directories themselves do not count as having any intrinsic size.)

# The total sizes of the directories above can be found as follows:

#     The total size of directory e is 584 because it contains a single file i of
# size 584 and no other directories.
#     The directory a has total size 94853 because it contains files f (size 29116),
# g (size 2557), and h.lst (size 62596), plus file i indirectly
# (a contains e which contains i).
#     Directory d has total size 24933642.
#     As the outermost directory, / contains every file.
# Its total size is 48381165, the sum of the size of every file.

# To begin, find all of the directories with a total size of at most 100000,
# then calculate the sum of their total sizes. In the example above,
# these directories are a and e; the sum of their total sizes is 95437 (94853 + 584).
# (As in this example, this process can count files more than once!)

# Find all of the directories with a total size of at most 100000.
# What is the sum of the total sizes of those directories?


# --- Part Two ---

# Now, you're ready to choose a directory to delete.

# The total disk space available to the filesystem is 70_000_000. To run the update,
# you need unused space of at least 30_000_000. You need to find a directory you can delete
#  that will free up enough space to run the update.

# In the example above, the total size of the outermost directory (and thus the total
# amount of used space) is 48381165; this means that the size of the unused space must
# currently be 21618835, which isn't quite the 30000000 required by the update.
# Therefore, the update still requires a directory with total size of at least 8381165
# to be deleted before it can run.

# To achieve this, you have the following options:

#     Delete directory e, which would increase unused space by 584.
#     Delete directory a, which would increase unused space by 94853.
#     Delete directory d, which would increase unused space by 24933642.
#     Delete directory /, which would increase unused space by 48381165.

# Directories e and a are both too small; deleting them would not free up enough space.
# However, directories d and / are both big enough! Between these, choose the smallest:
# d, increasing unused space by 24933642.

# Find the smallest directory that, if deleted, would free up enough space on the
# filesystem to run the update. What is the total size of that directory?

import os
import networkx as nx
from networkx.algorithms.traversal import dfs_successors, dfs_predecessors
from enum import Enum

Line = Enum("Line", ["cd", "list", "file", "dir"])


class SpringCleaning:
    def __init__(self):
        _data = open(os.getcwd() + "/../../problem_specs/day7.txt", "r")
        self.terminal_output = _data.read().splitlines()
        _data.close()
        self.filesystem = nx.DiGraph()
        self.filesystem.add_node(0, name="/")
        self.cwd = 0

        self.files_in_directories = {}
        self.files_in_directories[self.cwd] = []

        self.max_index = 0

        self.total_filespace = 7e7

    def _parse_line(self, line):
        items_in_line = line.split(" ")
        if len(items_in_line) == 2:
            if items_in_line[0] == "$":
                return Line.list, None
            if items_in_line[0] == "dir":
                return Line.dir, items_in_line[1]
            if items_in_line[0].isnumeric():
                return eval(items_in_line[0]), items_in_line[1]

        if not items_in_line[0] == "$":
            raise nameError("Degree 3 entry that isn't a command.")

        return Line.cd, items_in_line[2]

    def get_dir_name(self, node: int):
        return self.filesystem.nodes[node]["name"]

    def children(self, node: int):
        try:
            children = dfs_successors(self.filesystem)[node]
        except KeyError:
            children = []
        return children

    def children_names(self, node: int):
        return [
            self.filesystem.nodes[node]["name"]
            for node in dfs_successors(self.filesystem, source=self.cwd)[self.cwd]
        ]

    def parent(self, node: int):
        return dfs_predecessors(self.filesystem)[node]

    def add_node_and_edge(self, tag: str):
        self.max_index += 1
        self.filesystem.add_node(self.max_index, name=tag)
        self.filesystem.add_edge(self.cwd, self.max_index)
        self.files_in_directories[self.max_index] = []

    def iterate(self):
        for idx, line in enumerate(self.terminal_output[1:]):
            key, tag = self._parse_line(line)
            if key == Line.cd and tag != "..":
                self.cwd = self.children(node=self.cwd)[
                    self.children_names(node=self.cwd).index(tag)
                ]
            if key == Line.cd and tag == "..":
                self.cwd = self.parent(self.cwd)
            if key == Line.list:
                pass
            if key == Line.dir:
                self.add_node_and_edge(tag=tag)
            if isinstance(key, int):
                filesize, filename = key, tag
                self.files_in_directories[self.cwd] += [filesize]

    def directory_size(self, node: int):
        top_level = sum(self.files_in_directories[node])
        children = self.children(node)
        child_sizes = 0
        if children:
            child_sizes = sum([self.directory_size(node=child) for child in children])
        return child_sizes + top_level

    def all_directory_size(self):
        return [self.directory_size(node) for node in self.filesystem.nodes]

    def part1(self):
        answer = 0
        for total_size in self.all_directory_size():
            if total_size <= 1e5:
                answer += total_size
        return answer

    @property
    def total_memory_used(self):
        return self.directory_size(node=0)

    @property
    def free_space(self):
        return self.total_filespace - self.total_memory_used

    def space_needed(self, filesize: int):
        if filesize < self.free_space:
            return 0
        return filesize - self.free_space

    def part2(self):
        for filesize in sorted(self.all_directory_size()):
            if filesize > self.space_needed(3e7):
                return filesize


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    s = SpringCleaning()
    s.iterate()
    nx.draw_networkx(s.filesystem)
    plt.savefig("graph.png")
    print(s.part2())
