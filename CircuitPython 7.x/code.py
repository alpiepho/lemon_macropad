# SPDX-FileCopyrightText: 2021 Noe Ruiz for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_macropad import MacroPad

BRIGHTNESS_LOW = 0.2
BRIGHTNESS_HIGH = 1.0

TYPE_CODE = 'code'
TYPE_TEXT = 'text'

WHITE = 0xFFFFFF
BLACK = 0x000000
GREEN = 0x00FF00
YELLOW = 0xFFFF00
ORANGE = 0xFF8C00
RED = 0xFF0000
BLUE = 0x0000FF

class Button():
    number = 1
    color = WHITE
    type = TYPE_CODE
    value = Keycode.SPACE
buttons = []

macropad = MacroPad()

for i in range(len(macropad.pixels)):
    macropad.pixels[i] = BLACK
macropad.pixels.brightness = BRIGHTNESS_HIGH


# The keycode sent for each button, will be paired with a control key
buttoncodes = [
    ConsumerControlCode.PLAY_PAUSE,
    ConsumerControlCode.FAST_FORWARD,
    ConsumerControlCode.VOLUME_INCREMENT,
    ConsumerControlCode.MUTE,
    ConsumerControlCode.VOLUME_DECREMENT,
    ConsumerControlCode.REWIND
]

# kbd = Keyboard(usb_hid.devices)

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)


cc = ConsumerControl(usb_hid.devices)

def parse_color(s):
    if s.startswith('0x'):
        return int(s, 16)
    else:
        value = WHITE
        s = s.upper()
        if s == 'WHITE':
            value = WHITE
        elif s == 'BLACK':
            value = BLACK
        elif s == 'GREEN':
            value = GREEN
        elif s == 'YELLOW':
            value = YELLOW
        elif s == 'RED':
            value = RED
        elif s == 'ORANGE':
            value = ORANGE
        elif s == 'BLUE':
            value = BLUE
        else:
            print('WARNING: given color string ' + s + ' is not known, using WHITE.')
    return value

def parse_type(s):
    value = TYPE_TEXT
    if s.lower() == 'code':
        value = TYPE_CODE
    return value

def parse_code(s):
    value = ConsumerControlCode.MUTE
    s = s.upper()
    if s == 'BRIGHTNESS_DECREMENT':
        value =ConsumerControlCode. BRIGHTNESS_DECREMENT
    elif s == 'BRIGHTNESS_INCREMENT':
        value = ConsumerControlCode.BRIGHTNESS_INCREMENT
    elif s == 'EJECT':
        value = ConsumerControlCode.EJECT
    elif s == 'FAST_FORWARD':
        value = ConsumerControlCode.FAST_FORWARD
    elif s == 'MUTE':
        value = ConsumerControlCode.MUTE
    elif s == 'PLAY_PAUSE':
        value = ConsumerControlCode.PLAY_PAUSE
    elif s == 'RECORD':
        value = ConsumerControlCode.RECORD
    elif s == 'REWIND':
        value = ConsumerControlCode.REWIND
    elif s == 'SCAN_NEXT_TRACK':
        value = ConsumerControlCode.SCAN_NEXT_TRACK
    elif s == 'STOP':
        value = ConsumerControlCode.STOP
    elif s == 'VOLUME_DECREMENT':
        value = ConsumerControlCode.VOLUME_DECREMENT
    elif s == 'VOLUME_INCREMENT':
        value = ConsumerControlCode.VOLUME_INCREMENT
    else:
        print('WARNING: given code string ' + s + ' is not known, using MUTE.')
    return value

def get_color(index):
    for b in buttons:
        if index+1 == b.number:
            return b.color
    return WHITE

def get_button(index):
    for b in buttons:
        if index+1 == b.number:
            return b
    return None

# read data.txt
try:
    with open('data.txt') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                continue
            if len(line) == 0:
                continue
            print(line)
            parts = line.split(':')
            if len(parts) == 4:
                b = Button()
                b.number = int(parts[0].strip())
                b.color = parse_color(parts[1].strip())
                b.type = parse_type(parts[2].strip())
                if b.type == TYPE_CODE:
                    b.value = parse_code(parts[3].strip())
                else:
                    b.value = parts[3].replace('"', '').strip()
                buttons.append(b)
except Exception as err:
    print(err)
    print('Please provide data.txt with details about buttons.')


print("\n\nWaiting for button presses")

while True:
    # check each button
    event = macropad.keys.events.get()
    if event:
        i = event.key_number
        if event.pressed:
            macropad.pixels[i] = get_color(i)
        if event.released:
            print("\n\nButton #%d Pressed" % i)
            b = get_button(i)
            if b != None:
                if b.type == TYPE_CODE:
                    print('code: ' + str(b.value))
                    cc.send(b.value)
                else:
                    print('text: ' + str(b.value))
                    layout.write(b.value)
            else:
                print()
            macropad.pixels[i] = BLACK
    time.sleep(0.01)
