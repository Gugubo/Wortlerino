import io
from enum import Enum

from PIL import Image, ImageDraw
from ttf_opensans import opensans

from wordle_guess import Guess, LetterGuess

IMG_FONT = opensans(font_weight=900).imagefont(size=48)
SQUARE_WIDTH = 64
SQUARE_HEIGHT = 64
GAP = 5


class Color(Enum):
    """Colors for the squares"""

    INCORRECT = "49494d"
    WRONG_POSITION = "ccb129"
    CORRECT = "468c3f"


def get_dimensions(guesses: list[list[LetterGuess]]) -> tuple[int, int]:
    """Returns dimensions for the image"""
    num_guesses = len(guesses)

    if not num_guesses:
        return (0, 0)

    word_len = len(guesses[0])

    width = (SQUARE_WIDTH * word_len) + (GAP * (word_len - 1)) + (GAP * 2)
    height = (SQUARE_HEIGHT * num_guesses) + (GAP * (num_guesses - 1)) + (GAP * 2)
    return (width, height)


def get_color(guess: Guess):
    """Returns color for type of guess"""
    if guess == Guess.CORRECT:
        color = Color.CORRECT
    elif guess == Guess.WRONG_POSITION:
        color = Color.WRONG_POSITION
    else:
        color = Color.INCORRECT

    return tuple(bytes.fromhex(color.value))


def get_image_from_guesses(guesses: list[list[LetterGuess]]):
    """Creates image out of list of guesses"""
    (width, height) = get_dimensions(guesses)
    out_img = Image.new("RGBA", (width, height))
    img_draw = ImageDraw.Draw(out_img)

    for attempt_idx, attempt in enumerate(guesses):
        for guess_idx, guess in enumerate(attempt):
            x0 = (guess_idx * SQUARE_WIDTH) + (GAP * (guess_idx)) + GAP
            y0 = (attempt_idx * SQUARE_HEIGHT) + (GAP * (attempt_idx)) + GAP

            x1 = x0 + SQUARE_WIDTH - 1
            y1 = y0 + SQUARE_HEIGHT - 1

            roundedness = 0
            img_draw.rounded_rectangle(
                [x0, y0, x1, y1], fill=get_color(guess.guess), radius=roundedness
            )

            (left, top, right, bottom) = IMG_FONT.getbbox(guess.letter.upper())
            font_width = right - left
            font_height = bottom - top

            img_draw.text(
                (
                    x0 + (SQUARE_WIDTH - font_width) / 2,
                    y0 + (SQUARE_HEIGHT - font_height) / 2 - top,
                ),
                guess.letter.upper(),
                font=IMG_FONT,
                fill=(255, 255, 255),
            )

    buf = io.BytesIO()
    out_img.save(buf, format="PNG")
    buf.seek(0)

    return buf
