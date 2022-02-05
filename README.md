# Wortlerino

Wortlerino is a discord wordle bot. It will create a random word for you to guess. See [Wordle](https://www.powerlanguage.co.uk/wordle/) for the rules.

## Features

- You can use multiple different word lists and change them while the bot is running
- You can use separate word lists for generating a word and for words that you're allowed to guess (like the real Wordle)
- You can change the length of generated words

## Using

Type `wortlerino`, `new`, or `n` to create a new game.

Type `word`, `guess`, or `w` followed by a guess.

After guessing the right word, start a new game with `next`, `again`, or `n`. (Or use any of the other keywords, they all work the same.)

### Example

![Guessing Example](https://user-images.githubusercontent.com/29143981/152344303-a73410b3-ec3f-49cb-835e-8fb2d9ef36e6.png)

## Settings

Change a setting while the bot is running by typing: `wortlerino setting new_value`
They will come into effect when a new word is generated.

Available settings:

- `word_list`: Changes the list from which new words can be generated (default: _Wordle_)
- `guess_list`: Changes the list of words which are allowed as guesses (default: _Wordle-all_)
- `length`: Changes the length of new words (takes one or two values) (default: _4 - 6_)

### Example

![Settings Example](https://user-images.githubusercontent.com/29143981/152359584-476dbc9d-9a37-4a36-995d-2db91c11a25f.png)

## Included word lists

- _Wordle_: All possible wordle words

- _Wordle-all_: All possible wordle words + all words wordle accepts as input

- _Wikipedia_: List of all German Wikipedia-Article-Titles

- _Substantive_: A list of a few hundred German nouns

- _German_: A big word list including inflections (should probably only be used for guesses)

- _English_: A big word list

- _Spelunky_: A list of all words that appear in Spelunky 2

## Requirements

```
pip install -r requirements.txt
```

## Running it

1. Create a `config.py` with your token in it, for example:

```python
TOKEN = "bFqLkmKnVoo7r1Lbc6S41pK3T0Gm1Vz9ZZUua9Y64TfWDV05Aql5DznwRUx"
```

2. Run `wortlerino.py`

## License

[GPL](https://choosealicense.com/licenses/gpl-3.0/)
