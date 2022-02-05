"""Wordle-Bot for discord"""

import discord
from image_guesses import get_image_from_guesses
import wordle
import config

# Discord stuff
client = discord.Client()
TOKEN = config.TOKEN

# Constants
VERSION = 1.1

YELLOW = "🟨"
GREEN = "🟩"
BLACK = "⬜"

COLOR_CORRECT = 0x538D4E
COLOR_STANDARD = 0x8D7D4E
COLOR_ERROR = 0x8D4E4E

WIKILINK = "https://XX.wikipedia.org/wiki/"

COMMANDS = [
    "wort",
    "word",
    "wortle",
    "wordle",
    "wortlerino",
    "wordlerino",
    "w",
    "neu",
    "new",
    "nochmal",
    "again",
    "next",
    "guess",
    "n",
    "set",
]

# Stores all wordle states (one per channel)
wordle_states = {}


def parse_message(message):
    """Parses message and returns color and text to respond with
    Will only parse messages if first word is in commands
    If no further arguments are given, will try to start a new game
    If two arguments are given, second one is taken as a guess
    If three or more arguments are given, it's treated as trying  to change settings:
        word_list, guess_list, or length
        word_list and guess_list will take one argument to choose the list
        length will take two arguments as min_length and max_length, or one argument to set both to be the same"""
    split_message = message.content.split()
    number_of_messages = len(split_message)

    # Chooses the channel-specific wordle state
    if message.channel not in wordle_states:
        wordle_states[message.channel] = wordle.WordleState()
    wordle_state = wordle_states[message.channel]

    # Parse message based on number of words in it
    if number_of_messages == 0 or split_message[0].lower() not in COMMANDS:
        return None, None, None  # Ignore this message, it's not for this bot
    if number_of_messages == 1:
        # Make a new game (if one isn't already in progress)
        if not wordle_state.game or wordle_state.game.won:
            try:
                wordle_state.create_game()
                print("new game:", wordle_state.game.word)
                return (
                    False,
                    COLOR_CORRECT,
                    f"New game started! (Word has {len(wordle_state.game.word)} letters and is from word list {wordle_state.word_list['name']})",
                )
            except wordle.NoWordsException as ex:
                return False, COLOR_ERROR, str(ex)
        else:
            return False, COLOR_ERROR, "There's already a game in progress!"

    elif number_of_messages == 2:
        # Take a guess
        guess = split_message[1].lower()
        try:
            won = wordle_state.game.guess(guess)
            img = get_image_from_guesses(wordle_state.game.guesses)
            file = discord.File(img, "guesses.png")
            if won:
                guesses = wordle_state.game.guesses
                return (
                    True,
                    COLOR_CORRECT,
                    f"\nCongrats! You guessed right after {len(guesses)} guess{'es' if len(guesses)>1 else ''}.",
                    file,
                )
            else:
                return (
                    False,
                    COLOR_STANDARD,
                    f"Confirmed to be in the word: {wordle_state.game.get_letters_definitely_in()}\nNot yet tried: {wordle_state.game.get_letters_not_tried()}\nDefinitely not in the word: {wordle_state.game.get_letters_definitely_out()}",
                    file,
                )
        except wordle.InvalidGuessException as ex:
            return False, COLOR_ERROR, str(ex)

    elif number_of_messages == 3:
        # Change some settings
        if split_message[1].lower() in [
            "wordlist",
            "word_list",
            "words",
            "wl",
            "w",
            "worte",
            "wörter",
        ]:
            try:
                wordle_state.set_word_list(split_message[2])
                return (
                    False,
                    COLOR_CORRECT,
                    f"Word list has been changed to {split_message[2]}: {wordle.WORD_LISTS[split_message[2].title()]['description']}!",
                )
            except wordle.InvalidSettingsException as ex:
                return False, COLOR_ERROR, str(ex)
        elif split_message[1].lower() in [
            "guesslist",
            "guess_list",
            "guess",
            "guesses",
            "gl",
            "g",
        ]:
            try:
                wordle_state.set_guess_list(split_message[2])
                return (
                    False,
                    COLOR_CORRECT,
                    f"Guess list has been changed to {split_message[2]}: {wordle.WORD_LISTS[split_message[2].title()]['description']}!",
                )
            except wordle.InvalidSettingsException as ex:
                return False, COLOR_ERROR, str(ex)
        elif split_message[1].lower() in [
            "alphabet",
            "letters",
            "buchstaben",
            "characters",
        ]:
            try:
                wordle_state.set_alphabet(split_message[2])
                return (
                    False,
                    COLOR_CORRECT,
                    f"Alphabet has been changed to {split_message[2]}: {wordle.LETTERS[split_message[2].title()]['description']}!",
                )
            except wordle.InvalidSettingsException as ex:
                return False, COLOR_ERROR, str(ex)
        elif split_message[1] in ["length", "size", "länge", "l"]:
            new_length = split_message[2]
            if not new_length.isnumeric():
                return False, COLOR_ERROR, "New length must be a number!"
            try:
                wordle_state.set_length(int(new_length), int(new_length))
                return (
                    False,
                    COLOR_CORRECT,
                    f"Length for new words has been set to {new_length}.",
                )
            except wordle.InvalidSettingsException as ex:
                return False, COLOR_ERROR, str(ex)
        else:
            return (
                False,
                COLOR_ERROR,
                "Not a valid setting. Try word_list, guess_list, or length!",
            )

    elif number_of_messages == 4:
        # Change settings (because length may take two arguments)
        if split_message[1] in ["length", "size", "länge", "l"]:
            new_min_length = split_message[2]
            new_max_length = split_message[3]
            if not new_min_length.isnumeric() or not new_max_length.isnumeric():
                return False, COLOR_ERROR, "New length must be a number!"
            try:
                wordle_state.set_length(int(new_min_length), int(new_max_length))
                return (
                    False,
                    COLOR_CORRECT,
                    f"Length for new words has been set to {new_min_length}-{new_max_length}.",
                )
            except wordle.InvalidSettingsException as ex:
                return False, COLOR_ERROR, str(ex)
        else:
            return (
                False,
                COLOR_ERROR,
                "Not a valid setting. Try word_list, guess_list, or length!",
            )
    else:
        return False, COLOR_ERROR, "Too many words!"
    return False, COLOR_ERROR, "Are you talking to me? Something went wrong."


async def send_embed(channel, title, color, description, url=None, file=None):
    """Sends an embed to the specified channel"""
    embed = discord.Embed(
        title=title,
        colour=color,
        description=description,
    )
    embed.set_footer(text=f"Wortlerino v{VERSION}")
    if url:
        embed.url = url

    if file is not None:
        embed.set_image(url=f"attachment://{file.filename}")

    await channel.send(embed=embed, file=file)


@client.event
async def on_ready():
    """Connected to discord"""
    print("Ready.")
    print("Name:", client.user.name)
    print("ID:", client.user.id)
    print()


@client.event
async def on_message(message):
    """When a message is sent"""

    file = None
    won, color, response, *rest = parse_message(message)
    if rest:
        file = rest[0]

    if won is not None:
        print("Parsed message:", message.content)
        if won:
            await send_embed(
                message.channel,
                wordle_states[message.channel].game.word.upper(),
                color,
                response,
                WIKILINK.replace(
                    "XX", wordle_states[message.channel].word_list["language"]
                )
                + wordle_states[message.channel].game.word.title(),
                file=file,
            )
        else:
            await send_embed(message.channel, "", color, response, file=file)


# Start the whole thing
client.run(TOKEN)
