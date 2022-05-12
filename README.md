
# lemon_macropad

Modification of lemon_keypad to run on 12 key macropad hardware.  This project allows setting up an Adafruit Macropad with various key mappings.  When a btton is pressed, that key mapping is sent via usb to the host PC.  Think of this as a simple customizable keyboard.

The concept was expanded beyond just sending ConsumerCodes as the lemon_keypad did, to sending strings of characters and Keycodes.  A previous implementation involved reading the button configurations from a text file,
but a simpler version was created.  To change the mappings, a use can edit the code.py directly.

This supports a color code for the pressed and "off" state.  The "off" state color os useful to color code your operations.

IMPORTANT NOTE: Do not add text strings with critical passwords.  THIS IS NOT SECURE. All strings are in plain text in the code.py file.

As this was being developed, we discovered another similar project by [Phillip Burgess](https://cdn-learn.adafruit.com/downloads/pdf/macropad-hotkeys.pdf) that is a more flexible design.  I would argue that this design is simpler, but the reader can judge.

I aslo found this [Macropad Guide](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-macropad-rp2040.pdf) quite useful.  Very thorough on the Macropad and CircuitPython in general.


# Example of code.py table

<pre>
# NOTE: user can edit this table with care.  
#       number 1-12 supported, 
#       colors should match color_dict
#       code value should match code_dict
buttons = [
    #      number,  colorOn,    colorOff,       type,       value
    Button(1,       'GREEN',    'BLACK_DIM',    'code',     'PLAY_PAUSE'),
    Button(2,       '0x440000', '0x111111',     'text',     'enter 123'),
    Button(10,      'WHITE',    '0x111111',     'text',     'enter abc'),
    Button(11,      'BLUE',     '0x111111',     'keys',     'UP_ARROW'),
]
</pre>

# Original REAME.txt

From: https://learn.adafruit.com/qtpy-lemon-mechanical-keypad-macropad

This bundle contains two folders, one each for CircuitPython 6.x and CircuitPython 7.x. You must use the files that match the version of CircuitPython you're using, e.g. if you are using CircuitPython 6, you will copy the files from the CircuitPython 6.x folder to your CIRCUITPY drive.

To use this project bundle, simply copy the contents of the CircuitPython version folder you're using from the zip file to your CIRCUITPY drive.
Contents in each version include:
* the code.py file
* the lib/ folder and all of its contents (including subfolders and .mpy or .py files)
* any assets (such as images, sounds, etc.)

NOTE: This will replace the current code.py, and the lib folder and its contents. Back up any desired code before copying these files!

 This zip was downloaded from https://learn.adafruit.com/qtpy-lemon-mechanical-keypad-macropad/code on May  7, 2022.

# List of Codes

<pre>
Keycode:
C
M
UP_ARROW
SPACE
A
B
D
E
F
G
H
I
J
K
L
N
O
P
Q
R
S
T
U
V
W
X
Y
Z
ONE
TWO
THREE
FOUR
FIVE
SIX
SEVEN
EIGHT
NINE
ZERO
ENTER
RETURN
ESCAPE
BACKSPACE
TAB
SPACEBAR
MINUS
EQUALS
LEFT_BRACKET
RIGHT_BRACKET
BACKSLASH
POUND
SEMICOLON
QUOTE
GRAVE_ACCENT
COMMA
PERIOD
FORWARD_SLASH
CAPS_LOCK
F1
F2
F3
F4
F5
F6
F7
F8
F9
F10
F11
F12
PRINT_SCREEN
SCROLL_LOCK
PAUSE
INSERT
HOME
PAGE_UP
DELETE
END
PAGE_DOWN
RIGHT_ARROW
LEFT_ARROW
DOWN_ARROW
KEYPAD_NUMLOCK
KEYPAD_FORWARD_SLASH
KEYPAD_ASTERISK
KEYPAD_MINUS
KEYPAD_PLUS
KEYPAD_ENTER
KEYPAD_ONE
KEYPAD_TWO
KEYPAD_THREE
KEYPAD_FOUR
KEYPAD_FIVE
KEYPAD_SIX
KEYPAD_SEVEN
KEYPAD_EIGHT
KEYPAD_NINE
KEYPAD_ZERO
KEYPAD_PERIOD
KEYPAD_BACKSLASH
APPLICATION
POWER
KEYPAD_EQUALS
F13
F14
F15
F16
F17
F18
F19
F20
F21
F22
F23
F24
LEFT_CONTROL
CONTROL
LEFT_SHIFT
SHIFT
LEFT_ALT
ALT
OPTION
LEFT_GUI
GUI
WINDOWS
COMMAND
RIGHT_CONTROL
RIGHT_SHIFT
RIGHT_ALT
RIGHT_GUI
modifier_bit

ConsumerControlCode:
PLAY_PAUSE
MUTE
RECORD
FAST_FORWARD
REWIND
SCAN_NEXT_TRACK
SCAN_PREVIOUS_TRACK
STOP
EJECT
VOLUME_DECREMENT
VOLUME_INCREMENT
BRIGHTNESS_DECREMENT
BRIGHTNESS_INCREMENT
</pre>

# TODO
- expand to use sequences of Keycodes
- expand to use general sequences of chars and Keycodes

# References
- https://learn.adafruit.com/qtpy-lemon-mechanical-keypad-macropad
- https://github.com/Neradoc/Circuitpython_Keyboard_Layouts
- https://cdn-learn.adafruit.com/downloads/pdf/macropad-hotkeys.pdf
- https://cdn-learn.adafruit.com/downloads/pdf/adafruit-macropad-rp2040.pdf
