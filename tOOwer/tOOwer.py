# This file contains all the necessary classes to implement a basic Tower of Hanoi implementation in python

class Disk:
    """
    A Disk class has a size and can be compared to other disks.

    :param size: int, A number indicating how large the disk is.
    """
    def __init__(self, size):
        self.size = size

    def __str__(self):
        return "#"*(2*self.size-1)

    def __repr__(self):
        return str((self.size, self.__str__()))

    def __lt__(self, other):
        return self.size < other.size

    def __gt__(self, other):
        return self.size > other.size

    def __eq__(self, other):
        return self.size == other.size

    def print_to_pole(self, n):
        """
        This method will convert the disk string into a format so that it can be printed to stdout
        and look pretty.
        :param n: int, required width
        :return: formatted string for stdout
        """
        ws = n - self.size  # The amount of whitespace required
        return " "*ws + str(self) + " "*ws


class Pole:
    """
    A pole is an object that can hold an array of Disks and can perform the action of adding and removing
    disks under the rules of the puzzle (i.e. One disk at a time, disks must be in descending size.

    :param name: str, name of pole
    :param disks: list, list of disks
    """
    def __init__(self, name, disks=[]):
        self.name = name
        self.disks = disks

    def __len__(self):
        return len(self.disks)

    def push(self, disk):
        """
        This method is used for adding a disk to a pole and checking if the move is legal.

        :param disk: Disk, the disk being added to the pole
        :return: self
        """
        if len(self) == 0:
            self.disks.append(disk)
            return self
        elif self[-1] > disk:
            self.disks.append(disk)
            return self
        else:
            raise Exception(f"You cannot put a disk of size {disk.size} on top of a disk of size {self[-1].size}, ya idiot.")

    def __getitem__(self, item):
        return self.disks[item]

    def __iter__(self):
        return self.disks.__iter__()

    def pop(self):
        """
        This method is used for popping the top disk off of a pole.

        :return: Disk, the top disk of the pole.
        """
        d = self[-1]    # Record top disk
        self.disks = self.disks[:-1]    # Remove the top disk from self.disks
        return d

    def __repr__(self):
        return str([disk.__repr__() for disk in self])


class Tower:
    """
    The object that represents the full puzzle.

    :param n: int, the number of disks in the problem.
    :param From: str, the name of the first pole.
    :param Using: str, the name of the first pole.
    :param To: str, the name of the first pole.
    """
    def __init__(self, n, From, Using, To):
        self.n = n
        self.From = From
        self.Using = Using
        self.To = To
        self.poles = [Pole(From, [Disk(n-i) for i in range(n)]), Pole(Using), Pole(To)]
        self.pole_dict = {From: 0, Using: 1, To: 2}

    def __getitem__(self, item):
        return self.poles[self.pole_dict[item]]

    def move(self, From, To):
        if len(self[From]) == 0:
            raise Exception(f"Pole {From} has no disks on it to move.")
        d = self[From].pop()
        try:
            self[To].push(d)
        except Exception as e:
            self[From].push(d)
            raise e
        finally:
            return self

    def __repr__(self):
        return str([self[i] for i in self.pole_dict.values()])

    def __iter__(self):
        return self.poles.__iter__()

    def solved(self):
        return (len(self[self.From]) == 0) & (len(self[self.Using]) == 0)

    def reset(self):
        self.poles = [Pole(self.From, [Disk(self.n-i) for i in range(self.n)]), Pole(self.Using), Pole(self.To)]

    def __str__(self):
        s = ''
        for i in range(self.n):
            for pole in self:
                if self.n-i-1 < len(pole):
                    s = s + pole[self.n - i - 1].print_to_pole(self.n)
                else:
                    s = s + " "*(self.n-1) + "|" + " "*(self.n-1)
            s = s + "\n"
        return s

    def play(self):
        try:
            from IPython.display import clear_output
        except Exception as e:
            raise Exception(e, "This method is designed for jupyter/IPython.")

        error = False

        while not self.solved():
            print(self)
            if error:
                print("The last move was invalid.")

            user_input = input("Input move using {FROM} to {TO} syntax")

            try:
                FROM = user_input.split(' to ')[0]
                TO = user_input.split(' to ')[1]
                self.move(FROM, TO)
                error = False
            except Exception as e:
                error = True
                pass

            clear_output
            print(self)
            print("Solved!")
