# Password Strength Calculator

This simple script gives you an ability to see your password complexity using entropy as
a measure of password strength.

More information about this method here:

https://en.wikipedia.org/wiki/Password_strength#Entropy_as_a_measure_of_password_strength


This script takes no account of human language (words, repeat letters, etc.). so I slightly changed the basic formula. Now it reduces basic number of received bits by half. More important is not the difference of the symbols, but the number of symbols in password. It assumes that each character is chosen independently from a set characters with equal probability. The longer the password, the harder it is to pick up the key. However, it takes into account upper, lower cases of characters and also special symbols. Script adds some bonus points to complexity of your password.

Furthermore this program will check your passphrase in the password blacklist which have to be called *most_common_passwords.txt* and put into same folder with this script. Example of such passwords could be found here:

http://www.passwordrandom.com/most-popular-passwords


Example:

This script requires that you had the Python interpreter (version 3.5 and higher) already installed on your system.

```#!bash

$ python password_strength.py # possibly requires call of python3 executive instead of just python

Enter your password> HelloWorld!
4

```

The assessment is scored from 1 to 10, where 1 is awfully weak and 10 is extremely strong.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
