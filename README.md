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
