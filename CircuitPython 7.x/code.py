# SPDX-FileCopyrightText: 2021 Noe Ruiz for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
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

color_dict = {
    'WHITE': 0xFFFFFF,
    'BLACK': 0x000000,
    'GREEN': 0x00FF00,
    'YELLOW': 0xFFFF00,
    'ORANGE': 0xFF8C00,
    'RED': 0xFF0000,
    'BLUE': 0x0000FF,
    'WHITE_DIM': 0xFFFFFF,
    'BLACK_DIM': 0xFFFFFF,
    'GREEN_DIM': 0x002200,
    'YELLOW_DIM': 0x222200,
    'ORANGE_DIM': 0x221200,
    'RED_DIM': 0x220000,
    'BLUE_DIM': 0x000022,
}

code_dict = {
    'BRIGHTNESS_DECREMENT': ConsumerControlCode. BRIGHTNESS_DECREMENT,
    'BRIGHTNESS_INCREMENT': ConsumerControlCode. BRIGHTNESS_INCREMENT,
    'EJECT': ConsumerControlCode. EJECT,
    'FAST_FORWARD': ConsumerControlCode. FAST_FORWARD,
    'MUTE': ConsumerControlCode. MUTE,
    'PLAY_PAUSE': ConsumerControlCode. PLAY_PAUSE,
    'RECORD': ConsumerControlCode. RECORD,
    'REWIND': ConsumerControlCode. REWIND,
    'SCAN_NEXT_TRACK': ConsumerControlCode. SCAN_NEXT_TRACK,
    'STOP': ConsumerControlCode. STOP,
    'VOLUME_DECREMENT': ConsumerControlCode. VOLUME_DECREMENT,
    'VOLUME_INCREMENT': ConsumerControlCode. VOLUME_INCREMENT,
}

class Button():
    number = 1
    colorOn = color_dict['WHITE']
    colorOff = color_dict['BLACK']
    type = TYPE_CODE
    codestr = ''
    value = Keycode.SPACE
buttons = []

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
cc = ConsumerControl(usb_hid.devices)
macropad = MacroPad()


def parse_color(s):
    if s.startswith('0x'):
        return int(s, 16)
    else:
        try:
            value = color_dict[s]
        except:
            value = color_dict['WHITE']
    return value

def parse_type(s):
    value = TYPE_TEXT
    if s.lower() == 'code':
        value = TYPE_CODE
    return value

def parse_code(s):
    try:
        value = code_dict[s]
    except:
        value = code_dict['MUTE']
    return value

def get_colorOn(index):
    for b in buttons:
        if index+1 == b.number:
            return b.colorOn
    return color_dict['WHITE']

def get_colorOff(index):
    for b in buttons:
        if index+1 == b.number:
            return b.colorOff
    return color_dict['BLACK']

def get_button(index):
    for b in buttons:
        if index+1 == b.number:
            return b
    return None

def check_keys():
    event = macropad.keys.events.get()
    if event:
        i = event.key_number
        if event.pressed:
            macropad.pixels[i] = get_colorOn(i)
        if event.released:
            print("\n\nButton #%d Pressed" % (i+1))
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
            macropad.pixels[i] = get_colorOff(i)


last_position = macropad.encoder
def check_encoder():
    global last_position
    if macropad.encoder != last_position:
        index = abs(macropad.encoder) % len(buttons)
        b = buttons[index]
        if b.type == TYPE_CODE:
            print(f'\n\n\n{b.number:2}: {b.codestr}')
        else:
            print(f'\n\n\n{b.number:2}: "{b.value}"')
    last_position = macropad.encoder




# read data.txt
data_found = True
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
            if len(parts) == 5:
                b = Button()
                b.number = int(parts[0].strip())
                b.colorOn = parse_color(parts[1].strip())
                b.colorOff = parse_color(parts[2].strip())
                b.type = parse_type(parts[3].strip())
                if b.type == TYPE_CODE:
                    b.codestr = parts[4].strip()
                    b.value = parse_code(parts[4].strip())
                else:
                    b.value = parts[4].replace('"', '').strip()
                buttons.append(b)
except Exception as err:
    data_found = False

# update neopixel colors from data.txt
for i in range(len(macropad.pixels)):
    macropad.pixels[i] = get_colorOff(i)
macropad.pixels.brightness = BRIGHTNESS_HIGH

# starting message
if data_found:
    print("\n\nWaiting for button presses")
else:
    print('Please provide data.txt with details about buttons.')

# main loop
while True:
    check_keys()
    check_encoder()
    time.sleep(0.01)

# TODO 
# - refactor
# - hold strings from data, convert when needed
# - test mode?
# - clear lcd icon
# - README 
# References - move to README
# https://github.com/Neradoc/Circuitpython_Keyboard_Layouts