import math

import random

def shuffle(str):
    str = list(str)
    [currentIndex,randomIndex,tempValue] = [len(str)-1,None,None]

    while currentIndex > 0 :
        randomIndex = random.randint(0,currentIndex)
        tempValue = str[randomIndex]
        str[randomIndex] = str[currentIndex]
        str[currentIndex] = tempValue
        currentIndex -= 1

    return ''.join(str)


shuffled:str = shuffle("hello")
print(shuffled)