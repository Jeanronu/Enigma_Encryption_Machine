"""
https://en.wikipedia.org/wiki/Enigma_rotor_details#Rotor_wiring_tables

reflector = A
plugboard = A-R, G-K, O-X
rotors = rotor1-rotor2-rotor3
message = A-> X

"""


class Keyboard:


    def forward(self, letter):
        signal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(letter)
        return signal

    def backward(self, signal):
        letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal]
        return letter

#k = Keyboard()
#print(k.forward("Z"))
#print(k.backward(0))



class Plugboard:

    def __init__(self, pairs):
        self.left = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.right = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for pair in pairs:
            firstletter = pair[0]
            secondletter = pair[1]
            positionfirst = self.left.find(firstletter)
            positionsecond = self.left.find(secondletter)
            self.left = self.left[:positionsecond] + firstletter + self.left[positionsecond+1:]
            self.left = self.left[:positionfirst] + secondletter + self.left[positionfirst + 1:]

# p = Plugboard(["AX","CY"])
# print(p.left)
# print(p.right)

    def forward(self, signal):
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

    def backward(self, signal):
        letter = self.left[signal]
        signal = self.right.find(letter)
        return signal

# p = Plugboard(["AB","CE"])
# print(p.forward(2))

class Rotor:

    def __init__(self, wiring, notch):
        self.left = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.right = wiring
        self.notch = notch

    def forward(self, signal):
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

    def backward(self, signal):
        letter = self.left[signal]
        signal = self.right.find(letter)
        return signal

    def show(self):
        print(self.left)
        print(self.right)
        print("")

    def rotate(self, n=1):
        for i in range(n):
            self.left = self.left[1:] + self.left[0]
            self.right = self.right[1:] + self.right[0]

    def rotatetoletter(self, letter):
        n = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(letter)
        self.rotate(n)



rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
rotor4 = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
rotor5 = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z")

# print(rotor3.forward(0))

# rotor1.show()
# rotor1.rotatetoletter("G")
# rotor1.show()

class Reflector:

    def __init__(self, wiring):
        self.left = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.right = wiring


    def reflect(self, signal):
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal


A = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
C = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")


Kb = Keyboard()
Pb = Plugboard(["AB", "CD", "EF"])

# letter = "A"
# signal = Kb.forward(letter)
# signal = Pb.forward(signal)
# signal = rotor3.forward(signal)
# signal = rotor2.forward(signal)
# signal = rotor1.forward(signal)
# signal = A.reflect(signal)
# signal = rotor1.backward(signal)
# signal = rotor2.backward(signal)
# signal = rotor3.backward(signal)
# signal = Pb.backward(signal)
# letter = Kb.backward(signal)
# print(letter)


class Enigma:

    def __init__(self, re, r1, r2, r3, pb, kb):
        self.re = re
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.pb = pb
        self.kb = kb

    def key_setting(self, key):
        self.r1.rotatetoletter(key[0])
        self.r2.rotatetoletter(key[1])
        self.r3.rotatetoletter(key[2])

    def encipher(self, letter: str):
        if self.r2.left[0] == self.r2.notch and self.r3.left[0] == self.r3.notch:
            self.r3.rotate()
            self.r2.rotate()
            self.r1.rotate()
        elif self.r3.left[0] == self.r3.notch:
            self.r3.rotate()
            self.r2.rotate()
        else:
            self.r3.rotate()

        signal = self.kb.forward(letter)
        signal = self.pb.forward(signal)
        signal = self.r3.forward(signal)
        signal = self.r2.forward(signal)
        signal = self.r1.forward(signal)
        signal = self.re.reflect(signal)
        signal = self.r1.backward(signal)
        signal = self.r2.backward(signal)
        signal = self.r3.backward(signal)
        signal = self.pb.backward(signal)
        letter = self.kb.backward(signal)
        return letter


ENIGMA = Enigma(B, rotor4, rotor2, rotor1, Pb, Kb)

# print(ENIGMA.encipher("A"))

ENIGMA.key_setting("CAT")

# ENIGMA.r2.show()
#
# message = "0234895"
# cipher_text = ""
# for letter in message:
#     if letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#         cipher_text = cipher_text + ENIGMA.encipher(letter)
#     else:
#         hi = 0
# print(cipher_text)


