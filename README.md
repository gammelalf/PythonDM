# PythonDM

## Dice

This tool provides the function "roll(expr)" for evaluating dice containing expressions.

Examples:
```python
>>> roll("d20")
11
>>> roll("2d6 + 2")
8
>>> roll("d6 + 2d8")
22
```

The function also takes a second optional argument "dice". This is the function used for
rolling a single dice. It takes an integer and returns an integer. The tool also provides
the alternative "gauss\_dice" whose rolls follow the normal distribution.

Examples:
```python
>>> roll("d20", gauss_dice)
11
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
