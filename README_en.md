# CSP solver 
[Spanish version](./README.md)

## Introduction
`csp-arboles` is a proyect that started as a simpler (and automatized) way to solve levels in a
[game about trees and tents from the Google Play Store](https://play.google.com/store/apps/details?id=com.frozax.tentsandtrees&pcampaignid=web_share)
applying the concepts from my Heuristics and Optimization class.

### Level properties
- The levels are square grids of NxM with a certain amount of trees.
- Each tree has a tent assigned to it, which must be adyacent horizontally or vertically.
- In the square surrounding each tent there cannot be another tent.
- The sum of the tents for each row and column must be what was indicated for each row or column (it's possible to not indicate it).

## Requirements
`csp-arboles` requires [python constraint](https://pypi.org/project/python-constraint/) >= 1.4.0

In addition, `csp-arboles` has been developed using Python 3.10, although an older version of Python 3 could probably work.

## Usage
Really all that is needed from this github repository is the file `csp-arboles.py`.
Inside the `tests/` folder are some tests I made (except for `arboles0` and `arboles1`, the rest are levels from the game).

To execute, the file containing the problem is passed as an argument:
```
$ python csp-arboles ./tests/arboles0
```
A solution will be printed to standard output.

### Format of the problems
The program expects a textfile with the following data:
- Size of the problem: XxY
- Number of tents that must be in each column, separated by spaces.
- Number of tents that must be in each row, separy by spaces.
- Representation of the level by rows marking the trees with `x` and the blank spaces with `-`.

The example level (`arboles6`):
<figure>
    <img src="level.jpg" alt="Example of a level" width=300>
</figure>

Would be represented:
```
8x8
1 3 - 3 1 2 1 2
2 1 - - - 1 2 -
--x--x-x
--------
x-----x-
-x--xx--
------x-
x-------
---x-x--
----x---
```

This solver is also able to find solutions to levels for wich the number of tents in some row or column is not specified, like in the example.
Rows or columns for which it is not specified the number of tents are represented with `-`.

### Output
After finding a solution for the problem, it is printed to the terminal formatted for ease of reading.
Solving the example problem we obtain this solution:
```
    1   3       3   1   2   1   2
  +---+---+---+---+---+---+---+---+
2 |   | △ | ◻ |   | △ | ◻ |   | ◻ |
1 |   |   |   |   |   |   |   | △ |
  | ◻ | △ |   |   |   | △ | ◻ |   |
  |   | ◻ |   | △ | ◻ | ◻ |   |   |
  |   | △ |   |   |   | △ | ◻ | △ |
1 | ◻ |   |   | △ |   |   |   |   |
2 | △ |   |   | ◻ |   | ◻ | △ |   |
  |   |   |   | △ | ◻ |   |   |   |
  +---+---+---+---+---+---+---+---+
```

Tents are shown with triangles (△) and tress with squares (◻).

# License #

MIT License

Copyright (c) 2023, Yago Brotón Gutiérrez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


# Authors #

Yago Brotón Gutiérrez <100451322@alumnos.uc3m.es>
Bachelor in Computer Science and Engineering <https://www.uc3m.es/bachelor-degree/computer-science>
Universidad Carlos III de Madrid <https://www.uc3m.es/home>
