# Cryptology

Algorithms for cryptology implemented as part of a cryptology course.

## Prerequisites

You must have [Python 3](https://www.python.org/) installed on your machine.

## Project structure

### Folders

* **assets** - images or other files that can be used to test some cipher algorithms.
* **outputs** - ciphered/deciphered assets
* **src** - functions and classes (math, cipher algorithms, helpers, ..)
* **tests** - unit tests

## GS15 cryptology course project

### The project

We had to implement 2 algorithms for the course's project:
- Threefish
- CramerShoup (with SHA-1 as hash function)

### How to run the project

We've built a simple cli, using [curses](https://docs.python.org/3/howto/curses.html), that allows the user to easily play with these 2 cipher algorithms and SHA-1.

The script that launchs the cli is at the root of the project. So you just have to go inside the project's directory with a terminal, and execute the script with Python 3:

```
python3 cli.py
```

**WARNING**
The Threefish decryption option in the cli is possessed by **dark magic**, and works only once in two.
It may be a problem with stdin/stdout.
So you can use *cli.py* for Threefish, but they may be some problems.
We built another cli (less advanced, but this one works perfectly) for Threefish. To run it, go to
the root of the project and execute this script with Python 3:

```
python3 cli_threefish.py
```

## Run the tests

```
python3 -m unittest discover tests
```

## Built With

* [Python 3](https://www.python.org/)
* [curses](https://docs.python.org/3/howto/curses.html)

## Authors

* Antoine Prudhomme - Initial work - [prudywsh](https://github.com/prudywsh)
* Alexis Grosjean - [Enilarik](https://github.com/Enilarik)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
