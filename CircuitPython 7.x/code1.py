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

class Button():
    def __init__(self, number, colorOn, colorOff, type, value):
        self.number = number
        self.colorOn = colorOn
        self.colorOff = colorOff
        self.type = type
        self.value = value

# NOTE: user can edit this table with care.  
#       number 1-12 supported, 
#       colors should match color_dict
#       code value should match code_dict
buttons = [
    #      number,  colorOn,    colorOff,       type,       value
    Button(1,       'GREEN',    'BLACK_DIM',    'code',     'PLAY_PAUSE'),
    Button(2,       '0x440000', '0x111111',     'text',     'enter 123'),
    Button(10,      'WHITE',    '0x111111',     'text',     'enter abc'),
]

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

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
cc = ConsumerControl(usb_hid.devices)
macropad = MacroPad()
text_lines = macropad.display_text()
text_lines.show()

def clearText():
    global text_lines
    text_lines[0] = ''
    text_lines[1] = ''
    text_lines[2] = ''

def setText(n, s):
    global text_lines
    text_lines[n] = s

def sendText():
    global text_lines
    text_lines.show()

def get_colorOn(index):
    for b in buttons:
        if index+1 == b.number:
            if b.value.startswith('0x'):
                return int(b.value, 16)
            try:
                return color_dict[b.value]
            except:
                return color_dict['WHITE']
    return color_dict['WHITE']

def get_colorOff(index):
    for b in buttons:
        if index+1 == b.number:
            if b.value.startswith('0x'):
                return int(b.value, 16)
            try:
                return color_dict[b.value]
            except:
                return color_dict['BLACK']
    return color_dict['BLACK']

def get_button(index):
    for b in buttons:
        if index+1 == b.number:
            return b
    return None

def get_code(s):
    try:
        return code_dict[s], s
    except:
        return code_dict['MUTE'], 'MUTE'

# check all macropad keys and process key press
def check_keys():
    global text_lines
    event = macropad.keys.events.get()
    if event:
        i = event.key_number
        if event.pressed:
            macropad.pixels[i] = get_colorOn(i)
        if event.released:
            clearText()
            setText(1, "Button #%d Pressed" % (i+1))
            b = get_button(i)
            if b != None:
                if b.type == TYPE_CODE:
                    code, s = get_code(b.value)
                    setText(2, 'code: ' + s)
                    cc.send(code)
                else:
                    setText(2, 'text: ' + str(b.value))
                    layout.write(b.value)
            sendText()
            macropad.pixels[i] = get_colorOff(i)


# check macropad encoder and display current settings
last_encoder = macropad.encoder
def check_encoder():
    global text_lines
    global last_position
    if macropad.encoder != last_encoder:
        index = abs(macropad.encoder) % len(buttons)
        b = buttons[index]
        clearText()
        setText(1, f'\n\n\n{b.number:2}: "{b.value}"')
        sendText()
    last_encoder = macropad.encoder

# update neopixel off colors
for i in range(len(macropad.pixels)):
    macropad.pixels[i] = get_colorOff(i)
macropad.pixels.brightness = 1.0

# starting message
clearText()
setText(1, 'Waiting for button')
setText(2, 'presses')
sendText()

# main loop
while True:
    check_keys()
    check_encoder()
    time.sleep(0.01)
