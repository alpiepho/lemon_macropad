# SPDX-FileCopyrightText: 2021 Noe Ruiz for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#

import time
import board
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_macropad import MacroPad

BRIGHTNESS_LOW = 0.2
BRIGHTNESS_HIGH = 1.0

BLACK = 0x000000
GREEN = 0x00FF00
YELLOW = 0xFFFF00
ORANGE = 0xFF8C00
RED = 0xFF0000

GREEN_DIM = 0x002200
YELLOW_DIM = 0x222200
ORANGE_DIM = 0x221200
RED_DIM = 0x220000

macropad = MacroPad()

for i in range(len(macropad.pixels)):
    macropad.pixels[i] = BLACK
macropad.pixels.brightness = BRIGHTNESS_HIGH

buttonpins = [board.KEY1, board.KEY2, board.KEY3, board.KEY4, board.KEY5, board.KEY6]

# The keycode sent for each button, will be paired with a control key
buttonkeys = [
    ConsumerControlCode.PLAY_PAUSE,
    ConsumerControlCode.FAST_FORWARD,
    ConsumerControlCode.VOLUME_INCREMENT,
    ConsumerControlCode.MUTE,
    ConsumerControlCode.VOLUME_DECREMENT,
    ConsumerControlCode.REWIND
]

cc = ConsumerControl(usb_hid.devices)

print("\n\nWaiting for button presses")

while True:
    # check each button
    event = macropad.keys.events.get()
    if event:
        i = event.key_number
        if event.pressed:
            macropad.pixels[i] = GREEN
        if event.released:
            print("\n\nButton #%d Pressed" % i)

            if i < len(buttonkeys):
                k = buttonkeys[i]  # get the corresp. keycode
                print('code: ' + str(k))
                cc.send(k)
            else:
                print()
            macropad.pixels[i] = BLACK
    time.sleep(0.01)
