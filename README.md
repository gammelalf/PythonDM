# PythonDM

## Dice

This tool provides the usual collection of dice, namely d4, d6, d8, d10, d20, d100.

To roll a single dice, type:
```python
d20()
```

You can also roll complexer compositions:
```python
2 * d6 + d4 + 2
```

Notes:
- The () are left away.
- It needs to be 2\*d6 instead of just 2d6.
- 2\*d6 means roll a d6 2-times.
- To multiply a single roll by 2 use 2\*d6().

It also provides a set of dice following a normal distribution available as gd\_

## Enemys

Enemy types are stored in json files in the enemys/ directory.
To create one in game (for example a Kobold) call:
```python
enemys.Kobold()
```

Notes on the json file:
- the file's name (without the .json) is the enemys name
- if a stat is left out of the file, the default will be used (see character.py)
- the max\_hp may be an integer or a string containing a "dice formula" to roll
- hp will be overwritten with max\_hp and can therefor be left away

## Battle

Here be dragons (TODO)
