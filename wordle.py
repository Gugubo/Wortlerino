"""Does wordle stuff"""

import collections
import random

from wordle_guess import LetterGuess, Guess

WORD_LISTS = {
    "Substantive": {
        "name": "Substantive",
        "filename": "substantive.txt",
        "description": "Wenige (~100) deutsche Substantive",
        "language": "de",
    },
    "German": {
        "name": "German",
        "filename": "german.txt",
        "description": "Deutsche Wörter (inklusive Flexionen)",
        "language": "de",
    },
    "Wikipedia": {
        "name": "Wikipedia",
        "filename": "wiki.txt",
        "description": "Liste der Titel aller deutschen Wikipedia-Artikel",
        "language": "de",
    },
    "Wordle": {
        "name": "Wordle",
        "filename": "wordle-answers.txt",
        "description": "All possible wordle words",
        "language": "en",
    },
    "Wordle-all": {
        "name": "Wordle-all",
        "filename": "wordle-all.txt",
        "description": "All possible wordle words + all words wordle accepts as input",
        "language": "en",
    },
    "Spelunky": {
        "name": "Spelunky",
        "filename": "spelunky.txt",
        "description": "All words that appear anywhere in Spelunky 2",
        "language": "en",
    },
    "English": {
        "name": "English",
        "filename": "english.txt",
        "description": "A few hundred thousand English words",
        "language": "en",
    },
}

LETTERS = {
    "German": {
        "letters": "abcdefghijklmnopqrstuvwxyzäöüß",
        "description": "Normales deutsches Alphabet",
    },
    "English": {
        "letters": "abcdefghijklmnopqrstuvwxyz",
        "description": "Standard English alphabet",
    },
}


class WordleState:
    """State including settings and the current wordle game"""

    def __init__(self):
        # Some default values
        self.word_list = WORD_LISTS[
            "Wordle"
        ]  # The list from which new words are chosen from
        self.guess_list = WORD_LISTS[
            "Wordle-all"
        ]  # The list of words which are valid to be guessed
        self.valid_letters = LETTERS["English"]
        self.min_length = 4
        self.max_length = 6
        self.game = None

    def create_game(self):
        """Creates a new game"""
        word = self._get_new_word()
        self.game = WordleGame(
            word,
            set(self.valid_letters["letters"]),
            self.guess_list["words"] + self.word_list["words"],
        )

    def _get_new_word(self):
        """Creates a new random word to be guessed"""
        valid_words = list(filter(self._is_valid_word, self.word_list["words"]))
        if len(valid_words) == 0:
            raise NoWordsException(
                "There are no words to choose! Change the word list or length requirements!"
            )
        return random.choice(valid_words).lower()

    def _is_valid_word(self, word):
        """Checks if a word is valid to be loaded in
        (correct length, only letters, lowercase or titlecase)"""
        return (
            self.max_length >= len(word) >= self.min_length
            and all(
                [letter.lower() in self.valid_letters["letters"] for letter in word]
            )
            and word[1:].islower()
        )

    def set_length(self, min_length, max_length):
        """Set length of new words to be generated"""
        if min_length > max_length:
            raise InvalidSettingsException(
                "Minimum length must be smaller than maximum length!"
            )
        if min_length < 1:
            raise InvalidSettingsException("Length must be at least 1!")
        if max_length > 20:
            raise InvalidSettingsException("Length must be 20 or smaller!")
        self.min_length = min_length
        self.max_length = max_length

    def set_word_list(self, new_word_list):
        """Sets list from which new words will be generated"""
        if new_word_list.lower() not in map(str.lower, WORD_LISTS):
            raise InvalidSettingsException(
                f"{new_word_list} is not a valid word list. Available word lists: {', '.join(WORD_LISTS)}"
            )
        self.word_list = WORD_LISTS[new_word_list.title()]

    def set_guess_list(self, new_guess_list):
        """Sets list for words that can be guessed"""
        if new_guess_list.lower() not in map(str.lower, WORD_LISTS):
            raise InvalidSettingsException(
                f"{new_guess_list} is not a valid word list. Available word lists: {', '.join(WORD_LISTS)}"
            )
        self.guess_list = WORD_LISTS[new_guess_list.title()]

    def set_alphabet(self, new_letters):
        """Sets alphabet from which words can be guessed"""
        if new_letters.lower() not in map(str.lower, LETTERS):
            raise InvalidSettingsException(
                f"{new_letters} is not a valid alphabet. Available alphabets: {', '.join(LETTERS)}"
            )
        self.valid_letters = LETTERS[new_letters.title()]


class InvalidGuessException(Exception):
    """Exception when a guess input isn't valid"""


class InvalidSettingsException(Exception):
    """Exception when a guess input isn't valid"""


class NoWordsException(Exception):
    """Exception when there are no words to be chosen"""


class WordleGame:
    """Handles a single game, each new word to be guessed is a new game"""

    def __init__(self, word, valid_letters, valid_words):
        assert len(word) > 0
        self.word = word
        self.valid_words = valid_words
        self.valid_letters = valid_letters
        self.guessed_letters = set()
        self.guesses = []
        self.won = False

    def guess(self, guess):
        """Takes guess input, handles it, returns whether it's right and analysis of letters"""
        if self.won:
            raise InvalidGuessException("Start a new game before guessing!")
        self._check_valid_guess(guess)
        self.guessed_letters.update(guess)
        result = self._analyze_guess(guess)
        self.guesses.append(result)
        self.won = set(lg.guess for lg in result) == {Guess.CORRECT}
        return self.won

    def get_letters_not_tried(self):
        return "".join(sorted(self.valid_letters - self.guessed_letters))

    def get_letters_definitely_in(self):
        return "".join(sorted(self.guessed_letters & set(self.word)))

    def get_letters_definitely_out(self):
        return "".join(sorted(self.guessed_letters - set(self.word)))

    def _check_valid_guess(self, guess):
        """Checks if a word is valid to be guessed, raises an exception if not"""
        if guess == self.word:
            return
        if len(guess) != len(self.word):
            raise InvalidGuessException(
                f"Guess needs to be {len(self.word)} letters long!"
            )
        if not set(guess).issubset(self.valid_letters):
            raise InvalidGuessException(f"{guess!r} contains invalid characters!")
        if self.valid_words and guess not in self.valid_words:
            raise InvalidGuessException(f"{guess!r} is not a valid word!")

    def _analyze_guess(self, guess):
        """Returns which of the letters in the guess are correct,
        in the wrong position, or not in the word"""

        n = len(self.word)
        result = [LetterGuess(c, Guess.INCORRECT) for c in guess]

        count = collections.Counter(self.word)

        # Mark all letters in the right position as green
        for i, c in enumerate(guess):
            if self.word[i] == c:
                result[i] = LetterGuess(c, Guess.CORRECT)
                count[c] -= 1

        # Mark letters in wrong position yellow
        for i, c in enumerate(guess):
            if result[i].guess == Guess.INCORRECT and count[c] > 0:
                result[i] = LetterGuess(c, Guess.WRONG_POSITION)
                count[c] -= 1

        return result


def load_lines(filename):
    """Loads lines from a file into list"""
    with open(filename, encoding="UTF-8") as file:
        lines = file.read().splitlines()
    return lines


# Load all lists when this file is loaded
for word_list in WORD_LISTS.values():
    word_list["words"] = list(
        map(str.lower, load_lines("wordLists/" + word_list["filename"]))
    )
print("wordle.py: All word lists loaded")
