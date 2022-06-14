import random
from typing import List


class PyShuffle:

    def __init__(self,text:str):
        self.text = text

    def set_values(self) -> List:
        self.text = list(self.text)
        return [len(self.text) - 1, None, None]

    def shuffle(self) -> str:
        [currentIndex, randomIndex, tempValue] = self.set_values()

        while currentIndex > 0:
            randomIndex = random.randint(0, currentIndex)
            tempValue = self.text[randomIndex]
            self.text[randomIndex] = self.text[currentIndex]
            self.text[currentIndex] = tempValue
            currentIndex -= 1

        return ''.join(self.text)