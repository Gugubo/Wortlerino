import io
from enum import Enum
from typing import List
from ttf_opensans import opensans
from PIL import Image, ImageDraw

from wordle_guess import LetterGuess, Guess

IMG_FONT = opensans(font_weight=600).imagefont(size=32)
SQUARE_WIDTH = 62
SQUARE_HEIGHT = 62
GAP = 5

class Color(Enum):
    INCORRECT = "787c7e"
    WRONG_POSITION = "c9b458"
    CORRECT = "6aaa64"

def get_dimensions(guesses: List[List[LetterGuess]]):
    num_guesses = len(guesses)

    if not num_guesses:
        return None

    word_len = len(guesses[0])

    width = (SQUARE_WIDTH * word_len) + (GAP * (word_len - 1)) + (GAP * 2)
    height = (SQUARE_HEIGHT * num_guesses) + (GAP * (num_guesses - 1)) + (GAP * 2)

    return (width, height)


def get_color(guess: Guess):
    if guess == Guess.CORRECT:
        color = Color.CORRECT
    elif guess == Guess.WRONG_POSITION:
        color = Color.WRONG_POSITION
    else:
        color = Color.INCORRECT

    return tuple(bytes.fromhex(color.value))


def get_image_from_guesses(guesses: List[List[LetterGuess]]):
    (width, height) = get_dimensions(guesses)
    out_img = Image.new("RGBA", (width, height))
    img_draw = ImageDraw.Draw(out_img)

    for attempt_idx, attempt in enumerate(guesses):
        for guess_idx, guess in enumerate(attempt):

            x0 = (guess_idx * SQUARE_WIDTH) + (GAP * (guess_idx)) + GAP
            y0 = (attempt_idx * SQUARE_HEIGHT) + (GAP * (attempt_idx)) + GAP

            x1 = x0 + SQUARE_WIDTH - 1
            y1 = y0 + SQUARE_HEIGHT - 1

            img_draw.rectangle([x0, y0, x1, y1], fill=get_color(guess.guess))
            font_width, font_height = IMG_FONT.getsize(guess.letter, None, None, None, 0)
            img_draw.text(
                (
                    x0 + (SQUARE_WIDTH / 2) - (font_width / 2),
                    y0 + (SQUARE_HEIGHT / 2) - (font_height / 2) - 5
                ),
                guess.letter,
                font=IMG_FONT,
                fill=(255, 255, 255),
            )

    buf = io.BytesIO()
    out_img.save(buf, format="PNG")
    buf.seek(0)

    return buf