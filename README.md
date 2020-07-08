# PythonDM

## Dice

In order to roll dices use the function `dice.roll()`.
It takes a dice containing expression as a string and evaluates it.

Examples:
```python
>>> dice.roll("d20")
11
>>> dice.roll("2d6 + 2")
8
>>> dice.roll("d6 + 2d8")
22
```

The function can also take a second optional argument. This is a function used for
rolling a single dice. It takes an integer and returns an integer.

There are some different types of dice provided:
- `dice.normal` a normal dice; the results are all equally likely
- `dice.gauss` a dice whose results follow a normal distribution
- `dice.lowest` always rolls the lowest possible value
- `dice.highest` always rolls the highest possible value
- `dice.expected` always rolls the expected average of a normal dice
If no dice is specified the `dice.normal` is used.

Examples:
```python
>>> roll("d20", dice.gauss)
11
>>> roll("2d6 + 1d8 + 3", dice.lowest)
6
>>> roll("6d12  + 18", dice.expected)
57
```

## Sheets

Sheets for characters (probably enemys) are stored in the sheets directory.
This directory (and its subdirectories) will be scanned for json files.

To access a sheet use:
```python
sheets.<subdir>.<sheet>
```

The enemys subdir will also be available as just
```python
enemys.<sheet>
```

## Battle

A battle is a collection of characters.

To add characters, use the function
```python
battle.add(character)
```
It takes any number of arguments. These can be:

- A Character object
- A sheet object
- A number followed by any other valid argument will add the argument number-times
- A list will call the function again on its entries

To sort the characters by their initiative (and make them determine it in the first place) use:
```python
battle.order()
```

For player rolls, the script will ask for input.
If characters' initiative matches, a second, third, etc. roll will be made.
