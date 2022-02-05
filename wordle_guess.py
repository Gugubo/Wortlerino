from dataclasses import dataclass
from enum import Enum, auto


class Guess(Enum):
    """Used to give feedback on a guess"""

    CORRECT = auto()
    WRONG_POSITION = auto()
    INCORRECT = auto()


@dataclass(frozen=True)
class LetterGuess:
    letter: str
    guess: Guess
