"""
https://en.wikipedia.org/wiki/Enigma_rotor_details#Rotor_wiring_tables
http://mckoss.com/enigma-simulator-js/  #we used this to make sure our code is encrypting correctly

reflector = B
plugboard = A-X, E-F, J-R
rotors = rotor1-rotor2-rotor3
key settings = CAT

reflector, 1st_rotor, 2nd_rotor, 3rd_rotor, plugboard, keyboard
the signal follows through the pathway described above starting from the keyboard up to the reflector and back to the keyboard
the forward functions defines the path from the keyboard to the reflector and from the right pair of the components to the left

Each component( plugboard, rotors and reflector) has two pairs of strings that contain all the alphabets
for the plugboard the right pair is ordered and the left pair only few letters are swapped
for the rotors and reflector the left pair is ordered and the right pair is jumbled(we used the historical enigma wiring)

# >>> encrypt('okay')  # commented this out to test the reverse, because this rotates the rotors which would result in
# 'YNST'               # a different output

>>> encrypt('ynst')
'OKAY'

"""

from typing import List

from Logic import precondition


class Keyboard:
    """
    >>> k = Keyboard()
    >>> k.forward('A')
    0
    >>> k.backward(0)
    'A'
    >>> k.backward(25)
    'Z'
    """

    def forward(self, letter: str):
        # finds the index or the position of the letter entered, which then can be passed to the plugboard
        letter = letter.upper()
        position = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(letter)
        return position

    def backward(self, position: int):
        # converts back the position of the letter it receives from the plugboard to the final encrypted letter
        letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[position]
        return letter


class Plugboard:
    """
    >>> p = Plugboard(["AX","CY"])
    >>> p.right
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    >>> p.left
    'XBYDEFGHIJKLMNOPQRSTUVWACZ'
    >>> p.forward(0)
    23
    >>> p.backward(23)
    0
    """

    def __init__(self, pairs: List[str]):
        # precondition(len(str) == 2)
        self.left = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.right = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for pair in pairs:
            # for each pair of letters, this function swaps their position in the left pair of the plugboard
            firstletter = pair[0]
            secondletter = pair[1]
            positionfirst = self.left.find(firstletter)
            positionsecond = self.left.find(secondletter)
            self.left = self.left[:positionsecond] + firstletter + self.left[positionsecond+1:]
            self.left = self.left[:positionfirst] + secondletter + self.left[positionfirst + 1:]

    def forward(self, position:int):
        # takes the position number from the keyboard and looks for the letter with that position number in the right
        # pair, then returns the position number of that letter in the left pair
        letter = self.right[position]
        position = self.left.find(letter)
        return position

    def backward(self, position: int):
        # similar to forward function, except that it takes position number from the 3rd rotor and looks for the letter
        # with that position number in the LEFT pair, then returns the position number of that letter in the RIGHT pair
        letter = self.left[position]
        position = self.right.find(letter)
        return position


class Rotor:
    """
    >>> rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
    >>> rotor1.show()
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    EKMFLGDQVZNTOWYHXUSPAIBRCJ
    >>> rotor1.rotate()
    >>> rotor1.show()
    BCDEFGHIJKLMNOPQRSTUVWXYZA
    KMFLGDQVZNTOWYHXUSPAIBRCJE
    >>> rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
    >>> rotor1.rotatetoletter("G")
    >>> rotor1.show()
    GHIJKLMNOPQRSTUVWXYZABCDEF
    DQVZNTOWYHXUSPAIBRCJEKMFLG

    """

    def __init__(self, wiring: str, notch: str):
        self.left = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.right = wiring
        self.notch = notch  # determines the manner of rotation of the rotors

    def forward(self, position: int):
        letter = self.right[position]
        position = self.left.find(letter)
        return position
    # these forward and backward functions are similar to the ones in the plugboard

    def backward(self, position: int):
        letter = self.left[position]
        position = self.right.find(letter)
        return position

    def show(self):  # to test the rotate and rotatetoletter functions below
        print(self.left)
        print(self.right)

    def rotate(self, n=1):
        # rotates the rotors by moving the first letters to the end of the strings
        for i in range(n):
            self.left = self.left[1:] + self.left[0]
            self.right = self.right[1:] + self.right[0]

    def rotatetoletter(self, letter:str):
        precondition(len(letter) == 1)
        n = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(letter)
        self.rotate(n)


class Reflector:

    def __init__(self, wiring: str):
        self.left = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.right = wiring  # we used the historical enigma reflector wiring

    def reflect(self, position:int):
        # takes the position number from the rotor and looks for the letter with that position number in the right
        # pair, then looks for that letter in the left pair and returns its position number
        letter = self.right[position]
        position = self.left.find(letter)
        return position


class Enigma:

    def __init__(self, reflector, rotor1, rotor2, rotor3, plugboard, keyboard):
        self.re = reflector
        self.r1 = rotor1
        self.r2 = rotor2
        self.r3 = rotor3
        self.pb = plugboard
        self.kb = keyboard

    def key_setting(self, key: str):
        # sets the starting letters of the rotors
        precondition(len(key) == 3)
        self.r1.rotatetoletter(key[0])
        self.r2.rotatetoletter(key[1])
        self.r3.rotatetoletter(key[2])

    def encipher(self, letter: str):
        if self.r2.left[0] == self.r2.notch and self.r3.left[0] == self.r3.notch:
            # all 3 rotors rotate when the 2nd and 3rd rotors match their turnover notches
            self.r3.rotate()
            self.r2.rotate()
            self.r1.rotate()
        elif self.r3.left[0] == self.r3.notch:
            # the 2nd and 3rd rotor rotates when the top letter of the 3rd rotor matches its turnover notch
            self.r3.rotate()
            self.r2.rotate()
        else:
            # the 3rd rotor always rotates
            self.r3.rotate()

        # moves the signal passed by the letter through each component of the enigma and returns the encrypted value
        position = self.kb.forward(letter)
        position = self.pb.forward(position)
        position = self.r3.forward(position)
        position = self.r2.forward(position)
        position = self.r1.forward(position)
        position = self.re.reflect(position)
        position = self.r1.backward(position)
        position = self.r2.backward(position)
        position = self.r3.backward(position)
        position = self.pb.backward(position)
        letter = self.kb.backward(position)
        return letter


# historical enigma rotor and reflector wiring that we used
rotor_I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
rotor_II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
rotor_IV = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

# creating objects and setting the keys for the enigma
Kb = Keyboard()
Pb = Plugboard(["AX", "EF", "JR"])
ENIGMA = Enigma(B, rotor_IV, rotor_II, rotor_I, Pb, Kb)
ENIGMA.key_setting('CAT')


def encrypt(word: str) -> str:
    encrypted_text = ""
    for letter in word:
        encrypted_text = encrypted_text + ENIGMA.encipher(letter)
    return encrypted_text
