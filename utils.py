import random


def is_worked(chance: float) -> bool:
    return random.random() <= chance
