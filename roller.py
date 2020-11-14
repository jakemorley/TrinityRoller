import pytest
import random


class Roller:
    def __init__(self, dietype=6, dicepool=1, explode=None, reroll=None):
        if isinstance(dietype, int) and (dietype > 2):
            self.dietype = dietype
        else:
            raise Exception("Die Type should be an integer value greater than 1.")
        if isinstance(dicepool, int) and (dicepool > 0):
            self.dicepool = dicepool
        else:
            raise Exception("Dicepool must be an integer greater than 0.")

        self.explode = None
        if explode is not None:
            if isinstance(explode, int) and (1 < explode <= dietype):
                self.explode = explode
            else:
                raise Exception(
                    "Invalid explode value - must be a positive integer less than or equal to the die type.")

        self.reroll = None
        if reroll is not None:
            if isinstance(reroll, int) and (1 < reroll <= dietype):
                self.reroll = reroll
            else:
                raise Exception("Invalid reroll value - must be a positive integer less than or equal to the die type.")

        self.result = []  # we store the last result rolled

    def roll(self, dicepool=None):
        # roll the default dicepool if none is provided
        if dicepool is None:
            dicepool = self.dicepool
        for i in range(0, dicepool):
            result = random.randint(1, self.dietype)
            if self.explode is not None:  # we have a die that can explode
                next_result = result
                while next_result >= self.explode:
                    next_result = random.randint(1, self.dietype)
                    result += next_result
            if self.reroll is not None:  # we have a die that is rerolled
                result_set = [result]
                while result_set[-1] >= self.reroll:
                    result_set.append(random.randint(1, self.dietype))
                    result = result_set  # we overwrite result at this point to ensure we have a result that is a list of ints
            self.result.append(result)
        return self.result

