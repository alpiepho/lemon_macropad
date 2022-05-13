# SPDX-FileCopyrightText: 2021 Noe Ruiz for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode
from adafruit_macropad import MacroPad

class Button():
    def __init__(self, number, colors, index, type, value):
        self.number = number
        self.colors = colors
        self.index = index
        self.type = type
        self.value = value

# NOTE: user can edit this table with care.  
#       number 1-12 supported, 
#       colors should match color_dict
#       code value should match code_dict
#           off,            pressed     off             pressed ...
colors0 = ['BLACK_DIM',     'GREEN'                             ]
colors1 = ['BLACK_DIM',     'RED',      'BLACK_DIM',    'GREEN' ]
colors2 = ['0x111111',      '0x440000'                          ]
colors3 = ['0x111111',      'WHITE'                             ]
colors4 = ['BLACK_DIM',     'GREEN'                             ]
colors7 = ['GREEN_DIM',     'BLACK',    'RED_DIM',      'BLACK' ] # mute off, mute on...
buttons = [
    #      number,      colors,       index,       type,       value
    Button(1,           colors1, 0,     'text',     ''                  ), # cycle colors
    # Button(2,           colors2, 0,     'text',     'enter 123'         ),
    # Button(3,           colors3, 0,     'text',     'enter abc'         ),
    # Button(4,           colors4, 0,     'code',     'PLAY_PAUSE'        ),
    Button(7,           colors7, 0,     'keys',     'CONTROL SHIFT M'   ), # Teams Mute
    Button(10,          colors0, 0,     'keys',     'WINDOWS ALT TAB'   ), # show all windows
    Button(11,          colors0, 0,     'keys',     'RIGHT_ARROW'       ), # rigtt
    Button(12,          colors0, 0,     'keys',     'ENTER'             ), # select
]

# NOTE: use the following to find valid strings
# def dump_codes():
#     print()
#     print('ConsumerControlCode:')
#     list = dir(ConsumerControlCode)
#     for c in list:
#         if not c.startswith('_'):
#             print(c)

# def dump_keys():
#     print()
#     print('Keycode:')
#     list = dir(Keycode)
#     for c in list:
#         if not c.startswith('_'):
#             print(c)

# dump_keys()
# dump_codes()


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

cc = ConsumerControl(usb_hid.devices)
macropad = MacroPad()

text_lines = macropad.display_text()
text_lines.show()

def clear_text():
    global text_lines
    text_lines[0].text = ''
    text_lines[1].text = ''
    text_lines[2].text = ''

def set_text(n, s):
    global text_lines
    text_lines[n].text = s

def send_text():
    global text_lines
    text_lines.show()

def get_color(index):
    for b in buttons:
        if index+1 == b.number:
            # next color and update index
            color = b.colors[b.index]
            print(color)
            b.index = b.index + 1
            if b.index >= len(b.colors):
                b.index = 0
            # convert color string
            if color.startswith('0x'):
                return int(color, 16)
            try:
                return color_dict[color]
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
        return getattr(ConsumerControlCode, s), s
    except:
        return getattr(ConsumerControlCode, 'MUTE'), 'MUTE'

def get_key(s):
    try:
        return getattr(Keycode, s), s
    except:
        return getattr(Keycode, 'SPACE'), 'SPACE'


# check all macropad keys and process key press
def check_keys():
    global text_lines
    event = macropad.keys.events.get()
    if event:
        i = event.key_number
        if event.pressed:
            macropad.pixels[i] = get_color(i)
        if event.released:
            clear_text()
            set_text(1, "Button #%d Pressed" % (i+1))
            b = get_button(i)
            if b != None:
                if b.type == 'code':
                    code, s = get_code(b.value)
                    set_text(2, 'code: ' + s)
                    cc.send(code)
                elif b.type == 'keys':
                    parts = b.value.split(' ')
                    set_text(2, 'key: ' + b.value)
                    for p in parts:
                        key, s = get_key(p)
                        print(s)
                        macropad.keyboard.press(key)
                    time.sleep(0.01)
                    for p in parts:
                        key, s = get_key(p)
                        macropad.keyboard.release(key)
                else:
                    set_text(2, 'text: ' + str(b.value))
                    macropad.keyboard_layout.write(b.value)
            send_text()
            macropad.pixels[i] = get_color(i)


# check macropad encoder and display current settings
last_encoder = macropad.encoder
def check_encoder():
    global text_lines
    global last_encoder
    if macropad.encoder != last_encoder:
        index = abs(macropad.encoder) % len(buttons)
        b = buttons[index]
        clear_text()
        set_text(1, f'{b.number:2}: {b.value}')
        send_text()
    last_encoder = macropad.encoder

# update neopixel off colors
for i in range(len(macropad.pixels)):
    macropad.pixels[i] = get_color(i)
macropad.pixels.brightness = 1.0

# starting message
clear_text()
set_text(1, 'Waiting for button')
set_text(2, 'presses')
send_text()

# main loop
while True:
    check_keys()
    check_encoder()
    time.sleep(0.01)
