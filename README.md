# PythonDM

## Conventions

### Attribute naming:

- names the user shouldn't be concerned about, start with a double "\_"
- functions the user should use, start with a single "\_"
- attribute the user should access, start without a "\_"

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

The enemys subdir will be available as just
```python
enemys.<sheet>
```

## Battle

Here be dragons (TODO)
