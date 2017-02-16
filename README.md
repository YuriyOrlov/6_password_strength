# Password Strength Calculator

This simple script gives you an ability to see your password complexity using entropy as
a measure of password strength.

More information about this method here:

https://en.wikipedia.org/wiki/Password_strength#Entropy_as_a_measure_of_password_strength


This script takes no account of human language (words, repeat letters, etc.). so I slightly changed the basic formula. Now it reduces basic number of received bits by half. More important is not the difference of the symbols, but the number of symbols in password. It assumes that each character is chosen independently from a set characters with equal probability. The longer the password, the harder it is to pick up the key. However, it takes into account upper, lower cases of characters and also special symbols. Script adds some bonus points to complexity of your password.

Furthermore, this program will check your passphrase in the password blacklist. You could write path to your *blacklist.txt*  file with an additional parameter "--file <path_to_your_file>". Example of such passwords can be found here:

http://www.passwordrandom.com/most-popular-passwords

*ATTENTION*: This program needs additional library for usage - chardet.
More information about it here:

https://github.com/chardet/chardet
https://pypi.python.org/pypi/chardet

Before using script, please be sure, that you've done ```pip install chardet```.

Example:

This script requires that you had the Python interpreter (version 3.5 and higher) already installed on your system.

```#!bash

$ python password_strength.py # possibly requires call of python3 executive instead of just python

Enter your password> HelloWorld!
4

```
Another example of using script with console parameter '--file'.


```#!bash

$ python password_strength.py --file ./most_common_passwords.txt

Enter your password> HelloWorld!
4

```
If you need some exmaple of how to use arguments just type ```python password_strength.py --help```.

The assessment is scored from 1 to 10, where 1 is awfully weak and 10 is extremely strong.


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
